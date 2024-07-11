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
from typing import Any

import numpy as np
from bloqade.ir.location import Chain

from .time_evolution import AnalogProgramEvolver


@dataclass
class DetuningLayer:
    """Class representing a detuning layer in a quantum reservoir."""

    num_sites: int  # Number of sites in the chain lattice
    lattice_spacing: float  # Lattice spacing ()
    omega: float  # Rabi frequency
    step_size: float  # Time evolution duration
    num_steps: int  # Number of time steps


class QRCModel:
    """Quantum Reservoir Computing (QRC) model."""

    def __init__(self, model_pca: Any, delta_max: float, detuning_layer: DetuningLayer):
        """
        Initialize the Quantum Reservoir Computing model with necessary components.

        Args:
            model_pca (Any): PCA model component.
            delta_max (float): Maximum delta parameter.
            detuning_layer (DetuningLayer): Detuning layer for the model.
        """
        self.model_pca = model_pca
        self.delta_max = delta_max
        self.detuning_layer = detuning_layer

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
        probabilities = evolver.evolve(backend="emulator")

        # TODO: added dot as placeholder, will need to revisit
        output_vector = np.dot(probabilities, x)

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

    def predict(self, xs: np.ndarray) -> list[int]:
        """
        Compute predictions for input images or data using quantum reservoir computing.

        Args:
            xs (np.ndarray): Input data, either a batch of images or a single image.

        Returns:
            list[int]: Predicted classes or values.

        TODO: Implement the transformation and prediction steps.
        """
        raise NotImplementedError
