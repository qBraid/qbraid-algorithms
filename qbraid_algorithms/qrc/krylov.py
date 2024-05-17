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

from bloqade.emulate.ir.emulator import Register
from bloqade.emulate.ir.state_vector import RydbergHamiltonian


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
