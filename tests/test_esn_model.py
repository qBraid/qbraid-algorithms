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
Unit tests for the clasical Echo State Network (ESN) model.

"""
import pytest
import torch

from qbraid_algorithms.esn import EchoStateNetwork, EchoStateReservoir


@pytest.mark.parametrize("input_size,hidden_size,output_size", [(10, 20, 5)])
def test_echo_state_network_initialization(input_size, hidden_size, output_size):
    """Test the initialization of the EchoStateNetwork."""
    reservoir = EchoStateReservoir(input_size, hidden_size)
    esn = EchoStateNetwork(reservoir, output_size)

    assert esn.reservoir.input_size == input_size
    assert esn.fc.in_features == hidden_size
    assert esn.fc.out_features == output_size
    assert isinstance(esn.fc, torch.nn.Linear)
    assert isinstance(esn.softmax, torch.nn.Softmax)
    assert esn.fc.in_features == hidden_size
    assert esn.fc.out_features == output_size


@pytest.mark.parametrize("input_size,hidden_size,output_size", [(10, 20, 5)])
def test_echo_state_network_output_size(input_size, hidden_size, output_size):
    """Test that the output size matches the expected output dimensions."""
    reservoir = EchoStateReservoir(input_size, hidden_size)
    esn = EchoStateNetwork(reservoir, output_size)
    input_data = torch.randn(1, input_size)
    output = esn.forward(input_data)

    assert output.size() == (1, output_size)


@pytest.mark.parametrize("input_size,hidden_size,output_size", [(10, 20, 5)])
def test_echo_state_network_forward_pass(input_size, hidden_size, output_size):
    """Test the forward pass to ensure it processes inputs and produces outputs correctly."""
    reservoir = EchoStateReservoir(input_size, hidden_size)
    esn = EchoStateNetwork(reservoir, output_size)
    input_data = torch.randn(1, input_size)
    output = esn.forward(input_data)

    assert output.dim() == 2  # Ensure output is two-dimensional
    assert output.size(0) == 1
    assert output.size(1) == output_size
    assert torch.all(output >= 0) and torch.all(
        output <= 1
    ), "Output values should be probabilities, hence between 0 and 1."
