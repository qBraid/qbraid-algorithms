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

from qbraid_algorithms.qrc import DetuningLayer, QRCModel, pca_reduction


@pytest.mark.parametrize("dim_pca", [3, 10])
def test_detuning_layer(dim_pca):
    """Test applying detuning layer to single feature vector."""
    hyperparams = {"lattice_spacing": 4, "omega": 2 * np.pi, "step_size": 0.5, "num_steps": 20}
    detuning_layer = DetuningLayer(num_sites=dim_pca, **hyperparams)
    model = QRCModel(model_pca=pca_reduction, delta_max=0.6, detuning_layer=detuning_layer)

    input_vector = np.random.rand(2**dim_pca)
    output_vector = model.apply_detuning(input_vector)
    assert np.shape(input_vector) == np.shape(output_vector)
