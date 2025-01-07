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
from __future__ import annotations

import numpy as np
import sklearn.decomposition
import sklearn.preprocessing
import torch


def one_hot_encoding(labels: np.ndarray, train: bool = True) -> torch.Tensor:
    """
    Convert a tensor of numeric labels into a one-hot encoded matrix using PyTorch.

    Args:
        labels (np.ndarray): The array of labels to encode.

    Returns:
        torch.Tensor: The one-hot encoded matrix where each row corresponds to a label.

    """
    encoder = sklearn.preprocessing.OneHotEncoder(sparse_output=False)
    reshaped_data = labels.reshape(-1, 1)
    if train:
        encoded_data = encoder.fit_transform(reshaped_data)
    else:
        encoded_data = encoder.transform(reshaped_data)
    return encoded_data


class PCA:
    """Principal Component Analysis (PCA) for dimensionality reduction."""

    def __init__(self, n_components: int):
        """
        Initialize the PCA class with the number of principal components to retain.

        Args:
            n_components (int): The number of principal components to retain.
        """
        self.n_components = n_components
        self.pca = sklearn.decomposition.PCA(n_components=self.n_components)

    def reduce(
        self, data: np.ndarray, data_dim: int, delta_max: int, train: bool = True
    ) -> np.ndarray:
        """
        Perform PCA reduction on the provided data to reduce its dimensionality.

        Args:
            data (np.ndarray): The input data tensor where each row represents a sample.
            data_dim (int): The dimension of the input data required for doing PCA.
            delta_max (int): Scaling factor to bring PCA values into a feasible range
                for local detuning.
            train (bool, optional): Whether the data is training data. Defaults to True.

        Returns:
            np.ndarray: The transformed data.

        Raises:
            ValueError: If `data_dim` is not compatible with `data` shape or
                if `n_components` is larger than `data_dim`.
        """
        if data.shape[1] != data_dim:
            raise ValueError("data_dim does not match the number of columns in data.")
        if self.n_components > data_dim:
            raise ValueError("n_components cannot be greater than data_dim.")

        data_reshaped = data.reshape(-1, data_dim)
        if train:
            data_pca = self.pca.fit_transform(data_reshaped)
        else:
            data_pca = self.pca.transform(data_reshaped)

        # Avoid division by zero if all elements are the same
        max_abs_val = np.max(np.abs(data_pca))
        if max_abs_val == 0:
            raise ValueError(
                "All input data are identical; PCA transformation is "
                "undefined with delta_max scaling."
            )

        scaled_data_pca = data_pca / max_abs_val * delta_max
        return scaled_data_pca
