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

import numpy as np
from bloqade.emulate.ir.atom_type import AtomType
from bloqade.emulate.ir.emulator import Register
from bloqade.atom_arrangement import Chain, Square, Rectangular, Honeycomb, Triangular, Lieb, Kagome, AtomArrangement
from bloqade.ir import Waveform
from bloqade.builder.field import uniform, scale, location
from bloqade import rydberg_h

@dataclass
class DetuningLayer:
    """Class representing a detuning layer in a quantum reservoir."""

    def __init__(
        self,
        program: AtomArrangement,
        spatial_modulation: str
    ):
        if spatial_modulation == "uniform":
            self.detuning: uniform = program.detuning.uniform
        elif spatial_modulation == "scale":
            self.detuning: scale = program.detuning.scale
        elif spatial_modulation == "location":
            self.detuning: location = program.detuning.location
        else:
            raise ValueError("Invalid spatial modulation type.")


def apply_layer(self):
    return self.detuning
