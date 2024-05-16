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
Module for integrating different quantum computing libraries with
the quantum reservoir.

"""

from abc import ABC, abstractmethod


class QuantumAdapter(ABC):
    """Base class for quantum library adapters."""

    @abstractmethod
    def initialize_reservoir(self):
        """Initialize the quantum reservoir with specific library settings."""


class PennylaneAdapter(QuantumAdapter):
    """Adapter for interfacing with Pennylane."""

    def initialize_reservoir(self):
        """Initialize the quantum reservoir using Pennylane."""
        raise NotImplementedError


class BloqadeAdapter(QuantumAdapter):
    """Adapter for interfacing with Bloqade."""

    def initialize_reservoir(self):
        """Initialize the quantum reservoir using Bloqade."""
        raise NotImplementedError
