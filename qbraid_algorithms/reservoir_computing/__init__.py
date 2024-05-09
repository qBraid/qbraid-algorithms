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
Reservoir computing algorithms are a subset of recurrent neural networks (RNNs) that utilize
a fixed, randomly connected network known as the 'reservoir' to process temporal data. Unlike
traditional RNNs, reservoir computing models uniquely train only the output weights of the network.
This characteristic makes them particularly efficient as dynamic feature extractors.

Echo State Networks
---------------------

Type of classical reservoir computing system where a large, random, fixed reservoir of
neurons processes temporal (or other) data, with training only applied to the readout
weights that map the reservoir's state to the desired output.

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
from .classical_esn import EchoStateNetwork, EchoStateReservoir
from .exceptions import ReservoirGenerationError

__all__ = ["EchoStateNetwork", "EchoStateReservoir", "ReservoirGenerationError"]
