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


def pca_reduction(
    data: torch.Tensor, n_components: int = 2
) -> tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor, torch.Tensor]]:
    """
    Perform PCA reduction on the provided data using PyTorch's pca_lowrank to
    reduce its dimensionality.

    Args:
        data (torch.Tensor): The input data tensor where each row represents a sample.
        n_components (int): The number of principal components to retain.

    Returns:
        tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor, torch.Tensor]]: A tuple containing the
            transformed data and the PCA components (u, s, v) used for the transformation.

    TODO: Implement the PCA reduction function using torch.pca_lowrank or another suitable method.
    """
    # Placeholder for actual implementation.
    u, s, v = torch.pca_lowrank(data, q=n_components)
    transformed_data = torch.mm(data, v[:, :n_components])
    return transformed_data, (u, s, v)
