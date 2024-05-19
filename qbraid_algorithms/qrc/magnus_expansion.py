from scipy.linalg import expm

class MagnusExpansion:
    def __init__(self, H):
        self.H = H

    def commutator(self, A, B):
        return A @ B - B @ A

    def compute_magnus_terms(self, t):
        H_t = self.H * t
        Ω1 = H_t

        # Second-order term
        comm_H1_H2 = self.commutator(self.H, self.H)
        Ω2 = 0.5 * (comm_H1_H2 * t**2)

        # Third-order term
        comm_H1_comm_H2_H3 = self.commutator(self.H, self.commutator(self.H, self.H))
        comm_H3_comm_H2_H1 = self.commutator(self.commutator(self.H, self.H), self.H)
        Ω3 = (1/6) * (comm_H1_comm_H2_H3 + comm_H3_comm_H2_H1) * t**3

        # Fourth-order term
        comm_H1_comm_H2_comm_H3_H4 = self.commutator(self.H, self.commutator(self.H, self.commutator(self.H, self.H)))
        comm_H4_comm_H3_comm_H2_H1 = self.commutator(self.commutator(self.commutator(self.H, self.H), self.H), self.H)
        Ω4 = (1/24) * (comm_H1_comm_H2_comm_H3_H4 + comm_H4_comm_H3_comm_H2_H1) * t**4

        return Ω1 + Ω2 + Ω3 + Ω4

    def time_evolution_operator(self, t):
        Ω = self.compute_magnus_terms(t)
        return expm(Ω)

    def simulate_dynamics(self, psi0, t_final, dt):
        psi = psi0
        t = 0
        while t < t_final:
            U = self.time_evolution_operator(dt)
            psi = U @ psi
            t += dt
        return psi
