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
.. admonition:: qBraid Algorithms
   :class: note-enhanced

   Python package containing quantum and hybrid quantum-classical algorithms that can
   be used to carry out research and investigate how to solve problems in different
   domains on simulators and near-term real quantum devices using shallow circuits.

.. admonition:: Modules
   :class: seealso

    .. autosummary::
        :toctree: ../stubs/

        bells_inequality
        bernstein_vazirani
        qft
        iqft
        qpe
        qtran
        hhl
        evolution
        embedding
        amplitude_amplification
        rodeo

"""

from ._version import __version__

__all__ = [
    "__version__",
    "bells_inequality",
    "qft",
    "iqft",
    "bernstein_vazirani",
    "qpe",
    "qtran",
    "evolution",
    "embedding",
    "amplitude_amplification",
    "hhl",
    "rodeo",
]
