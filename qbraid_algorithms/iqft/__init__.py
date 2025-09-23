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
Inverse Quantum Fourier Transform (IQFT)

.. admonition:: Inverse Quantum Fourier Transform (IQFT)
   :class: note-enhanced

    This module provides an implementation of the **Inverse Quantum Fourier Transform (IQFT)**,
    the inverse operation of the Quantum Fourier Transform.
    The IQFT is essential for extracting information from quantum algorithms, particularly
    in quantum phase estimation, Shor's algorithm, and other quantum algorithms that
    require converting from the frequency domain back to the computational basis.
    The IQFT transforms quantum states from Fourier basis back to computational basis,
    enabling measurement and classical post-processing of quantum algorithm results.

.. admonition:: FORMULATION
   :class: seealso

    **Transformation**: The IQFT is the inverse of the QFT, transforming an :math:`n`-qubit 
    state from the Fourier basis back to the computational basis:

        :math:`\\text{IQFT}|j\\rangle = \\frac{1}{\\sqrt{2^n}} \\sum_{k=0}^{2^n-1} 
        \\omega_n^{-jk} |k\\rangle`

        where :math:`\\omega_n = e^{2\\pi i/2^n}` is the primitive :math:`2^n`-th root of unity.

    **Circuit Implementation**: The IQFT circuit consists of:

    1. **Swap Operations**: Reverse the qubit order from QFT
    
    2. **Inverse Controlled Rotations**: Apply :math:`R_k^{\\dagger}` gates where:
    
       :math:`R_k^{\\dagger} = \\begin{pmatrix} 1 & 0 \\\\ 0 & e^{-2\\pi i/2^k} \\end{pmatrix}`

    3. **Inverse Hadamard Gates**: Apply :math:`H^{\\dagger} = H` to each qubit

    **Matrix Form**: For :math:`n` qubits, the IQFT matrix is:

        :math:`\\text{IQFT} = \\frac{1}{\\sqrt{2^n}} \\begin{pmatrix}
        1 & 1 & 1 & \\cdots & 1 \\\\
        1 & \\omega_n^{-1} & \\omega_n^{-2} & \\cdots & \\omega_n^{-(2^n-1)} \\\\
        \\vdots & \\vdots & \\vdots & \\ddots & \\vdots \\\\
        1 & \\omega_n^{-(2^n-1)} & \\omega_n^{-2(2^n-1)} & \\cdots & \\omega_n^{-(2^n-1)^2}
        \\end{pmatrix}`


.. admonition:: Functions
   :class: seealso

    .. autosummary::
        :toctree: ../stubs/

        generate_program
        save_to_qasm

"""

from .iqft import generate_program, save_to_qasm

__all__ = ["generate_program", "save_to_qasm"]
