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
from dataclasses import dataclass

import numpy as np

from bloqade.atom_arrangement import Square, Chain, Rectangular, Honeycomb, Triangular, Lieb, Kagome, AtomArrangement
from bloqade.builder.waveform import PiecewiseLinear

class GeometryOptions:  # pylint: disable=too-few-public-methods


    # pylint: disable-next=too-many-arguments
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

        self.atom_arrangement: AtomArrangement = atom_arrangement_shape_dictionary.get(atom_arrangement_shape)
        self.lattice_spacing: float = lattice_spacing

@dataclass
class AnalogEvolution:

    def __init__(
            self,
            rabi_amplitudes: list[float],
            durations: list[float],
            simulation: bool,
            geometric_configuration: GeometryOptions
            ):


        self.simulation = simulation
        self.amplitudes = rabi_amplitudes
        self.durations = durations


    def get_prob(counts, num_atoms):
        """Helper function for calculating the Rydberg probability averaged over all the shots"""
        prob = np.zeros(num_atoms)

        total_shots = 0 # Total number of shots in the counts
        for key, val in counts[0].items():
            prob += np.array([float(bit) for bit in [*key]]) * val
            total_shots += val

        prob /= total_shots
        return prob

    def _time_evolution(self, amp_waveform, num_atoms: int):
        """
        evolves the program over discrete list of time steps
        """

        program = (
                amp_waveform
                .detuning.uniform.piecewise_linear(self.durations, self.amplitudes)
            )

        if self.simulation:
            [emulation] = (program.bloqade.python().hamiltonian())
            emulation.evolve(times=self.durations)

            return emulation.hamiltonian.tocsr(time=self.durations[-1]).toarray()



        else:
            hardware_run_bitstrings = program.braket.aquila.run_async(100).report().counts()

            expected_statevector = self.get_prob(hardware_run_bitstrings, num_atoms)
            return expected_statevector

    def time_evolution(self, num_atoms: int):
        """
        evolves the program over discrete list of time steps
        """
        program_setup = self.geometric_configuration.atom_arrangement(
            lattice_spacing=self.geometric_configuration.lattice_spacing
            ).rydberg.rabi.amplitude.uniform.constant(15.0, 4.0)
        return self._time_evolution(program_setup, num_atoms)



