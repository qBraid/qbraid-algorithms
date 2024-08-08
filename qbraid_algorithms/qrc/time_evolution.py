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
from collections import OrderedDict
from decimal import Decimal

import numpy as np
from bloqade.atom_arrangement import Chain
from bloqade.builder.field import Detuning
from dataclasses import dataclass, field
from typing import Any
from bloqade.emulate.ir.atom_type import AtomType
from bloqade.emulate.ir.emulator import Register

from bloqade import (
    waveform,
    rydberg_h,
    piecewise_linear,
    piecewise_constant,
    constant,
    linear,
    var,
    cast,
    start,
    get_capabilities,
)



class AnalogProgramEvolver:
    """Class for evolving program over discrete list of time steps.
       Changed into requiring dynamics.py for compatability and equivalency to julia code
    """

    SUPPORTED_BACKENDS = ["emulator", "qpu"]

    

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

    def evolve(self, layer: DetuningLayer, x: numpy.array backend: str) -> np.ndarray:
        """Evolves program over discrete list of time steps"""

        # pre-processing
        local_detuning_wf = piecewise_linear(layer.durations.tolist(), values = x)

        # this I have to check
        detuning: Detuning = self.atoms.rydberg.rabi.amplitude

        amp_waveform = detuning.uniform.constant(max(layer.amplitudes), sum(layer.durations))

        if backend == "emulator":
            if emu_option == None:
                [emulation] = program.bloqade.python().hamiltonian()
                emulation.evolve(times=self.time_steps)
                return emulation.hamiltonian.tocsr(time=self.time_steps[-1]).toarray()

            # the only problem is getting that program layout...have to ask Trenten
            if emu_option == "rydberg_h":
                emulation = rydberg_h(
                  layer.atoms, detuning = local_detuning_wf, amplitude = amp_waveform,
                  )
                # something like should be the chronological order
                output_evolution = emulation.evolve(times=layer.durations)
                return output_evolution
                # return emulation.hamiltonian.tocsr(time=layer.durations[-1]).toarray()

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
