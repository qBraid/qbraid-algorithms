# Copyright 2025 qBraid
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Rodeo Algorithm

.. admonition:: Rodeo
   :class: note-enhanced

    This module provides an implementation of the **Rodeo algorithm**, a quantum
    algorithm for estimating expectation values of observables with high precision.
    The Rodeo algorithm is particularly useful for **quantum chemistry**, **quantum simulation**,
    and **variational quantum algorithms** where accurate expectation value estimation
    is crucial for optimization and ground state preparation.
    The algorithm uses **controlled Hamiltonian evolution** with **random phase shifts**
    and **ancilla measurements** to extract expectation values with reduced resource
    requirements compared to standard quantum expectation value estimation methods.

.. admonition:: FORMULATION
   :class: seealso

    **Problem**: Given a quantum state :math:`|\\psi\\rangle` and observable :math:`O`,
    estimate the expectation value :math:`\\langle\\psi|O|\\psi\\rangle`.

    **Algorithm Steps**:

    1. **Ancilla Preparation**: Prepare ancilla qubit in superposition:

            :math:`|+\\rangle = \\frac{1}{\\sqrt{2}}(|0\\rangle + |1\\rangle)`

    2. **Controlled Evolution**: Apply controlled Hamiltonian evolution with random time :math:`t`:

            :math:`|\\psi_1\\rangle = \\frac{1}{\\sqrt{2}}(|0\\rangle|\\psi\\rangle +
            |1\\rangle e^{-iOt}|\\psi\\rangle)`

    3. **Ancilla Rotation**: Apply Hadamard to ancilla for interference:

            :math:`|\\psi_2\\rangle = \\frac{1}{2}[(1 + e^{-iOt})|0\\rangle|\\psi\\rangle +
            (1 - e^{-iOt})|1\\rangle|\\psi\\rangle]`

    4. **Measurement**: Measure ancilla and extract expectation value from statistics

    **Expectation Value Extraction**: For small evolution times :math:`t`, the expectation
    value is estimated as:

        :math:`\\langle\\psi|O|\\psi\\rangle = \\lim_{t \\to 0} \\frac{1}{t} \\arcsin(\\sqrt{P_1})`

        where :math:`P_1` is the probability of measuring :math:`|1\\rangle` in the ancilla.

    **Variance Reduction**: The algorithm achieves improved precision through:

    - **Random Sampling**: Multiple evolution times reduce systematic errors
    - **Statistical Averaging**: Ensemble measurements improve accuracy
    - **Controlled Evolution**: Direct access to Hamiltonian eigenvalue information


.. admonition:: Classes
   :class: seealso

    .. autosummary::
        :toctree: ../stubs/

        RodeoLibrary

"""
from .rodeo import RodeoLibrary

__all__ = ["RodeoLibrary"]
