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
Module for quantum time evolution using Magnus expansion.

"""

from scipy.linalg import expm


class MagnusExpansion:
    """
    Class that describes a time evolution using Magnus expansion.

    """

    def __init__(self, H):
        self.H = H

    def commutator(self, A, B):
        """Compute the commutator of two matrices."""
        return A @ B - B @ A

    def compute_magnus_terms(self, t):
        """Compute the terms of the Magnus expansion."""
        H_t = self.H * t
        Ω1 = H_t

        # Second-order term
        comm_H1_H2 = self.commutator(self.H, self.H)
        Ω2 = 0.5 * (comm_H1_H2 * t**2)

        # Third-order term
        comm_H1_comm_H2_H3 = self.commutator(self.H, self.commutator(self.H, self.H))
        comm_H3_comm_H2_H1 = self.commutator(self.commutator(self.H, self.H), self.H)
        Ω3 = (1 / 6) * (comm_H1_comm_H2_H3 + comm_H3_comm_H2_H1) * t**3

        # Fourth-order term
        comm_H1_comm_H2_comm_H3_H4 = self.commutator(
            self.H, self.commutator(self.H, self.commutator(self.H, self.H))
        )
        comm_H4_comm_H3_comm_H2_H1 = self.commutator(
            self.commutator(self.commutator(self.H, self.H), self.H), self.H
        )
        Ω4 = (1 / 24) * (comm_H1_comm_H2_comm_H3_H4 + comm_H4_comm_H3_comm_H2_H1) * t**4

        return Ω1 + Ω2 + Ω3 + Ω4

    def time_evolution_operator(self, t):
        """Compute the time evolution operator using Magnus expansion."""
        Ω = self.compute_magnus_terms(t)
        return expm(Ω)

    def simulate_dynamics(self, psi0, t_final, dt):
        """Simulate the dynamics of the system."""
        psi = psi0
        t = 0
        while t < t_final:
            U = self.time_evolution_operator(dt)
            psi = U @ psi
            t += dt
        return psi
