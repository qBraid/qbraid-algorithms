# krylov.py
from dataclasses import dataclass
from bloqade.emulate.ir.emulator import Register
from bloqade.emulate.ir.state_vector import RydbergHamiltonian
from bloqade.atom_arrangement import Square
from scipy.linalg import expm
import numpy as np

class KrylovOptions:
    """Class that describes options for a Krylov subspace method."""
    def __init__(self, progress=False, progress_name="emulating", normalize_step=1, normalize_finally=True, tol=1e-7):
        self.progress = progress
        self.progress_name = progress_name
        self.normalize_step = normalize_step
        self.normalize_finally = normalize_finally
        self.tol = tol

@dataclass
class KrylovEvolution:
    """Class that describes a time evolution using Krylov subspace methods."""
    reg: Register
    start_clock: float
    durations: list[float]
    hamiltonian: RydbergHamiltonian
    options: KrylovOptions

    def generate_krylov_basis(self, H, psi0, m):
        """Generates the first m Krylov basis vectors."""
        n = len(psi0)
        K = np.zeros((n, m), dtype=complex)
        K[:, 0] = psi0 / np.linalg.norm(psi0)
        for j in range(1, m):
            K[:, j] = H @ K[:, j-1]
            for k in range(j):
                K[:, j] -= np.dot(K[:, k], K[:, j]) * K[:, k]
            K[:, j] /= np.linalg.norm(K[:, j])
        return K

    def gram_schmidt(self, V):
        """Orthonormalizes the vectors using the Gram-Schmidt process."""
        Q, R = np.linalg.qr(V)
        return Q

    def krylov_evolution(self, psi0, t, m):
        """Projects the Hamiltonian onto the Krylov subspace and computes the time evolution."""
        H = self.hamiltonian.rydberg  # Access the correct attribute
        K = self.generate_krylov_basis(H, psi0, m)
        H_m = K.T.conj() @ H @ K
        exp_Hm = expm(-1j * H_m * t)
        psi_t = K @ exp_Hm @ K.T.conj() @ psi0
        return psi_t

    def emulate_step(self, step, clock, duration):
        """Simulate a single time step of quantum evolution using the Krylov subspace method."""
        try:
            psi0 = self.reg.state_vector
            evolved_state = self.krylov_evolution(psi0, duration, len(self.durations))
            self.reg.state_vector = evolved_state
        except Exception as e:
            raise NotImplementedError(f"Emulation step failed: {e}")

    def normalize_register(self):
        """Normalize the quantum register if specified in options."""
        if self.options.normalize_finally:
            norm = np.linalg.norm(self.reg.state_vector)
            if norm > self.options.tol:
                self.reg.state_vector /= norm

# Usage Example
# Define the initial state
initial_state = np.array([1, 0, 0, 0], dtype=complex)

# Create a KrylovEvolution instance
krylov_options = KrylovOptions()
krylov_evolution = KrylovEvolution(
    reg=Register(initial_state),
    start_clock=0.0,
    durations=[0.1, 0.2, 0.3],
    hamiltonian=None,  # This will be initialized in __post_init__
    options=krylov_options
)

# Simulate the evolution (example step)
krylov_evolution.emulate_step(step=0, clock=0.0, duration=0.1)
