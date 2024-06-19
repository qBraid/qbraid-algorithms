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
from typing import Any
import numpy as np
from scipy.optimize import newton_krylov
from bloqade import rydberg_h
from bloqade.emulate.ir.emulator import Register
from bloqade.emulate.ir.state_vector import RydbergHamiltonian
from bloqade.atom_arrangement import Square


# Placeholder for Krylov options with dummy attributes
class KrylovOptions:
    """Class that describes options for a Krylov subspace method.

    Args:
        progress (bool): Whether to show progress during the evolution.
        progress_name (str): Name for the progress indicator.
        normalize_step (int): Frequency of normalization steps.
        normalize_finally (bool): Whether to normalize the quantum state at the end.
        tol (float): Tolerance for numerical operations.

    """

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
    """Class that describes a time evolution using Krylov subspace methods.

    Args:
        reg (Register): Quantum register for the evolution.
        start_clock (float): Start time of the evolution.
        durations (list[float]): Durations of each time step.
        hamiltonian (RydbergHamiltonian): Hamiltonian for the evolution.
        options (KrylovOptions): Options for the evolution process.
    """

    reg: Register
    start_clock: float
    durations: list[float]
    hamiltonian: RydbergHamiltonian
    options: KrylovOptions
    lattice_size: int
    lattice_spacing: float
    max_rabi: float
    max_detuning: float
    atom_arrangement: Any = None

    def __post_init__(self):
        self.atom_arrangement = Square(self.lattice_size, lattice_spacing=self.lattice_spacing)
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
                atoms_positions=self.atom_arrangement.positions,
                detuning=program_instance.rydberg.detuning(current_time),
                amplitude=program_instance.rydberg.rabi.amplitude(current_time)
            )

        final_state = newton_krylov(time_evolution, initial_state, method='lgmres', maxiter=100)
        return final_state

    def emulate_step(self, step: int, clock: float, duration: float) -> "KrylovEvolution":
        """
        Simulate a single time step of quantum evolution using the Krylov subspace method.

        Args:
            step: Current step index.
            clock: Current time.
            duration: Duration of the current time step.

        Returns:
            Self with the quantum state updated.

        TODO: Implement the emulation step function.
        """
        raise NotImplementedError

    def normalize_register(self):
        """
        Normalize the quantum register if specified in options.

        TODO: Implement the normalization logic.
        """
        raise NotImplementedError


if __name__ == "__main__":
    krylov_evolution = KrylovEvolution(
        reg=Register(),
        start_clock=0.0,
        durations=[0.4, 3.2, 0.4],
        hamiltonian=RydbergHamiltonian(),
        options=KrylovOptions(),
        lattice_size=3,
        lattice_spacing=5.0,
        max_rabi=15.8,
        max_detuning=16.33
    )

    initial_state = np.zeros((krylov_evolution.lattice_size, krylov_evolution.lattice_size))
    time_steps = np.linspace(0, 1, 100)

    final_state = krylov_evolution.krylov_time_evolution(initial_state, time_steps)
    print(final_state)
