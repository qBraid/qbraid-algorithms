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

import torch
from sklearn.preprocessing import OneHotEncoder

def one_hot_encoding(labels: torch.Tensor, num_classes: int) -> torch.Tensor:
    """
    Convert a tensor of numeric labels into a one-hot encoded matrix using PyTorch.

    Args:
        labels (torch.Tensor): The tensor of labels to encode.
        num_classes (int): The total number of classes.

    Returns:
        torch.Tensor: The one-hot encoded matrix where each row corresponds to a label.

    TODO: Implement the one-hot encoding function.
    """
    # Placeholder for actual implementation.
    encoder = OneHotEncoder(sparse_output=False)
    # I don't know if the reshape params will be universal or not
    encoded_data = encoder.fit_transform(lables.targets.numpy().reshape(-1, 1))
    # return torch.nn.functional.one_hot(labels, num_classes=num_classes)
