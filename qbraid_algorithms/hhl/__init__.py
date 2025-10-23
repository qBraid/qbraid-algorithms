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
Harrow-Hassidim-Lloyd (HHL) Algorithm

.. admonition:: Harrow-Hassidim-Lloyd (HHL)
   :class: note-enhanced

    This module provides an implementation of the **Harrow-Hassidim-Lloyd (HHL)** algorithm,
    a quantum algorithm for solving systems of linear equations.
    The HHL algorithm offers exponential speedup over classical methods for certain
    classes of sparse, well-conditioned matrices, making it fundamental for quantum
    machine learning, optimization, and scientific computing applications.
    The algorithm combines **quantum phase estimation**, **controlled rotations**,
    and **amplitude amplification** to encode the solution of :math:`A\\mathbf{x} = \\mathbf{b}`
    in quantum amplitudes, enabling efficient extraction of linear system solutions.

.. admonition:: FORMULATION
   :class: seealso

    **Linear System Problem**: Given a Hermitian matrix :math:`A \\in \\mathbb{C}^{N \\times N}`
    and vector :math:`|b\\rangle`, find the solution :math:`|x\\rangle` to: :math:`A|x\\rangle = |b\\rangle`

    **Algorithm Steps**:

    1. **State Preparation**: Prepare the input state :math:`|b\\rangle` and ancilla qubits:

            :math:`|\\psi_0\\rangle = |b\\rangle \\otimes |0\\rangle_{\\text{clock}} \\otimes
            |0\\rangle_{\\text{ancilla}}`

    2. **Quantum Phase Estimation**: Apply QPE to estimate eigenvalues :math:`\\lambda_j` of :math:`A`:

            :math:`|\\psi_1\\rangle = \\sum_j \\beta_j |u_j\\rangle \\otimes |\\tilde{\\lambda}_j\\rangle \\otimes
            |0\\rangle`

    3. **Controlled Rotation**: Apply controlled rotation based on eigenvalue estimates:

            :math:`|\\psi_2\\rangle = \\sum_j \\beta_j |u_j\\rangle \\otimes |\\tilde{\\lambda}_j\\rangle \\otimes
            \\left(\\sqrt{1-\\frac{C^2}{\\tilde{\\lambda}_j^2}}|0\\rangle + \\frac{C}{\\tilde{\\lambda}_j}|1
            \\rangle\\right)`

    4. **Uncomputation**: Reverse QPE and measure ancilla in :math:`|1\\rangle` state:

            :math:`|x\\rangle = \\frac{1}{\\sqrt{\\sum_j |\\beta_j|^2/\\lambda_j^2}} \\sum_j
            \\frac{\\beta_j}{\\lambda_j} |u_j\\rangle`

    **Complexity**: The algorithm achieves :math:`\\mathcal{O}(\\log(N) s^2 \\kappa^2 / \\epsilon)`
    runtime, where :math:`s` is the sparsity, :math:`\\kappa` is the condition number,
    and :math:`\\epsilon` is the desired precision.

    **Requirements**: Efficient state preparation for :math:`|b\\rangle`, well-conditioned
    matrix :math:`A`, and sparse Hamiltonian simulation for :math:`e^{iAt}`.

.. admonition:: Classes
   :class: seealso

    .. autosummary::
        :toctree: ../stubs/

        HHLLibrary

"""
from .hhl import HHLLibrary

__all__ = ["HHLLibrary"]
