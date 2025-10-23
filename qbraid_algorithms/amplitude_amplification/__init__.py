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

r"""
Amplitude Amplification Algorithm

.. admonition:: Amplitude Amplification
   :class: note-enhanced

   This module provides implementations of amplitude amplification algorithms, including
   Grover's algorithm and general amplitude amplification techniques.
   **Grover's algorithm** provides quadratic speedup for searching unsorted databases by
   repeatedly applying an oracle that marks target states and diffusion operator that
   inverts amplitudes about average. **General Amplitude Amplification** works with
   arbitrary oracles and state preparation operators.

.. admonition:: FORMULATION
   :class: seealso

   .. container:: side-by-side

      .. container:: left-box

         .. admonition:: Grover's
            :class: note

            For a search space of :math:`N` items containing :math:`M` target solutions:

            * **Oracle operator**: :math:`O_f = I - 2|f\rangle\langle f|`   ``marks target states``
            * **Diffusion operator**: :math:`D = 2|s\rangle\langle s| - I` where
              :math:`|s\rangle = \frac{1}{\sqrt{N}}\sum_{i=0}^{N-1}|i\rangle`
            * **Grover operator**: :math:`G = D \cdot O_f`
            * **Optimal iterations**: :math:`k \approx \frac{\pi}{4}\sqrt{\frac{N}{M}}`
            * **Success probability**: approaches 1 after :math:`k` iterations

      .. container:: right-box

         .. admonition:: General Amplitude Amplification
            :class: note

            For initial state :math:`|\psi\rangle` and target subspace spanned by good states:

            * **State preparation**: :math:`A|\psi\rangle = \sqrt{1-a}|\psi_0\rangle + \sqrt{a}|\psi_1\rangle`
            * **Reflection operators**:

              - :math:`S_{\psi} = I - 2|\psi\rangle\langle\psi|`   ``reflects about initial state``
              - :math:`S_{\chi} = I - 2|\chi\rangle\langle\chi|`   ``reflects about good states``

            * **Amplitude amplification operator**: :math:`Q = -A S_{\psi} A^{\dagger} S_{\chi}`
            * **Amplified amplitude**: grows as :math:`\sin((2k+1)\theta)` where :math:`\sin^2(\theta) = a`

.. admonition:: Classes
   :class: seealso

   .. autosummary::
      :toctree: ../stubs/

      AALibrary

"""

from .amp_ampl import AALibrary

__all__ = ["AALibrary"]
