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
Module for encoding of data.

"""
import numpy as np
import torch
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
