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
Unit tests for the Reservoir data class used by the Echo State Network (ESN) model.

"""

import pytest
import torch

from qbraid_algorithms.esn import EchoStateReservoir, ReservoirGenerationError


@pytest.mark.parametrize("input_size,hidden_size", [(10, 100), (5, 80), (3, 150)])
def test_reservoir_initialization(input_size, hidden_size):
    """Test initialization of a Reservoir instance for different input and hidden sizes."""
    reservoir = EchoStateReservoir(input_size, hidden_size, sparsity=0.5)

    assert reservoir.input_size == input_size
    assert reservoir.hidden_size == hidden_size
    assert reservoir.x.size() == (hidden_size, 1)
    assert torch.all(reservoir.x == 0)


def test_input_weight_matrix_dimensions():
    """Test setting the dimensions of the input weight matrix 'w_in'."""
    reservoir = EchoStateReservoir(input_size=10, hidden_size=100, sparsity=0.5)
    assert reservoir.w_in.size() == (100, 11)  # Includes bias term


def test_reservoir_matrix_meets_target_sparsity():
    """Test whether the internal weight matrix 'w' of a Reservoir instance meets
    the target sparsity within an acceptable margin of error."""
    target_sparsity = 0.8
    reservoir = EchoStateReservoir(input_size=10, hidden_size=100, sparsity=target_sparsity)
    total_elements = reservoir.w.numel()
    non_zero_elements = reservoir.w.nonzero().size(0)
    zero_elements = total_elements - non_zero_elements
    actual_sparsity = zero_elements / total_elements

    tolerance = 0.015
    expected_sparsity_lower_bound = target_sparsity - (target_sparsity * tolerance)
    expected_sparsity_upper_bound = target_sparsity + (target_sparsity * tolerance)

    assert expected_sparsity_lower_bound <= actual_sparsity <= expected_sparsity_upper_bound, (
        f"Actual sparsity {actual_sparsity} outside of expected range "
        f"[{expected_sparsity_lower_bound}, {expected_sparsity_upper_bound}]"
    )


def test_raising_error_on_invalid_weight_generation():
    """Test that an error is raised during reservoir generation
    when the maximum eigenvalue of the weight matrix is zero."""
    with pytest.raises(ReservoirGenerationError):
        EchoStateReservoir(input_size=3, hidden_size=5, sparsity=1.0, max_retries=0)


def test_spectral_radius():
    """Test setting the spectral radius of the internal weight matrix."""
    reservoir = EchoStateReservoir(
        input_size=10, hidden_size=100, sparsity=0.5, spectral_radius=0.95
    )
    eigenvalues = torch.linalg.eigvals(reservoir.w)  # pylint: disable=not-callable
    max_eigenvalue = torch.max(torch.abs(eigenvalues)).item()
    assert pytest.approx(max_eigenvalue, 0.01) == 0.95


def test_evolve_state():
    """Test evolving the state representation x for a given input u."""
    reservoir = EchoStateReservoir(input_size=3, hidden_size=5, sparsity=0.5)
    initial_state = torch.clone(reservoir.x)
    u = torch.randn(3, 1)
    reservoir.evolve(u)
    assert not torch.all(torch.eq(reservoir.x, initial_state))


def test_leaking_rate_effect():
    """Tests the reservoir's responsiveness by verifying that a low leaking rate limits state
    changes to less than the input's norm, indicating minimal integration of new information.
    """
    reservoir = EchoStateReservoir(input_size=3, hidden_size=5, sparsity=0.5, leak=0.1)
    initial_state = torch.clone(reservoir.x)
    u = torch.randn(3, 1)
    reservoir.evolve(u)
    assert torch.norm(reservoir.x - initial_state) < torch.norm(u)
