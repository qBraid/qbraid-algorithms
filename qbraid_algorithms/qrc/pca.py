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
Module implemting Principal Component Analysis (PCA) for dimensionality reduction.

"""
import numpy as np
import torch
from sklearn.decomposition import PCA


def pca_reduction(
    data: torch.Tensor,
    n_components: int,
    data_dim: int,
    delta_max: int,
    train: bool = True,
) -> torch.Tensor:
    """
    Perform PCA reduction on the provided data using PyTorch's pca_lowrank to
    reduce its dimensionality.

    Args:
        data (torch.Tensor): The input data tensor where each row represents a sample.
        n_components (int): The number of principal components to retain.
        data_dim (int) : The dimension of the input data required for doing PCA.
        delta_max (int) : The scaling factor for bring PCA values to the feasible range of local detuning.
        train (bool, optional): Whether the data is training data. Defaults to True.

    Returns:
        torch.Tensor: The transformed data
    """
    # Perform PCA on training data
    pca = PCA(n_components=n_components)
    data_array: np.ndarray = data.data.numpy()
    data_reshaped = data_array.reshape(-1, data_dim)
    if train:
        data_pca = pca.fit_transform(data_reshaped)
    else:
        data_pca = pca.transform(data_reshaped)

    # Scale PCA values to feasible range of local detuning
    scaled_data_pca = data_pca / np.max(np.abs(data_pca)) * delta_max

    return scaled_data_pca
