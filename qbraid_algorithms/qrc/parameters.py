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
Module for handling tunable parameters of the quantum reservoir.

"""

from dataclasses import dataclass, field


@dataclass
class ReservoirParameters:
    """A class to store and manage reservoir parameters.

    Attributes:
        size (int): The size of the reservoir.
        decay_rates (List[float]): Decay rates of the reservoir elements.
        coupling_constants (List[float]): Coupling constants between reservoir elements.
    """

    size: int
    decay_rates: list[float] = field(default_factory=list)
    coupling_constants: list[float] = field(default_factory=list)
