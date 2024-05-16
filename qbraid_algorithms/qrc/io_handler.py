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
Module for input/output handling in the quantum reservoir computing framework.

"""


class InputHandler:
    """Handle input data conversion for quantum processing."""

    def convert_input(self, data):
        """Convert classical data into a format suitable for quantum processing.

        Args:
            data (Any): The data to be converted.

        Returns:
            Any: The data converted into a quantum-compatible format.
        """
        return data


class OutputHandler:
    """Process outputs from the quantum reservoir."""

    def process_output(self, output):
        """Process the output data from the quantum reservoir.

        Args:
            output (Any): The output data to process.

        Returns:
            Any: The processed output data.
        """
        return output
