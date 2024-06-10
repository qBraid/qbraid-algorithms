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
Module defining time-series datasets for reservoir computing tasks.

"""

import numpy as np
import torch
from numpy.lib.stride_tricks import sliding_window_view
from torch.utils.data import TensorDataset


def _to_tensors(x: list, y: list) -> TensorDataset:
    """Convert lists of numpy arrays into a formatted TensorDataset."""
    x_tensor = torch.tensor(x, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.float32).view(-1, 1, 1)
    return TensorDataset(x_tensor, y_tensor)


def create_sequences(data: np.ndarray, n_steps: int) -> tuple:
    """Create (input, output) pairs from time series data for model training."""
    x = sliding_window_view(data, window_shape=n_steps)

    y = data[n_steps:]
    x = x[: len(y)]

    return x, y


def create_time_series_data(n_points: int, cycles: int, n_steps: int) -> TensorDataset:
    """Generate a sine wave time series and create (input, output) pairs for model training."""
    t = np.linspace(0, 2 * np.pi * cycles, n_points)
    x, y = create_sequences(np.sin(t), n_steps)
    return _to_tensors(x, y)
