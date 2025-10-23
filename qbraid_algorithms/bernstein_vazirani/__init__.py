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
Bernstein-Vazirani Algorithm

.. admonition:: Bernstein-Vazirani
   :class: note-enhanced

    This module provides a complete implementation of the Bernstein-Vazirani algorithm,
    a quantum algorithm that demonstrates quantum parallelism by determining a hidden
    bit string with a single query.
    The algorithm works by preparing a superposition of all possible inputs, applying
    an oracle that encodes the hidden bit string, then using the inverse quantum
    Fourier transform to extract the hidden string. This achieves exponential speedup
    over classical algorithms that require n queries for an n-bit string.

.. admonition:: FORMULATION
   :class: seealso

    For a hidden n-bit string :math:`s` and oracle function :math:`f(x) = s \\cdot x \\pmod{2}`:

    1. **State Preparation**: Initialize :math:`n` qubits in superposition and ancilla in :math:`|-\\rangle`:

        :math:`H^{\\otimes n}|0\\rangle^{\\otimes n} \\otimes |-\\rangle =
        \\frac{1}{\\sqrt{2^n}} \\sum_{x=0}^{2^n-1} |x\\rangle \\otimes |-\\rangle`

    2. **Oracle Application**: Apply :math:`U_f` implementing phase kickback:

        :math:`U_f|x\\rangle|-\\rangle = (-1)^{f(x)}|x\\rangle|-\\rangle =
        (-1)^{s \\cdot x}|x\\rangle|-\\rangle`

    3. **Hadamard Transform**: Apply :math:`H^{\\otimes n}` to extract the hidden string:

        :math:`H^{\\otimes n} \\left[\\frac{1}{\\sqrt{2^n}} \\sum_{x} (-1)^{s \\cdot x}|x\\rangle\\right] =
        |s\\rangle`

    Direct measurement yields the hidden string :math:`s` with probability 1,
    demonstrating quantum parallelism through superposition and interference.

.. admonition:: Functions
   :class: seealso

    .. autosummary::
        :toctree: ../stubs/

        generate_program
        save_to_qasm
        generate_oracle
"""

from .bernvaz import generate_oracle, generate_program, save_to_qasm

__all__ = ["generate_program", "save_to_qasm", "generate_oracle"]
