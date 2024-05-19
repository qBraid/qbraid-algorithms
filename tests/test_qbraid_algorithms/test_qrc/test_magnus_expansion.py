import numpy as np
from qbraid_algorithms import qrc

def test_simulate_dynamics():
    # Define a simple Hamiltonian and initial state
    H = np.array([[0, 1], [1, 0]], dtype=complex)  # Simple Hamiltonian
    psi0 = np.array([1, 0], dtype=complex)        # Initial state
    t_final = 1.0
    dt = 0.01

    # Create an instance of MagnusExpansion
    magnus = qrc.magnus_expansion.MagnusExpansion(H)

    # Simulate the dynamics
    final_state = magnus.simulate_dynamics(psi0, t_final, dt)

    # Add assertions to check the final state
    # For example:
    expected_final_state = np.array([0.54030231+0.84147098j, 0.00000000+0.j])
    np.testing.assert_allclose(final_state, expected_final_state, rtol=1e-5)
