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
Module for simulating the dynamics of a quantum reservoir.

"""

import math
from dataclasses import dataclass, field
from typing import Any

import numpy as np
from bloqade.emulate.ir.atom_type import AtomType
from bloqade.emulate.ir.emulator import Register
from bloqade.emulate.ir.state_vector import RydbergHamiltonian

from .krylov import KrylovEvolution


@dataclass
class DetuningLayer:
    """Class representing a detuning layer in a quantum reservoir."""

    atoms: list[AtomType]  # Atom positions
    readouts: list[Any]  # Readout observables
    omega: float  # Rabi frequency
    t_start: float  # Evolution starting time
    t_end: float  # Evolution ending time
    step: float  # Readout time step
    reg: Register = field(
        default_factory=lambda *args, **kwargs: Register(*args, **kwargs)
    )  # Quantum state storage


def generate_sites(lattice_type, dimension, scale):
    """
    Generate positions for atoms on a specified lattice type with a given scale.

    Args:
        lattice_type (Any): Type of the lattice.
        dimension (int): Number of principal components.
        scale (float): Scale factor for lattice spacing.

    Returns:
        Any: Positions of atoms.

    TODO: Implement actual site generation based on lattice type.
    """
    raise NotImplementedError


def rydberg_h(atoms: list[AtomType], delta: float, omega: float) -> RydbergHamiltonian:
    """
    Generate the Hamiltonian for a Rydberg atom system.

    Args:
        atoms (list[AtomType]): Atom positions.
        omega (float): Rabi frequency.

    Returns:
        RydbergHamiltonian: Hamiltonian matrix.
    """
    raise NotImplementedError


def set_zero_state(reg: Register):
    """
    Set the quantum state to the zero state.

    Args:
        reg (Register): Quantum state storage.
    """
    raise NotImplementedError


def apply_layer(layer: DetuningLayer, x: np.ndarray) -> np.ndarray:
    """
    Simulate quantum evolution and record output for a given set of PCA values (x).

    Args:
        layer (DetuningLayer): Configuration and quantum state of the layer.
        x (np.ndarray): Vector or matrix of real numbers representing PCA values for each image.

    Returns:
        np.ndarray: Output values from the simulation.

    TODO: Implement the actual simulation using suitable quantum simulation libraries.
    """
    h = rydberg_h(layer.atoms, x, layer.omega)

    reg = layer.reg
    reg = set_zero_state(reg)

    t_start = layer.t_start
    t_end = layer.t_end
    t_step = layer.step
    start_clock = NotImplemented

    # initialize output vector
    steps = math.floor((t_end - t_start) / t_step)
    out = np.zeros(steps * len(layer.readouts))

    # Numerically simulate the quantum evolution with Krylov methods and store the readouts
    i = 1
    prob = KrylovEvolution(
        reg, start_clock=start_clock, durations=[t_step] * steps, hamiltonian=h, options=None
    )
    for i in range(steps):
        # ignore first time step, this is just the initial state
        if i == 0:
            continue

        # TODO: Implement the emulation step function.
        # NOTE: The following lines are placehoders. They are not correct, and should be replaced.
        prob.emulate_step(i, t_start + i * t_step, t_step)
        for j, readout in enumerate(layer.readouts):
            out[i * len(layer.readouts) + j] = readout(prob)

    return out
