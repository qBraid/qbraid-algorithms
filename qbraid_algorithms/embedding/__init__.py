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
Quantum Block Encoding and Embedding

.. admonition:: Quantum Block Encoding
   :class: note-enhanced

    This module provides implementations of quantum **block encoding** techniques for
    embedding classical matrices into quantum circuits.
    Block encoding is fundamental for quantum linear algebra algorithms, enabling efficient quantum implementations
    of matrix operations through unitary transformations.
    The module implements preparation-selection (Prep-Select) frameworks and specialized
    embeddings for structured matrices like **Toeplitz**, **diagonal**, and **Pauli** forms, providing
    quantum speedups for linear algebraic computations.

.. admonition:: FORMULATION
   :class: seealso

    **Block Encoding Definition**: For a matrix :math:`A \\in \\mathbb{C}^{2^n \\times 2^n}`
    with :math:`\\|A\\| \\leq \\alpha`, a :math:`(\\alpha, a, \\epsilon)`-block encoding is a
    unitary :math:`U` such that:

        :math:`\\langle 0^a | U | 0^a \\rangle = \\frac{A}{\\alpha} + E`

        where :math:`\\|E\\| \\leq \\epsilon` and :math:`a` is the number of ancilla qubits.

    **Preparation-Selection Framework**:

    1. **Preparation**: Create superposition over matrix elements:

        :math:`\\text{PREP}|0\\rangle = \\sum_{j} \\sqrt{p_j} |j\\rangle`

    2. **Selection**: Apply controlled operations based on index:

        :math:`\\text{SELECT}|j\\rangle|\\psi\\rangle = |j\\rangle U_j|\\psi\\rangle`

    3. **Block Encoding**: Combine preparation and selection:

        :math:`U = \\text{PREP}^\\dagger \\cdot \\text{SELECT} \\cdot \\text{PREP}`

    **Specialized Embeddings**:

    - **Toeplitz**: Exploit circulant structure via quantum Fourier transforms
    - **Diagonal**: Direct phase encoding for diagonal matrices
    - **Pauli Decomposition**: Express operators as weighted Pauli string sums

.. admonition:: Classes
   :class: seealso

    .. autosummary::
        :toctree: ../stubs/

        PrepSelLibrary
        Prep
        Select
        PauliOperator
        Toeplitz
        Diagonal

"""
from .prep_sel import PauliOperator, Prep, PrepSelLibrary, Select
from .toeplitz import Diagonal, Toeplitz

__all__ = [
    "prep_sel",
    "Toeplitz",
    "Prep",
    "Select",
    "Diagonal",
    "PauliOperator",
    "PrepSelLibrary",
]
