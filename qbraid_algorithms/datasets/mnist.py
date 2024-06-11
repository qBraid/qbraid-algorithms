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
Module defining MNIST dataset for reservoir computing tasks.

"""
import numpy as np


def load_mnist_data(download: bool = False, train: bool = True) -> np.ndarray:
    """Load the MNIST dataset."""
    import torchvision  # pylint: disable=import-outside-toplevel

    transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])
    dataset = torchvision.datasets.MNIST(
        "./MNIST_data/", download=download, train=train, transform=transform
    )
    dataset_array: np.ndarray = dataset.data.numpy()
    return dataset_array
