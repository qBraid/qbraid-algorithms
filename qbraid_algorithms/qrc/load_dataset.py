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
Module implemting loading of MNIST dataset, could be later be made to support other datasets

"""

from torchvision import datasets, transforms


def load_dataset() -> tuple[torch.Tensor, torch.Tensor]:
      """
    Perform loading of MNiST dataset for now.

    Args:
        None

    Returns:
        tuple[torch.Tensor, torch.Tensor] which contains the training and testing datasets.
      """

  # Load MNIST dataset
  transform = transforms.Compose([transforms.ToTensor()])
  train_dataset = datasets.MNIST('~/.pytorch/MNIST_data/', download=True, train=True, transform=transform)
  test_dataset = datasets.MNIST('~/.pytorch/MNIST_data/', download=True, train=False, transform=transform)

  return (train_dataset, test_dataset)
