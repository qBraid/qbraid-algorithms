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
Module for classical reservoir computing with Echo State Networks (ESNs).

"""

import torch

from .reservoir import EchoStateReservoir


class EchoStateNetwork(torch.nn.Module):  # pylint: disable=too-few-public-methods
    """
    An Echo State Network module that combines a Reservoir with a fully connected output layer.

    Attributes:
        reservoir (Reservoir): The reservoir component of the ESN.
        fc (torch.nn.Linear): Linear layer to map reservoir states to output dimensions.
        softmax (torch.nn.Softmax): Softmax activation function for generating output probabilities.
    """

    def __init__(self, reservoir: EchoStateReservoir, output_size: int):
        """
        Initializes the Echo State Network with a reservoir and a linear output layer.

        Args:
            reservoir (EchoStateReservoir): Reservoir component of the ESN.
            output_size (int): Size of each output sample.
        """
        super().__init__()
        self.reservoir = reservoir
        self.fc = torch.nn.Linear(in_features=reservoir.hidden_size, out_features=output_size)
        self.softmax = torch.nn.Softmax(dim=-1)

    def forward(self, input_data: torch.Tensor) -> torch.Tensor:
        """
        Processes the input through the network and returns the output probabilities.

        Args:
            input_data: A tensor of input data.

        Returns:
            torch.Tensor: A tensor containing the softmax probabilities of the outputs.
        """
        u = input_data.flatten()  # Flatten data into a single vector
        u = u.unsqueeze(dim=0).t()  # Transpose to desired input shape for the reservoir

        self.reservoir.evolve(u)  # Pass through reservoir

        h = self.fc(self.reservoir.x.t())  # Pass transposed output x through the linear layer
        if len(h[0]) != 1:
            h = self.softmax(h)  # Apply softmax
        return h
