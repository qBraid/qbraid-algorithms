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
Module for encoding of classical data.

"""
import numpy as np
import torch
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder


def one_hot_encoding(labels: np.ndarray, train: bool = True) -> torch.Tensor:
    """
    Convert a tensor of numeric labels into a one-hot encoded matrix using PyTorch.

    Args:
        labels (np.ndarray): The array of labels to encode.

    Returns:
        torch.Tensor: The one-hot encoded matrix where each row corresponds to a label.

    """
    encoder = OneHotEncoder(sparse_output=False)
    reshaped_data = labels.reshape(-1, 1)
    if train:
        encoded_data = encoder.fit_transform(reshaped_data)
    else:
        encoded_data = encoder.transform(reshaped_data)
    return encoded_data


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
        data_dim (int): The dimension of the input data required for doing PCA.
        delta_max (int): Scaling factor to bring PCA vals into a feasible range for local detuning.
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
