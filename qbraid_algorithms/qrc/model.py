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

# from torch import nn


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


# Define neural network model
# class Net(nn.Module):
#     def __init__(self):
#         super(Net, self).__init__()
#         self.fc1 = nn.Linear(dim_pca, 10)
#     def forward(self, x):
#         x = torch.relu(self.fc1(x))
#         return x
#     # Train classical model using PCA features
#     model_reg = Net()
#     criterion = nn.CrossEntropyLoss()
#     optimizer = optim.Adam(model_reg.parameters(), lr=0.01)
#     for epoch in range(1000):
#         for x, y in train_loader:
#             x = x.view(-1, 28*28)
#             x_pca = pca.transform(x.numpy())
#             x_pca = torch.tensor(x_pca, dtype=torch.float32)
#             y = torch.tensor(y, dtype=torch.long)
#             optimizer.zero_grad()
#             output = model_reg(x_pca)
#             loss = criterion(output, y)
#             loss.backward()
#             optimizer.step()
#     # Train QRC model using quantum reservoir computing
#     pre_layer = DetuningLayer(atoms, readouts, Ω, t_start, t_end, step)
#     model_qrc = Net()
#     for epoch in range(1000):
#         for x, y in train_loader:
#             x = x.view(-1, 28*28)
#             x_pca = pca.transform(x.numpy())
