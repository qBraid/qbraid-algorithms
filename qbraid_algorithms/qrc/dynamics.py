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

from dataclasses import dataclass, field
from typing import Any

import numpy as np
from bloqade.emulate.ir.atom_type import AtomType
from bloqade.emulate.ir.emulator import Register
from bloqade.atom_arrangement import Chain

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
    
    Note: For now adding a simple lattice type, later we can add different options.
    
    Args:
        lattice_type (Any): Type of the lattice.
        dimension (int): Number of principal components.
        scale (float): Scale factor for lattice spacing.

    Returns:
        Any: Positions of atoms.

    TODO: Implement actual site generation based on lattice type.
    """
    return Chain(dimension, lattice_spacing=scale)

def apply_layer(layer: DetuningLayer, x: np.ndarray) -> np.ndarray:
    """
    Simulate quantum evolution and record output for a given set of PCA values (x).

    Note: Frequency omega is not a input for rydberg_h python function, instead amplitude is there.
    For detuning we use x.
    
    Args:
        layer (DetuningLayer): Configuration and quantum state of the layer.
        x (np.ndarray): Vector or matrix of real numbers representing PCA values for each image.

    Returns:
        np.ndarray: Output values from the simulation.

    TODO: Implement the actual simulation using suitable quantum simulation libraries.
    """
    # using omega as amplitude for now, since other things don't make sense. 
    #detuning has to be of form wave so need to get back to it
    hamiltonian = rydberg_h(
          layer.atoms, detuning = x, amplitude = layer.omega,
      )
    
    layer.t_start = 0
    layer.t_end = 5
    layer.t_step = 0.1
    steps = (t_end - t_start)/t_step + 1
    times = []
    for i in range(int(steps)):
        times.append(t_start + i*t_step)
    
    # something like should be the chronological order
    hamiltonian.evolve(times=times)
