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
Module providing Inverse Quantum Fourier Transform (IQFT) algorithm implementation.

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
    Load the Inverse Quantum Fourier Transform circuit as a pyqasm module.

    Args:
        num_qubits (int): The number of qubits for the IQFT.

    Returns:
        (PyQasm Module) pyqasm module containing the IQFT circuit
    """
    # Load the IQFT QASM files into a staging directory
    temp_dir = tempfile.mkdtemp()
    iqft_src = Path(__file__).parent / "iqft.qasm"
    iqft_sub_src = Path(__file__).parent / "iqft_subroutine.qasm"
    iqft_dst = os.path.join(temp_dir, "iqft.qasm")
    iqft_sub_dst = os.path.join(temp_dir, "iqft_subroutine.qasm")
    shutil.copy(iqft_src, iqft_dst)
    shutil.copy(iqft_sub_src, iqft_sub_dst)

    # Replace variable placeholders with user-defined parameters
    replacements = {"IQFT_SIZE": str(num_qubits)}
    _prep_qasm_file(iqft_sub_dst, replacements)
    _prep_qasm_file(iqft_dst, replacements)

    # Load the algorithm as a pyqasm module
    module = pyqasm.load(iqft_dst)

    # Delete the created files
    shutil.rmtree(temp_dir)

    return module


def generate_subroutine(num_qubits: int, quiet: bool = False, path: str | None = None) -> None:
    """
    Creates an IQFT subroutine module with user-defined number of qubits.

    Args:
        num_qubits (int): The number of qubits for the IQFT.
        quiet (bool): If True, suppresses output messages.
        path (str): The directory path where the IQFT subroutine will be created.
                   If None, creates in the current working directory.

    Returns:
        None
    """
    # Copy the IQFT subroutine QASM file to the specified or current working directory
    iqft_src = Path(__file__).parent / "iqft_subroutine.qasm"
    if path is None:
        iqft_dst = os.path.join(os.getcwd(), "iqft.qasm")
    else:
        iqft_dst = os.path.join(path, "iqft.qasm")
    shutil.copy(iqft_src, iqft_dst)

    # Replace variable placeholders with user-defined parameters
    replacements = {"IQFT_SIZE": str(num_qubits)}
    _prep_qasm_file(iqft_dst, replacements)

    if not quiet:
        print(f"Subroutine 'iqft' has been added to {iqft_dst}")
