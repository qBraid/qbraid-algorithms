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

from bloqade import (
    waveform,
    rydberg_h,
    piecewise_linear,
    piecewise_constant,
    constant,
    linear,
    var,
    cast,
    start,
    get_capabilities,
)

@dataclass
class DetuningLayer:
    """Class representing a detuning layer in a quantum reservoir."""
    def __init__(
        self,
    atoms: list[AtomType],  # Atom positions
    readouts: list[Any],  # Readout observables
    omega: float,  # Rabi frequency
    t_start: float,  # Evolution starting time
    t_end: float,  # Evolution ending time
    step: float,  # Readout time step
    reg: Register = field(
        default_factory=lambda *args, **kwargs: Register(*args, **kwargs)
    )  # Quantum state storage
    ):
        self.atoms = atoms
        self.readouts = readouts
        self.amplitudes = omega
        self.t_start = t_start
        self.t_end = t_end
        self.t_step = t_step
        steps = (t_end - t_start)/t_step + 1
        
        durations = []
        for i in range(int(steps)):
            durations.append(t_start + i * t_step)
            
        self.durations = durations
        self.time_steps = self._get_time_steps(durations)


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

def create_detuning_format()

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
    #conversion of detuning layer
    # something like this should be provided 
    # x= x_test_pca[:, 1:num_examples].reshape(x_test_pca[:, 1:num_examples].size).tolist()

    local_detuning_wf = piecewise_linear(self.durations.tolist(), values = x)

    # this have to check
    detuning: Detuning = self.atoms.rydberg.rabi.amplitude
    amp_waveform = detuning.uniform.constant(max(self.amplitudes), sum(self.durations))
    
    hamiltonian = rydberg_h(
          layer.atoms, detuning = local_detuning_wf, amplitude = amp_waveform,
      )
    


    
    # something like should be the chronological order
    hamiltonian.evolve(times=self.durations)
