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
Quantum Hamiltonian Evolution

.. admonition:: Quantum Hamiltonian Evolution
   :class: note-enhanced

    This module provides implementations of quantum **Hamiltonian evolution** algorithms
    for simulating quantum systems and computing matrix functions.
    These techniques are fundamental for quantum simulation, quantum chemistry,
    quantum optimization, and quantum machine learning applications.
    The module implements **Trotter decomposition** methods for time evolution and
    **Generalized Quantum Signal Processing (GQSP)** for polynomial approximations
    of Hamiltonian functions, along with test Hamiltonians for benchmarking.

.. admonition:: FORMULATION
   :class: seealso

    **Time Evolution Problem**: Given a Hamiltonian :math:`H` and time :math:`t`,
    compute the unitary time evolution operator:

        :math:`U(t) = e^{-iHt}`

    **Trotter-Suzuki Decomposition**: For :math:`H = H_1 + H_2 + \\ldots + H_k`,
    approximate the evolution using product formulas:

    1. **First-order Trotter**:

        :math:`e^{-iHt} \\approx \\left(\\prod_{j=1}^k e^{-iH_j t/n}\\right)^n`

    2. **Suzuki Higher-order**: Recursive symmetric decomposition with coefficients
       :math:`p_k` and :math:`q_k`:

        :math:`S_{2k}(t) = \\prod_{j=1}^{5^{k-1}} S_2(p_k t) S_2(q_k t) S_2(p_k t)`

    **Generalized Quantum Signal Processing**: For polynomial :math:`P(x)`,
    construct a quantum circuit that implements: :math:`\\langle 0| U_{\\text{GQSP}} |0\\rangle = P(H)`
    using controlled rotations with optimized phase angles :math:`\\{\\phi_k\\}`:

        :math:`U_{\\text{GQSP}} = \\prod_{k=0}^d R_Y(\\phi_{2k}) R_Z(\\phi_{2k-1})
        (|1\\rangle\\langle 1| \\otimes H + |0\\rangle\\langle 0| \\otimes I)`

    **Test Hamiltonians**: Standard quantum many-body systems for benchmarking:

    - **Transverse Field Ising**: :math:`H = -J\\sum_{i} Z_i Z_{i+1} - h\\sum_i X_i`
    - **Heisenberg XYZ**: :math:`H = \\sum_{i} (J_x X_i X_{i+1} + J_y Y_i Y_{i+1} +
      J_z Z_i Z_{i+1})`
    - **Fermionic Hubbard**: :math:`H = -t\\sum_{\\langle i,j\\rangle,\\sigma}
      (c^\\dagger_{i\\sigma} c_{j\\sigma} + \\text{h.c.}) + U\\sum_i n_{i\\uparrow} n_{i\\downarrow}`

.. admonition:: Classes
   :class: seealso

    .. autosummary::
        :toctree: ../stubs/

        GQSP
        Trotter
        TransverseFieldIsing
        HeisenbergXYZ
        FermionicHubbard
        RandomizedHamiltonian

.. admonition:: Functions
   :class: seealso

    .. autosummary::
        :toctree: ../stubs/

        create_test_hamiltonians

"""
from .gqsp import GQSP
from .h_test_suite import (
    FermionicHubbard,
    HeisenbergXYZ,
    RandomizedHamiltonian,
    TransverseFieldIsing,
    create_test_hamiltonians,
)
from .trotter import Trotter

__all__ = [
    "Trotter",
    "GQSP",
    "TransverseFieldIsing",
    "HeisenbergXYZ",
    "FermionicHubbard",
    "RandomizedHamiltonian",
    "create_test_hamiltonians",
]
