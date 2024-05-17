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
from typing import Any, Callable

import numpy as np

from .dynamics import DetuningLayer


@dataclass
class QRCModel:
    """Quantum Reservoir Computing (QRC) model."""

    model_pca: Any  # PCA model component
    spectral: float  # Spectral radius or related parameter
    delta_max: float  # Maximum delta parameter
    detuning_layer: DetuningLayer  # Detuning layer
    linear_regression: Callable  # Linear regression model

    def __call__(self, xs: np.ndarray) -> list[int]:
        """
        Compute predictions for input images or data using quantum reservoir computing.

        Args:
            xs (np.ndarray): Input data, either a batch of images or a single image.

        Returns:
            list[int]: Predicted classes or values.

        TODO: Implement the transformation and prediction steps.
        """
        raise NotImplementedError
