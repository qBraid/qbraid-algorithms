import pytest
from bloqade.emulate.ir.state_vector import StateVector
from qbraid_algorithms.qrc.krylov import KrylovEvolution, KrylovOptions

def test_krylov_evolution():
    atoms = [...]  # Define your atoms here
    delta = 1.0
    omega = 1.0
    reg = StateVector(...)  # Initialize your StateVector here
    options = KrylovOptions()
    durations = [0.1, 0.2, 0.3]

    evolution = KrylovEvolution(reg, 0.0, durations, atoms, delta, omega, options)
    evolution.emulate_step(0, 0.0, 0.1)

    assert evolution.reg is not None  # Add more assertions as needed

if __name__ == "__main__":
    pytest.main()
