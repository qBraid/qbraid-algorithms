from bloqade import start
from bloqade.atom_arrangement import Square
from bloqade import rydberg_h
from scipy.optimize import newton_krylov
import numpy as np

class KrylovTimeEvolution:
    def __init__(self, lattice_size, lattice_spacing, max_rabi, max_detuning):
        self.lattice_size = lattice_size
        self.lattice_spacing = lattice_spacing
        self.max_rabi = max_rabi
        self.max_detuning = max_detuning

        # Initialize the atom arrangement
        self.atom_arrangement = Square(lattice_size, lattice_spacing=lattice_spacing)

        # Define the Rydberg Hamiltonian
        self.hamiltonian = self.define_hamiltonian()

    def define_hamiltonian(self):
        adiabatic_durations = [0.4, 3.2, 0.4]

        program = (
            self.atom_arrangement
            .rydberg.rabi.amplitude.uniform.piecewise_linear(
                durations=adiabatic_durations, values=[0.0, self.max_rabi, self.max_rabi, 0.0]
            )
            .rydberg.detuning.uniform.piecewise_linear(
                durations=adiabatic_durations,
                values=[
                    -self.max_detuning,
                    -self.max_detuning,
                    self.max_detuning,
                    self.max_detuning,
                ],
            )
        )
        return program

    def krylov_time_evolution(self, initial_state, time_steps):
        time_index = [0]

        def time_evolution(state):
            current_time = time_steps[time_index[0]]
            time_index[0] += 1

            # Evaluate the Hamiltonian at the current time step
            program_instance = self.hamiltonian

            # Use the current state and time to get the next state
            return rydberg_h(
                atoms_positions=self.atom_arrangement,
                detuning=program_instance.rydberg.rabi.amplitude.uniform.piecewise_linear(durations=adiabatic_durations, values=[0.0, self.max_rabi, self.max_rabi, 0.0])
                durations=adiabatic_durations, values=[0.0, self.max_rabi, self.max_rabi, 0.0]
            ),
             amplitude=program_instance.rydberg.rabi.amplitude(current_time)
            )

        final_state = newton_krylov(time_evolution, initial_state, method='lgmres', maxiter=100)
        return final_state

if __name__ == "__main__":
    krylov_evolution = KrylovTimeEvolution(lattice_size=3, lattice_spacing=5.0, max_rabi=15.8, max_detuning=16.33)

    initial_state = np.zeros((krylov_evolution.lattice_size, krylov_evolution.lattice_size))
    time_steps = np.linspace(0, 1, 100)

    final_state = krylov_evolution.krylov_time_evolution(initial_state, time_steps)
    print(final_state)
