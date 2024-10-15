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
Module for assembling QRC model components and computing prediction.

"""
from dataclasses import dataclass
from decimal import Decimal

import numpy as np
from bloqade.emulate.ir.atom_type import ThreeLevelAtomType
from bloqade.emulate.ir.emulator import Register
from bloqade.emulate.ir.space import Space
from bloqade.emulate.ir.state_vector import StateVector
from bloqade.ir.location import Chain

from .encoding import PCA
from .time_evolution import AnalogProgramEvolver


@dataclass
class DetuningLayer:
    """Class representing a detuning layer in a quantum reservoir."""

    num_sites: int  # Number of sites in the chain lattice
    lattice_spacing: float  # Lattice spacing
    omega: float  # Rabi frequency
    step_size: float  # Time evolution duration
    num_steps: int  # Number of time steps


class QRCModel:
    """Quantum Reservoir Computing (QRC) model."""

    def __init__(self, pca: PCA, delta_max: float, detuning_layer: DetuningLayer):
        """
        Initialize the Quantum Reservoir Computing model with necessary components.

        """
        self.pca = pca
        self.delta_max = delta_max
        self.detuning_layer = detuning_layer
        self.space = self.compute_space()

        if self.detuning_layer.num_sites != self.pca.n_components:
            raise ValueError("PCA and detuning layer dimensions do not match.")

    @staticmethod
    def generate_sites(num_sites: int, lattice_spacing: float) -> list[tuple[Decimal, Decimal]]:
        """
        Generate a list of lattice positions as tuples with Decimal precision.

        Args:
            num_sites (int): The number of lattice sites.
            lattice_spacing (float): The spacing between each lattice site.

        Returns:
            list: A list of tuples, each representing the x-coordinate of a lattice site.
        """
        lattice_spacing = Decimal(str(lattice_spacing))
        return [(Decimal(0), Decimal(0) + i * lattice_spacing) for i in range(num_sites)]

    def compute_space(self) -> Space:
        """Compute Space object based on the detuning layer parameters."""
        atom_type = ThreeLevelAtomType()
        sites = self.generate_sites(
            self.detuning_layer.num_sites, self.detuning_layer.lattice_spacing
        )
        blockade_radius = Decimal("0")  # TODO: Calculate blockade radius based on detuning params
        register = Register(atom_type=atom_type, sites=sites, blockade_radius=blockade_radius)
        return Space.create(register)

    def apply_pca(self, xs: np.ndarray, data_dim: int, train: bool = True) -> np.ndarray:
        """
        Apply PCA transformation to the input data.

        Args:
            xs (np.ndarray): Input data.
            data_dim (int): The dimension of the input data required for doing PCA.
            train (bool, optional): Whether the data is training data. Defaults to True.

        Returns:
            np.ndarray: Transformed data.
        """
        return self.pca.reduce(xs, data_dim, self.delta_max, train)

    def apply_detuning(self, x: np.ndarray) -> np.ndarray:
        """
        Simulate quantum evolution and record output for a given set of values (x).

        Args:
            x (np.ndarray): Vector or matrix of real numbers representing PCA values for each image.

        Returns:
            np.ndarray: Output values from the simulation.
        """
        layer = self.detuning_layer

        # using 0th order. Will need to modify to consider slew rate based on hardware
        amplitude_omegas = [layer.omega] * (layer.num_steps - 2)
        amplitudes = list(np.pad(amplitude_omegas, (1, 1), mode="constant"))

        durations = [Decimal(layer.step_size)] * (layer.num_steps - 1)

        atoms = Chain(layer.num_sites, lattice_spacing=layer.lattice_spacing)

        evolver = AnalogProgramEvolver(atoms=atoms, rabi_amplitudes=amplitudes, durations=durations)

        state = StateVector(self.space, x)
        output_vector = evolver.evolve(backend="emulator", state=state)

        return output_vector

    def linear_regression(self, embeddings):
        """
        Perform linear regression on given data

        Args:
            embeddings: The input data tensor.

        Returns:
            Any: The predicted output tensor.

        TODO: Implement the linear regression model, possibly using torch.nn.Linear.
        """
        raise NotImplementedError

    def predict(self, xs: np.ndarray, data_dim: int, train: bool = True) -> list[int]:
        """
        Compute predictions for input images or data using quantum reservoir computing.

        Args:
            xs (np.ndarray): Input data, either a batch of images or a single image.

        Returns:
            list[int]: Predicted classes or values.

        TODO: Implement the transformation and prediction steps.
        """
        raise NotImplementedError
