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
Quantum Phase Estimation (QPE)

.. admonition:: Quantum Phase Estimation (QPE)
   :class: note-enhanced

    This module provides an implementation of the **Quantum Phase Estimation (QPE)** algorithm,
    a fundamental quantum algorithm for estimating eigenvalues of unitary operators.
    QPE is central to many quantum algorithms including **Shor's algorithm**, **HHL algorithm**,
    and quantum simulation, providing exponential precision improvement over classical methods.
    The algorithm uses **controlled unitary operations** and the **quantum Fourier transform**
    to extract phase information with high precision, enabling efficient eigenvalue
    computation for quantum systems and linear algebra applications.

.. admonition:: FORMULATION
   :class: seealso

    **Problem**: Given a unitary operator :math:`U` and eigenstate :math:`|u\\rangle` such that
    :math:`U|u\\rangle = e^{2\\pi i \\varphi}|u\\rangle`, estimate the phase :math:`\\varphi`.

    **Algorithm Steps**:

    1. **Initialization**: Prepare :math:`n` ancilla qubits in superposition and eigenstate:

            :math:`|\\psi_0\\rangle = \\frac{1}{\\sqrt{2^n}} \\sum_{j=0}^{2^n-1} |j\\rangle \\otimes |u\\rangle`

    2. **Controlled Unitary Evolution**: Apply controlled :math:`U^{2^k}` operations:

            :math:`|\\psi_1\\rangle = \\frac{1}{\\sqrt{2^n}} \\sum_{j=0}^{2^n-1}
            e^{2\\pi i \\varphi j} |j\\rangle \\otimes |u\\rangle`

    3. **Inverse QFT**: Apply IQFT to ancilla register:

            :math:`|\\psi_2\\rangle = |\\tilde{\\varphi}\\rangle \\otimes |u\\rangle`

    4. **Measurement**: Measure ancilla to obtain :math:`n`-bit approximation :math:`\\tilde{\\varphi}`

    **Precision**: With :math:`n` ancilla qubits, QPE estimates :math:`\\varphi` to
    :math:`n`-bit precision with high probability:

            :math:`|\\varphi - \\tilde{\\varphi}| \\leq \\frac{1}{2^n}`

    **Success Probability**: For exact phases representable in :math:`n` bits,
    success probability is 1. For general phases, success probability
    :math:`\\geq \\frac{4}{\\pi^2} \\approx 0.405`.

    **Circuit Depth**: Requires :math:`O(n^2)` gates and :math:`O(n)` applications
    of controlled-:math:`U^{2^k}` operations.

.. admonition:: Classes
   :class: seealso

    .. autosummary::
        :toctree: ../stubs/

        PhaseEstimationLibrary

.. admonition:: Functions
   :class: seealso

    .. autosummary::
        :toctree: ../stubs/

        load_program
        generate_subroutine
        get_result

"""

from .phase_est import PhaseEstimationLibrary
from .qpe import generate_subroutine, get_result, load_program

__all__ = [
    "load_program",
    "generate_subroutine",
    "get_result",
    "PhaseEstimationLibrary",
]
