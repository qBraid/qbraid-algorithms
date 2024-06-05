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

import torch
from sklearn.decomposition import PCA

def pca_reduction(
    data: torch.Tensor, n_components: int = 2, data_dim: int = 10, delta_max: int = 10,
) -> tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor, torch.Tensor]]:
    """
    Perform PCA reduction on the provided data using PyTorch's pca_lowrank to
    reduce its dimensionality.

    Args:
        data (torch.Tensor): The input data tensor where each row represents a sample.
        n_components (int): The number of principal components to retain.
        data_dim (int) : The dimension of the input data required for doing PCA.
        delta_max (int) : The scaling factor for bring PCA values to the feasible range of local detuning.

    Returns:
        tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor, torch.Tensor]]: A tuple containing the
            transformed data and the PCA components (u, s, v) used for the transformation.

    TODO: Implement the PCA reduction function using torch.pca_lowrank or another suitable method.
    """
    # Perform PCA on training data
    pca = PCA(n_components=n_components)
    data_pca = pca.fit_transform(data.data.numpy().reshape(data_dim))
    
    # Scale PCA values to feasible range of local detuning
    scaled_data_pca = data_pca / np.max(np.abs(data_pca)) * delta_max

    # u, s, v = torch.pca_lowrank(data, q=n_components)
    # transformed_data = torch.mm(data, v[:, :n_components])
    # return transformed_data, (u, s, v)

    return scaled_data_pca
