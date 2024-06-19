from bloqade import var, rydberg_h
from bloqade.atom_arrangement import Square
from scipy.optimize import newton_krylov
import numpy as np

class KrylovTimeEvolution:
    def __init__(self, lattice_size, lattice_spacing, max_rabi, max_detuning):
        self.lattice_size = lattice_size
        self.lattice_spacing = lattice_spacing
        self.max_rabi = max_rabi
        self.max_detuning = max_detuning

        # Define the variables explicitly
        self.max_rabi_var = var("max_rabi")
        self.max_detuning_var = var("max_detuning")

        # Initialize the atom arrangement
        self.atom_arrangement = Square(lattice_size, lattice_spacing=lattice_spacing)

        # Define the Rydberg Hamiltonian
        self.hamiltonian = self.define_hamiltonian()

    def define_hamiltonian(self):
        # Define the Hamiltonian using piecewise linear functions
        adiabatic_durations = [0.4, 3.2, 0.4]

        hamiltonian = (
            self.atom_arrangement.rydberg.rabi.amplitude.uniform.piecewise_linear(
                durations=adiabatic_durations, values=[0.0, self.max_rabi_var, self.max_rabi_var, 0.0]
            )
            .detuning.uniform.piecewise_linear(
                durations=adiabatic_durations,
                values=[
                    -self.max_detuning_var,
                    -self.max_detuning_var,
                    self.max_detuning_var,
                    self.max_detuning_var,
                ],
            )
            .assign(max_rabi=self.max_rabi, max_detuning=self.max_detuning)
        )

        # print(f"Hamiltonian: {hamiltonian}\n")

        return hamiltonian

    def krylov_time_evolution(self, initial_state, time_steps):
        # Initialize time index
        time_index = [0]

        # Define a function that represents the time evolution
        def time_evolution(state):
            time = time_steps[time_index[0]]
            time_index[0] += 1  # Update the time index for the next iteration
            return rydberg_h(state, self.hamiltonian, time)

        routine = time_evolution(initial_state).bloqade.python().hamiltonian
        print(f"{routine}\n")
        # Use newton_krylov to perform the time evolution
        final_state = newton_krylov(time_evolution, initial_state, method='lgmres', maxiter=100)

        return final_state

if __name__ == "__main__":
    krylov_evolution = KrylovTimeEvolution(lattice_size=3, lattice_spacing=5.0, max_rabi=15.8, max_detuning=16.33)

    # Example initial state (needs to be defined according to your problem)
    initial_state = np.zeros((krylov_evolution.lattice_size, krylov_evolution.lattice_size))

    # Define time steps
    time_steps = np.linspace(0, 1, 100)

    # Perform the Krylov time evolution
    final_state = krylov_evolution.krylov_time_evolution(initial_state, time_steps)

    print(final_state)

