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
Unit tests for the QRC (Quantum Reservoir Computing) model.

"""
import numpy as np
import pytest

from qbraid_algorithms.qrc import PCA, DetuningLayer, QRCModel


@pytest.mark.parametrize("dim_pca", [3, 10])
def test_detuning_layer(dim_pca):
    """Test applying detuning layer to single feature vector."""
    hyperparams = {"lattice_spacing": 4, "omega": 2 * np.pi, "step_size": 0.5, "num_steps": 20}
    detuning_layer = DetuningLayer(num_sites=dim_pca, **hyperparams)
    model = QRCModel(pca=PCA(n_components=dim_pca), detuning_layer=detuning_layer, delta_max=0.6)

    input_vector = np.random.rand(2**dim_pca)
    output_vector = model.apply_detuning(input_vector)
    assert np.shape(input_vector)[0] == np.shape(output_vector)[0]


def test_pca_reduction_on_identical_data():
    """Test PCA reduction on identical data points."""
    pca = PCA(n_components=1)
    data = np.array([[1, 1], [1, 1], [1, 1]])
    with pytest.raises(ValueError):
        pca.reduce(data, data_dim=2, delta_max=10)


def test_pca_reduction():
    """Test PCA reduction on regular data."""
    pca = PCA(n_components=1)
    data = np.array([[1, 2], [3, 4], [5, 6]])
    result = pca.reduce(data, data_dim=2, delta_max=10, train=True)
    assert result.shape == (3, 1), "Output shape is incorrect."


def test_invalid_dimensions():
    """Test PCA reduction with invalid data dimensions."""
    pca = PCA(n_components=3)
    data = np.array([[1, 2], [3, 4]])
    with pytest.raises(ValueError):
        pca.reduce(data, data_dim=2, delta_max=10)
