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
Quantum Algorithm Translation and QASM Generation

.. admonition:: Quantum Translation Framework (QTRAN)
   :class: note-enhanced

    This module provides a comprehensive framework for **quantum algorithm translation**
    and **QASM code generation**. QTRAN enables systematic construction of quantum
    circuits through high-level abstractions, automated gate library management,
    and optimized QASM subroutine generation for quantum algorithms.
    The framework supports **modular circuit design**, **gate library composition**,
    and **cross-platform quantum code generation**, facilitating rapid development
    and deployment of quantum algorithms across different quantum hardware platforms.

.. admonition:: FORMULATION
   :class: seealso

    **Circuit Construction**: QTRAN provides builders for systematic quantum circuit assembly:

    **Gate Library Framework**: Organize quantum operations into reusable libraries:

        :math:`\\mathcal{L} = \\{G_1, G_2, \\ldots, G_n\\}`

        where each gate :math:`G_i` represents a quantum operation with associated parameters.

    **Circuit Builder Pattern**: Construct circuits through compositional operations:

        :math:`C = B(G_1 \\circ G_2 \\circ \\ldots \\circ G_n)`

        where :math:`B` is the builder function and :math:`\\circ` denotes gate composition.

    **QASM Generation**: Transform high-level circuit descriptions to executable QASM:

        :math:`\\text{QASM} = T(C, \\mathcal{P})`

        where :math:`T` is the translation function and :math:`\\mathcal{P}` are platform parameters.

    **Key Components**:

    - **FileBuilder**: Manages QASM file structure and includes
    - **GateBuilder**: Constructs individual quantum gates with parameters
    - **QasmBuilder**: Assembles complete QASM programs from components
    - **IncludeBuilder**: Handles library imports and dependencies
    - **GateLibrary**: Provides extensible gate operation collections
    - **std_gates**: Standard quantum gate implementations

    **Abstraction Levels**: Supports multiple abstraction levels from low-level
    gate operations to high-level algorithm subroutines, enabling both
    fine-grained control and rapid prototyping.

.. admonition:: Classes
   :class: seealso

    .. autosummary::
        :toctree: ../stubs/

        FileBuilder
        GateBuilder
        QasmBuilder
        IncludeBuilder
        GateLibrary
        std_gates

"""
# pylint: disable=invalid-name
from .gate_library import GateLibrary, std_gates
from .module_loader import qasm_pipe
from .qasm_builder import FileBuilder, GateBuilder, IncludeBuilder, QasmBuilder

__all__ = [
    "FileBuilder",
    "QasmBuilder",
    "GateBuilder",
    "IncludeBuilder",
    "GateLibrary",
    "std_gates",
    "qasm_pipe",
]
