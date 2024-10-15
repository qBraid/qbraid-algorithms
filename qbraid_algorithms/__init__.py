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
Python package containing quantum and hybrid quantum-classical algorithms that can
be used to carry out research and investigate how to solve problems in different
domains on simulators and near-term real quantum devices using shallow circuits.

.. currentmodule:: qbraid_algorithms

"""

from . import datasets, esn, qrc

try:
    # Injected in _version.py during the build process.
    from ._version import __version__  # type: ignore
except ImportError:
    __version__ = "dev"


__all__ = ["datasets", "esn", "qrc"]
