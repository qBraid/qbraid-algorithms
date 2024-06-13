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
Module for quantum time evolution using Krylov subspace methods.

"""
from dataclasses import dataclass
import numpy as np
from scipy.linalg import expm
from bloqade.emulate.ir.state_vector import StateVector, RydbergHamiltonian
from bloqade.factory import rydberg_h  # Import the rydberg_h function


# Placeholder for Krylov options with dummy attributes
class KrylovOptions:  # pylint: disable=too-few-public-methods
    """Class that describes options for a Krylov subspace method.

    Args:
        progress (bool): Whether to show progress during the evolution.
        progress_name (str): Name for the progress indicator.
        normalize_step (int): Frequency of normalization steps.
        normalize_finally (bool): Whether to normalize the quantum state at the end.
        tol (float): Tolerance for numerical operations.

    """

    # pylint: disable-next=too-many-arguments
    def __init__(
        self,
        progress: bool = False,
        progress_name: str = "emulating",
        normalize_step: int = 1,
        normalize_finally: bool = True,
        tol: float = 1e-7,
    ):
        self.progress = progress
        self.progress_name = progress_name
        self.normalize_step = normalize_step
        self.normalize_finally = normalize_finally
        self.tol = tol


@dataclass
class KrylovEvolution:
    reg: StateVector
    start_clock: float
    durations: list[float]
    atoms: list  # Add atoms attribute
    delta: float  # Add delta attribute
    omega: float  # Add omega attribute
    options: KrylovOptions

    def generate_krylov_basis(self, h, psi_0, m):
        n = len(psi_0)
        k = np.zeros((n, m), dtype=complex)
        k[:, 0] = psi_0 / np.linalg.norm(psi_0)
        for j in range(1, m):
            k[:, j] = h @ k[:, j - 1]
            for i in range(j):
                k[:, j] -= np.dot(k[:, i], k[:, j]) * k[:, i]
            k[:, j] /= np.linalg.norm(k[:, j])
        return k

    def gram_schmidt(self, v):
        q, _ = np.linalg.qr(v)
        return q

    def krylov_evolution(self, h, psi_0, t, m):
        k = self.generate_krylov_basis(h, psi_0, m)
        h_m = k.T.conj() @ h @ k
        exp_h_m = expm(-1j * h_m * t)
        psi_t = k @ exp_h_m @ k.T.conj() @ psi_0
        return psi_t

    def emulate_step(self, step: int, clock: float, duration: float) -> "KrylovEvolution":
        try:
            psi_0 = self.reg
            hamiltonian = rydberg_h(self.atoms, self.delta, self.omega)  # Use rydberg_h function
            evolved_state = self.krylov_evolution(
                hamiltonian.rydberg, psi_0, duration, len(self.durations)
            )
            self.reg = evolved_state
        except Exception as err:
            raise NotImplementedError("Emulation step failed") from err

    def normalize_register(self) -> None:
        if self.options.normalize_finally:
            norm = np.linalg.norm(self.reg)
            if norm > self.options.tol:
                self.reg /= norm
