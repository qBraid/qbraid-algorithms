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
Quantum Fourier Transform (QFT)

.. admonition:: Quantum Fourier Transform (QFT)
   :class: note-enhanced

    This module provides an implementation of the **Quantum Fourier Transform (QFT)**,
    a fundamental quantum algorithm that performs the discrete Fourier transform
    on quantum states. The QFT is a cornerstone of quantum computing, serving as
    a key component in **Shor's algorithm**, **quantum phase estimation**, and
    many other quantum algorithms requiring frequency domain analysis.
    The QFT enables efficient transformation between computational and Fourier bases,
    providing exponential speedup over classical FFT for certain quantum applications.

.. admonition:: FORMULATION
   :class: seealso

    **Transformation**: The QFT maps an :math:`n`-qubit computational basis state 
    to a superposition in the Fourier basis:

        :math:`\\text{QFT}|j\\rangle = \\frac{1}{\\sqrt{2^n}} \\sum_{k=0}^{2^n-1} 
        \\omega_n^{jk} |k\\rangle`

        where :math:`\\omega_n = e^{2\\pi i/2^n}` is the primitive :math:`2^n`-th root of unity.


    **Circuit Implementation**: The QFT circuit consists of:

    1. **Hadamard Gates**: Apply :math:`H` to each qubit for uniform superposition
    
    2. **Controlled Phase Rotations**: Apply :math:`R_k` gates where:
    
            :math:`R_k = \\begin{pmatrix} 1 & 0 \\\\ 0 & e^{2\\pi i/2^k} \\end{pmatrix}`

    3. **Swap Operations**: Reverse qubit order for correct output

    **Recursive Structure**: For qubit :math:`j`, the QFT can be written as:

        :math:`\\text{QFT}|j\\rangle = \\frac{1}{\\sqrt{2}} 
        \\left(|0\\rangle + e^{2\\pi i \\cdot 0.j_n}|1\\rangle\\right) \\otimes
        \\frac{1}{\\sqrt{2}} \\left(|0\\rangle + e^{2\\pi i \\cdot 0.j_{n-1}j_n}|1\\rangle\\right) 
        \\otimes \\ldots`

    **Matrix Form**: The QFT matrix for :math:`n` qubits is:

        :math:`\\text{QFT} = \\frac{1}{\\sqrt{2^n}} \\begin{pmatrix}
        1 & 1 & 1 & \\cdots & 1 \\\\
        1 & \\omega_n & \\omega_n^2 & \\cdots & \\omega_n^{2^n-1} \\\\
        \\vdots & \\vdots & \\vdots & \\ddots & \\vdots \\\\
        1 & \\omega_n^{2^n-1} & \\omega_n^{2(2^n-1)} & \\cdots & \\omega_n^{(2^n-1)^2}
        \\end{pmatrix}`

    **Complexity**: Requires :math:`O(n^2)` gates compared to :math:`O(n \\log n)` 
    classical complexity, but enables quantum parallelism for quantum states.

.. admonition:: Classes
   :class: seealso

    .. autosummary::
        :toctree: ../stubs/

        QFTLibrary

.. admonition:: Functions
   :class: seealso

    .. autosummary::
        :toctree: ../stubs/

        generate_program
        save_to_qasm

"""

from .qft import generate_program, save_to_qasm
from .qft_lib import QFTLibrary

__all__ = ["generate_program", "save_to_qasm", "QFTLibrary"]
