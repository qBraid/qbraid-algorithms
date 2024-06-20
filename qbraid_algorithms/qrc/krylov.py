# qbraid_algorithms/qrc/krylov_foo_2.py

from bloqade import start, rydberg_h
from bloqade.atom_arrangement import Square
from scipy.optimize import newton_krylov
import numpy as np
from qbraid_algorithms.qrc.dynamics import DetuningLayer

class KrylovTimeEvolution:
    def __init__(self, lattice_size, lattice_spacing, max_rabi, max_detuning, step, atom_arrangement):
        self.lattice_size = lattice_size
        self.lattice_spacing = lattice_spacing
        self.max_rabi = max_rabi
        self.max_detuning = max_detuning
        self.step = step

        # Initialize the atom arrangement
        self.atom_arrangement = atom_arrangement

        # Initialize the detuning layer
        self.detuning_layer = DetuningLayer(
            atoms=[],  # Placeholder for atom positions
            readouts=[],  # Placeholder for readout observables
            omega=max_rabi,
            t_start=0,
            t_end=step * 3,  # Example duration
            step=step
        )

        # Define the Rydberg Hamiltonian
        self.program = self.detuning_layer.setup_program(self.atom_arrangement)

    def krylov_time_evolution(self, initial_state, time_steps):
        time_index = [0]

        def time_evolution(state):
            current_time = time_steps[time_index[0]]
            time_index[0] += 1

            # Evaluate the Hamiltonian at the current time step
            program_instance = self.program

            # Use the current state and time to get the next state
            # Currently hardcoded to run on local python bloqade emulator
            return rydberg_h(
                atoms_positions=self.atom_arrangement,
                detuning=program_instance.rydberg.detuning,
                amplitude=program_instance.rydberg.rabi.amplitude(current_time)
            ).bloqade.python().hamiltonian(state)

        final_state = newton_krylov(time_evolution, initial_state, method='lgmres', maxiter=100)
        return final_state

if __name__ == "__main__":
    krylov_evolution = KrylovTimeEvolution(
        lattice_size=3,
        lattice_spacing=5.0,
        max_rabi=15.8,
        max_detuning=16.33,
        step=0.4,  # Example step size
        atom_arrangement="Square"
    )

    initial_state = np.zeros((krylov_evolution.lattice_size, krylov_evolution.lattice_size))
    time_steps = np.linspace(0, 1, 100)

    final_state = krylov_evolution.krylov_time_evolution(initial_state, time_steps)
    print(final_state)
