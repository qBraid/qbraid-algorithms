# Copyright (C) 2024 qBraid
#
# This file is part of the qBraid-SDK
#
# The qBraid-SDK is free software released under the GNU General Public License v3
# or later. You can redistribute and/or modify it under the terms of the GPL v3.
# See the LICENSE file in the project root or <https://www.gnu.org/licenses/gpl-3.0.html>.
#
# THERE IS NO WARRANTY for the qBraid-SDK, as per Section 15 of the GPL v3.

# pylint: disable=redefined-outer-name

"""
Unit tests for Quantum Reservoir Computing (QRC) dynamics modules.

"""
from unittest.mock import Mock

import numpy as np
import pytest
from bloqade.emulate.ir.atom_type import AtomType
from bloqade.emulate.ir.emulator import Register
from bloqade.emulate.ir.space import Space, SpaceType
from bloqade.emulate.ir.state_vector import StateVector
from numpy.typing import NDArray

from qbraid_algorithms.qrc.time_evolution import AnalogEvolution, EvolveOptions
from qbraid_algorithms.qrc.magnus import MagnusExpansion


@pytest.fixture
def program_register() -> Register:
    """Create a program register."""
    return Mock()


@pytest.fixture
def atom_type() -> AtomType:
    """Create an atom type."""
    return Mock()


@pytest.fixture
def configurations() -> NDArray:
    """Create configurations."""
    return Mock()


@pytest.fixture
def space_type() -> SpaceType:
    """Create a space type."""
    return Mock()


@pytest.fixture
def space(program_register, atom_type, configurations, space_type) -> Space:
    """Create a space object."""
    return Space(
        space_type=space_type,
        atom_type=atom_type,
        program_register=program_register,
        configurations=configurations,
    )


@pytest.mark.skip(reason="Not implemented yet")
def test_rbh(space):
    """Test the Rydberg Blockade Hamiltonian (RBH)"""
    initial_state = np.array([1, 0, 0, 0], dtype=complex)

    # Create a KrylovEvolution instance
    krylov_options = EvolveOptions()
    krylov_evolution = AnalogEvolution(
        reg=StateVector(data=initial_state, space=space),
        start_clock=0.0,
        durations=[0.1, 0.2, 0.3],
        hamiltonian=None,  # This will be initialized in __post_init__
        options=krylov_options,
    )

    # Simulate the evolution (example step)
    krylov_evolution.emulate_step(step=0, clock=0.0, duration=0.1)

    final_state = np.array([], dtype=complex)  # dummy value
    expected_value = StateVector(data=final_state, space=space)

    assert krylov_evolution.reg == expected_value


@pytest.mark.skip(reason="Not completed yet")
def test_simulate_dynamics():
    """Test the simulation of quantum dynamics using Magnus expansion."""
    # Define a simple Hamiltonian and initial state
    h = np.array([[0, 1], [1, 0]], dtype=complex)  # Simple Hamiltonian
    psi0 = np.array([1, 0], dtype=complex)  # Initial state
    t_final = 1.0
    dt = 0.01

    # Create an instance of MagnusExpansion
    magnus = MagnusExpansion(h)

    # Simulate the dynamics
    final_state = magnus.simulate_dynamics(psi0, t_final, dt)

    # Add assertions to check the final state
    # For example:
    expected_final_state = np.array([0.54030231 + 0.84147098j, 0.00000000 + 0.0j])
    np.testing.assert_allclose(final_state, expected_final_state, rtol=1e-5)
