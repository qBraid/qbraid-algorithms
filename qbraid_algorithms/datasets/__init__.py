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
Dataset generation for reservoir computing tasks.

Functions
----------

.. autosummary::
    :toctree: ../stubs/

    create_sequences
    create_time_series_data
    load_mnist_data


"""

from .mnist import load_mnist_data
from .sequences import create_sequences, create_time_series_data

__all__ = ["create_sequences", "create_time_series_data", "load_mnist_data"]
