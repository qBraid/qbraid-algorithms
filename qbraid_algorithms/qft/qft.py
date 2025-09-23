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
Quantum Fourier Transform (QFT) Algorithm Implementation

This module provides a complete implementation of the Quantum Fourier Transform,
a fundamental building block for many quantum algorithms.

The QFT transforms quantum states from the computational basis to the Fourier basis
by applying Hadamard gates and controlled phase rotations. It's essential for
algorithms like Shor's algorithm and quantum phase estimation, providing the
quantum analogue of the classical discrete Fourier transform.

Formulation:
    The QFT transforms a quantum state |j⟩ to |ψ⟩ = 1/√N Σₖ₌₀^(N-1) e^(2πijk/N)|k⟩
    where N = 2ⁿ for n qubits. The circuit implements this using Hadamard gates H
    and controlled phase rotations R_k with phase φ = 2π/2^k. The total circuit
    depth is O(n²) with O(n²) gates.
"""
import os
import shutil
from pathlib import Path

import pyqasm
from pyqasm.modules.base import QasmModule

from qbraid_algorithms.qtran import QasmBuilder
from qbraid_algorithms.utils import _prep_qasm_file

from .qft_lib import QFTLibrary


def generate_program(num_qubits: int) -> QasmModule:
    """
    Load the Quantum Fourier Transform circuit as a pyqasm module.
    Args:
        num_qubits (int): The number of qubits for the QFT.

    Returns:
        (PyQasm Module) pyqasm module containing the QFT circuit
    """

    # Load the algorithm
    sys = QasmBuilder(qubits=num_qubits)
    qft = sys.import_library(QFTLibrary)
    qft.QFT([*range(num_qubits)])
    module = pyqasm.loads(sys.build())

    return module


def save_to_qasm(num_qubits: int, quiet: bool = False, path: str | None = None) -> None:
    """
    Creates a QFT subroutine module with user-defined number of qubits.

    Args:
        num_qubits (int): The number of qubits for the QFT.
        quiet (bool): If True, suppresses output messages.
        path (str): The directory path where the QFT subroutine will be created.
                   If None, creates in the current working directory.

    Returns:
        None
    """
    # Copy the QFT subroutine QASM file to the specified or current working directory
    qft_src = Path(__file__).parent.parent / "qasm_resources/qft_subroutine.qasm"
    if path is None:
        qft_dst = os.path.join(os.getcwd(), "qft.qasm")
    else:
        qft_dst = os.path.join(path, "qft.qasm")
    shutil.copy(qft_src, qft_dst)

    # Replace variable placeholders with user-defined parameters
    replacements = {"QFT_SIZE": str(num_qubits)}
    _prep_qasm_file(qft_dst, replacements)

    if not quiet:
        print(f"Subroutine 'qft' has been added to {qft_dst}")
