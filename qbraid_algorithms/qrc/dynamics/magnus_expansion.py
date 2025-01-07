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

    def __init__(self, h):
        self.h = h

    def commutator(self, a, b):
        """Compute the commutator of two matrices."""
        return a @ b - b @ a

    def compute_magnus_terms(self, t):
        """Compute the terms of the Magnus expansion."""
        h_t = self.h * t
        omega_1 = h_t

        # Second-order term
        comm_h1_h2 = self.commutator(self.h, self.h)
        omega_2 = 0.5 * (comm_h1_h2 * t**2)

        # Third-order term
        comm_h1_comm_h2_h3 = self.commutator(self.h, self.commutator(self.h, self.h))
        comm_h3_comm_h2_h1 = self.commutator(self.commutator(self.h, self.h), self.h)
        omega_3 = (1 / 6) * (comm_h1_comm_h2_h3 + comm_h3_comm_h2_h1) * t**3

        # Fourth-order term
        comm_h1_comm_h2_comm_h3_h4 = self.commutator(
            self.h, self.commutator(self.h, self.commutator(self.h, self.h))
        )
        comm_h4_comm_h3_comm_h2_h1 = self.commutator(
            self.commutator(self.commutator(self.h, self.h), self.h), self.h
        )
        omega_4 = (1 / 24) * (comm_h1_comm_h2_comm_h3_h4 + comm_h4_comm_h3_comm_h2_h1) * t**4

        return omega_1 + omega_2 + omega_3 + omega_4

    def time_evolution_operator(self, t):
        """Compute the time evolution operator using Magnus expansion."""
        omega = self.compute_magnus_terms(t)
        return expm(omega)

    def simulate_dynamics(self, psi0, t_final, dt):
        """Simulate the dynamics of the system."""
        psi = psi0
        t = 0
        while t < t_final:
            u = self.time_evolution_operator(dt)
            psi = u @ psi
            t += dt
        return psi
