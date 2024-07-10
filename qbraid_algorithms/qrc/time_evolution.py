# Copyright (C) 2024 qBraid
#
# This file is part of the qBraid-SDK
#
# The qBraid-SDK is free software released under the GNU General Public License v3
# or later. You can redistribute and/or modify it under the terms of the GPL v3.
# See the LICENSE file in the project root or <https://www.gnu.org/licenses/gpl-3.0.html>.
#
# THERE IS NO WARRANTY for the qBraid-SDK, as per Section 15 of the GPL v3.

"""
Module for quantum time evolution using Krylov subspace methods.

"""
from collections import OrderedDict

import numpy as np
from bloqade.atom_arrangement import (
    AtomArrangement,
    Chain,
    Honeycomb,
    Kagome,
    Lieb,
    Rectangular,
    Square,
    Triangular,
)

# from bloqade.builder.waveform import PiecewiseLinear


class GeometryOptions:
    """Class for defining the geometric configuration of the atoms in the lattice."""

    def __init__(
        self,
        atom_arrangement_shape: str,
        lattice_spacing: float,
    ):
        atom_arrangement_shape_dictionary = {
            "Square": Square,
            "Chain": Chain,
            "Rectangular": Rectangular,
            "Honeycomb": Honeycomb,
            "Triangular": Triangular,
            "Lieb": Lieb,
            "Kagome": Kagome,
        }

        self.atom_arrangement: AtomArrangement = atom_arrangement_shape_dictionary.get(
            atom_arrangement_shape
        )
        self.lattice_spacing: float = lattice_spacing


class AnalogProgramEvolver:
    """Class for evolving program over discrete list of time steps.

    Attributes:
        num_atoms (int): Number of atoms in the system.
        amplitudes (List[float]): List of Rabi oscillation amplitudes.
        durations (List[float]): List of pulse durations.
        geometric_configuration (GeometryOptions): Configuration options for the geometric setup.
    """

    SUPPORTED_BACKENDS = ["local_simulator", "aquila"]

    def __init__(
        self,
        num_atoms: int,
        rabi_amplitudes: list[float],
        durations: list[float],
        geometric_configuration: GeometryOptions,
    ):
        """Initializes the AnalogEvolution with provided parameters.

        Args:
            num_atoms (int): Number of atoms in the system.
            rabi_amplitudes (list[float]): Rabi amplitudes for each pulse.
            durations (list[float]): Duration of each pulse.
            geometric_configuration (GeometryOptions): Geometric settings for the evolution.

        """
        self.num_atoms = num_atoms
        self.amplitudes = rabi_amplitudes
        self.durations = durations
        self.geometric_configuration = geometric_configuration

    def compute_rydberg_probs(self, counts: OrderedDict) -> np.ndarray:
        """Calculate the average probability distribution of Rydberg states over all shots.

        Args:
            counts (OrderedDict): An OrderedDict where keys are bitstring state representations
                and values are the counts of each state observed.

        Returns:
            np.ndarray: The probability of each state, averaged over all shots.
        """
        prob = np.zeros(self.num_atoms)

        total_shots = 0  # Total number of shots in the counts
        for key, val in counts.items():
            prob += np.array([float(bit) for bit in [*key]]) * val
            total_shots += val

        prob /= total_shots
        return prob

    def evolve(self, backend: str) -> np.ndarray:
        """Evolves program over discrete list of time steps"""
        amp_waveform = self.geometric_configuration.atom_arrangement(
            lattice_spacing=self.geometric_configuration.lattice_spacing
        ).rydberg.rabi.amplitude.uniform.constant(15.0, 4.0)
        program = amp_waveform.detuning.uniform.piecewise_linear(self.durations, self.amplitudes)

        if backend == "local_simulator":
            [emulation] = program.bloqade.python().hamiltonian()
            emulation.evolve(times=self.durations)

            return emulation.hamiltonian.tocsr(time=self.durations[-1]).toarray()

        if backend == "aquila":
            # TODO: Revise for async task handling to avoid blocking while waiting for results.
            bitstring_counts_batch: list[OrderedDict] = (
                program.braket.aquila.run_async(100).report().counts()
            )
            if (
                len(bitstring_counts_batch) != 1
            ):  # TODO: Double-check that counts list will always be length 1 here.
                raise ValueError("Expected a single batch of counts.")
            bitstring_counts = bitstring_counts_batch[0]
            return self.compute_rydberg_probs(bitstring_counts)

        raise ValueError(
            f"Backend {backend} is not supported. Supported backends are: {self.SUPPORTED_BACKENDS}"
        )
