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
Module for simulating the dynamics of a quantum reservoir.

"""

from dataclasses import dataclass, field
from typing import Any

from bloqade.atom_arrangement import AtomArrangement
from bloqade.ir import Waveform
from bloqade.builder import field

@dataclass
class DetuningLayer:
    """Class representing a detuning layer in a quantum reservoir."""

    def __init__(
        self,
        program: AtomArrangement,
        spatial_modulation: str
    ):

        if spatial_modulation == "uniform":
            self.detuning: field.uniform = program.detuning.uniform
        elif spatial_modulation == "scale":
            raise NotImplementedError(
            f"{self.__class__.__name__}.spatial_modulation == 'scale' not implemented\n"
        )
            # self.detuning: scale = program.detuning.scale
        elif spatial_modulation == "location":
            raise NotImplementedError(
            f"{self.__class__.__name__}.spatial_modulation == 'location' not implemented\n"
        )
            # self.detuning: location = program.detuning.location
        else:
            raise ValueError("Invalid spatial modulation type.")


    def apply_layer(self, program):
        return self.detuning.piecewise_linear(program.durations, program.amplitudes)
