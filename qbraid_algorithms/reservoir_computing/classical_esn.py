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
from dataclasses import dataclass, field

import torch

from .exceptions import ReservoirGenerationError


@dataclass
class EchoStateReservoir:  # pylint: disable=too-many-instance-attributes
    """Dataclass for a reservoir component of an Echo State Network."""

    input_size: int
    hidden_size: int
    sparsity: float = 0.9
    spectral_radius: float = 0.99
    a: float = 0.6
    leak: float = 1.0
    max_retries: int = 3
    w_in: torch.Tensor = field(init=False)
    w: torch.Tensor = field(init=False)
    x: torch.Tensor = field(init=False)

    def __post_init__(self):
        self.w_in = self._generate_w_in()
        self.w = self._generate_w(max_retries=self.max_retries)
        self.x = torch.zeros(self.hidden_size, 1)

    def _generate_w_in(self, mean: float = 0.0) -> torch.Tensor:
        """Generates and returns a random input weight matrix, w_in."""
        return torch.randn(self.hidden_size, self.input_size + 1).normal_(mean=mean, std=self.a)

    def _generate_w(self, mean: float = 0.0, max_retries: int = 3) -> torch.Tensor:
        """Generates a sparse internal weight matrix, w, with retries if necessary."""
        for attempt in range(max_retries + 1):
            w = torch.randn(self.hidden_size, self.hidden_size).normal_(
                mean=mean, std=self.spectral_radius
            )
            w = torch.where(torch.rand_like(w) > self.sparsity, w, torch.zeros_like(w))
            eigenvalues = torch.linalg.eigvals(w)  # pylint: disable=not-callable
            max_abs_eigenvalue = torch.max(torch.abs(eigenvalues)).item()
            if max_abs_eigenvalue != 0:
                w *= self.spectral_radius / max_abs_eigenvalue
                return w
            if attempt == max_retries:
                raise ReservoirGenerationError(
                    f"Failed to generate a valid weight matrix after {max_retries} retries; "
                    "max eigenvalue was zero."
                )
        return w

    def evolve(self, u: torch.Tensor) -> None:
        """
        Updates and returns the state representation x for a given input u.

        Args:
            u: Input vector.

        """
        temp_state = torch.tanh(
            torch.mm(self.w_in, torch.cat((torch.tensor([[1.0]]), u), 0)) + torch.mm(self.w, self.x)
        )
        new_state = (1 - self.leak) * self.x + self.leak * temp_state
        self.x = new_state


class EchoStateNetwork(torch.nn.Module):
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
        h_soft = self.softmax(h)  # Apply softmax
        return h_soft
