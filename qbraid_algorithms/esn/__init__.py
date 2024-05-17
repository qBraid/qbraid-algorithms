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
Module providing classical Echo State Network (ESN) models.

ESNs are a type of classical reservoir computing system where a large, random,
fixed reservoir of neurons processes temporal (or other) data, with training only
applied to the readout weights that map the reservoir's state to the desired output.

Classes
---------

.. autosummary::
    :toctree: ../stubs/

    EchoStateNetwork
    EchoStateReservoir


Exceptions
------------

.. autosummary::
    :toctree: ../stubs/

    ReservoirGenerationError

"""

from .exceptions import ReservoirGenerationError
from .model import EchoStateNetwork
from .reservoir import EchoStateReservoir

__all__ = ["EchoStateNetwork", "EchoStateReservoir", "ReservoirGenerationError"]
