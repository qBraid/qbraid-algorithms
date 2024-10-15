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
Module for quantum time evolution using emulator or QPU.

"""
from __future__ import annotations

from collections import OrderedDict
from decimal import Decimal
from typing import Optional

import numpy as np
from bloqade.atom_arrangement import Chain
from bloqade.builder.field import Detuning, RabiAmplitude
from bloqade.emulate.ir.state_vector import StateVector


class AnalogProgramEvolver:
    """Class for evolving program over discrete list of time steps.

    Attributes:
        atoms (Chain): Chain lattice.
        amplitudes (List[float]): List of Rabi oscillation amplitudes.
        durations (List[Decimal]): List of pulse durations.
        time_steps (list[float]): The times to evaluate the state vector.
    """

    SUPPORTED_BACKENDS = ["emulator", "qpu"]

    def __init__(
        self,
        atoms: Chain,
        rabi_amplitudes: list[float],
        durations: list[Decimal],
    ):
        """Initializes the AnalogEvolution with provided parameters.

        Args:
            atoms (Chain): Chain lattice.
            rabi_amplitudes (list[float]): Rabi amplitudes for each pulse.
            durations (list[Decimal]): Duration of each pulse.

        """
        self.atoms = atoms
        self.amplitudes = rabi_amplitudes
        self.durations = durations
        self.time_steps = self._get_time_steps(durations)

    @staticmethod
    def _get_time_steps(durations: list[Decimal]) -> list[float]:
        """Generate time steps from list of pulse durations."""
        return list(np.cumsum([0.0] + [float(d) for d in durations]))

    @staticmethod
    def compute_rydberg_probs(num_sites: int, counts: OrderedDict) -> np.ndarray:
        """Calculate the average probability distribution of Rydberg states over all shots.

        Args:
            num_sites (int): Number of sites in the chain lattice
            counts (OrderedDict): An OrderedDict where keys are bitstring state representations
                and values are the counts of each state observed.

        Returns:
            np.ndarray: The probability of each state, averaged over all shots.
        """
        prob = np.zeros(num_sites)

        total_shots = 0  # Total number of shots in the counts
        for key, val in counts.items():
            prob += np.array([float(bit) for bit in [*key]]) * val
            total_shots += val

        prob /= total_shots
        return prob

    def evolve(self, backend: str, state: Optional[StateVector] = None) -> np.ndarray:
        """Evolves program over discrete list of time steps"""
        rabi_amp: RabiAmplitude = self.atoms.rydberg.rabi.amplitude

        value = max(self.amplitudes)
        duration = sum(self.durations)
        detuning: Detuning = rabi_amp.uniform.constant(value, duration).detuning
        program = detuning.uniform.piecewise_linear(self.durations, self.amplitudes)

        if backend == "emulator":
            [emulation] = program.bloqade.python().hamiltonian()
            emulation.evolve(state=state, times=self.time_steps)
            return emulation.hamiltonian.tocsr(time=self.time_steps[-1]).toarray()

        if backend == "qpu":
            # TODO: Revise for async task handling to avoid blocking while waiting for results.
            bitstring_counts_batch: list[OrderedDict] = (
                program.braket.aquila.run_async(100).report().counts()
            )
            if (
                len(bitstring_counts_batch) != 1
            ):  # TODO: Double-check that counts list will always be length 1 here.
                raise ValueError("Expected a single batch of counts.")
            bitstring_counts = bitstring_counts_batch[0]
            return self.compute_rydberg_probs(self.atoms.L, bitstring_counts)

        raise ValueError(
            f"Backend {backend} is not supported. Supported backends are: {self.SUPPORTED_BACKENDS}"
        )
