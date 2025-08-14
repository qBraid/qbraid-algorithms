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
Module providing Quantum Fourier Transform (QFT) algorithm implementation.

"""
import os
import shutil
import tempfile
from pathlib import Path

import pyqasm
from pyqasm.modules.base import QasmModule

from qbraid_algorithms.utils import _prep_qasm_file


def load_program(num_qubits: int) -> QasmModule:
    """
    Load the Quantum Fourier Transform circuit as a pyqasm module.
    Args:
        num_qubits (int): The number of qubits for the QFT.

    Returns:
        (PyQasm Module) pyqasm module containing the QFT circuit
    """
    # Load the QFT QASM files into a staging directory
    temp_dir = tempfile.mkdtemp()
    qft_src = Path(__file__).parent / "qft.qasm"
    qft_sub_src = Path(__file__).parent / "qft_subroutine.qasm"
    qft_dst = os.path.join(temp_dir, "qft.qasm")
    qft_sub_dst = os.path.join(temp_dir, "qft_subroutine.qasm")
    shutil.copy(qft_src, qft_dst)
    shutil.copy(qft_sub_src, qft_sub_dst)

    # Replace variable placeholders with user-defined parameters
    replacements = {"QFT_SIZE": str(num_qubits)}
    _prep_qasm_file(qft_sub_dst, replacements)
    _prep_qasm_file(qft_dst, replacements)

    # Load the algorithm
    module = pyqasm.load(qft_dst)

    # Delete the created files
    shutil.rmtree(temp_dir)

    return module


def generate_subroutine(num_qubits: int, quiet: bool = False, path: str = None) -> None:
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
    qft_src = Path(__file__).parent / "qft_subroutine.qasm"
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
