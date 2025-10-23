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
Bell's Inequality Experiment

.. admonition:: Bell's Inequality Experiment
   :class: note-enhanced

   This module provides an implementation of Bell's inequality experiment, a fundamental
   test of quantum mechanics that demonstrates **Non-local correlations**.
   The experiment creates an entangled Bell state, applies different measurement bases
   to each qubit, and measures correlations.
   When Bell's inequality is violated, it
   proves that quantum correlations cannot be explained by classical local hidden
   variable theories.

.. admonition:: FORMULATION
   :class: seealso

    This implementation tests Bell's inequality using three Bell singlet states prepared between qubit pairs.

    1. **State Preparation**: Each qubit pair is prepared in the Bell singlet state:

        :math:`|\\Psi^-\\rangle = 1/\\sqrt{2}(|01\\rangle - |10\\rangle)`
    2. **Measurement Settings**: Three different measurement configurations:

        - Circuit AB: Alice measures at 0°, Bob measures at 60° (:math:`\\pi/3`)
        - Circuit AC: Alice measures at 0°, Charlie measures at 120° (:math:`2\\pi/3`)
        - Circuit BC: Bob measures at 60° (:math:`\\pi/3`), Charlie measures at 120° (:math:`2\\pi/3`)
    3. **Bell's Inequality**: The CHSH inequality for Bell singlet states:

        :math:`|E(0°, 60°) - E(0°, 120°) + E(60°, 120°)| \\leq 2`

        where :math:`E(\\theta_A, \\theta_B) = -\\cos(\\theta_A - \\theta_B)` is the correlation function.
    4. **Quantum Prediction**: For Bell singlet states, quantum mechanics predicts:

        :math:`|E(0°, 60°) - E(0°, 120°) + E(60°, 120°)| = |-\\cos(60°) + \\cos(120°) - \\cos(60°)| = 3 > 2`

        This violates Bell's inequality, demonstrating non-local quantum correlations.

.. admonition:: Functions
   :class: seealso

    .. autosummary::
       :toctree: ../stubs/

       generate_program

"""

from .bells_inequality import generate_program

__all__ = [
    "generate_program",
]
