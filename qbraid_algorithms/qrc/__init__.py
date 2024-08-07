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
Module providing Quantum Reservoir Computing (QRC) models.

Classes
---------

.. autosummary::
    :toctree: ../stubs/

    QRCModel
    MagnusExpansion
    DetuningLayer
    MagnusExpansion
    AnalogProgramEvolver
    PCA

Functions
----------

.. autosummary::
    :toctree: ../stubs/

    one_hot_encoding

"""

from .encoding import PCA, one_hot_encoding
from .magnus_expansion import MagnusExpansion
from .qrc_model import DetuningLayer, QRCModel
from .time_evolution import AnalogProgramEvolver

__all__ = [
    "QRCModel",
    "MagnusExpansion",
    "DetuningLayer",
    "AnalogProgramEvolver",
    "PCA",
    "one_hot_encoding",
]
