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
Module providing Bernstein-Vazirani algorithm implementation.

"""
import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Union

import pyqasm
from pyqasm.modules.base import QasmModule

from qbraid_algorithms.utils import _prep_qasm_file


def load_program(bitstring: Union[str, list[int]]) -> QasmModule:
    """
    Load the Bernstein-Vazirani circuit as a pyqasm module.

    Args:
        bitstring (Union[str, list[int]]): The hidden bitstring `s` as a string of '0's
        and '1's

    Returns:
        (PyQasm Module) pyqasm module containing the Bernstein-Vazirani circuit
    """

    # Load the Bernstein-Vazirani QASM files into a staging directory
    temp_dir = tempfile.mkdtemp()
    bernvaz_src = Path(__file__).parent / "bernvaz.qasm"
    bernvaz_dst = os.path.join(temp_dir, "bernvaz.qasm")
    bernvaz_sub_src = Path(__file__).parent / "bernvaz_subroutine.qasm"
    bernvaz_sub_dst = os.path.join(temp_dir, "bernvaz_subroutine.qasm")
    shutil.copy(bernvaz_src, bernvaz_dst)
    shutil.copy(bernvaz_sub_src, bernvaz_sub_dst)

    # Replace variable placeholders with user-defined parameters
    replacements = _generate_replacements(bitstring)
    _prep_qasm_file(bernvaz_sub_dst, replacements)
    _prep_qasm_file(bernvaz_dst, replacements)

    # Load the algorithm as a pyqasm module
    module = pyqasm.load(bernvaz_dst)

    # Delete the created files
    shutil.rmtree(temp_dir)

    return module


def generate_subroutine(
    bitstring: Union[str, list[int]], quiet: bool = False, path: Optional[str] = None
) -> None:
    """
    Creates a Bernstein-Vazirani subroutine module with user-defined hidden bitstring.

    Args:
        bitstring (Union[str, list[int]]): The hidden bitstring.
        quiet (bool): If True, suppresses output messages.
        path (str): The directory path where the Bernstein-Vazirani subroutine will be created.
                   If None, creates in the current working directory.

    Returns:
        None
    """
    # Copy the B-V subroutine QASM file to the specified or current working directory
    bernvaz_src = Path(__file__).parent / "bernvaz_subroutine.qasm"
    if path is None:
        bernvaz_dst = os.path.join(os.getcwd(), "bernvaz.qasm")
    else:
        bernvaz_dst = os.path.join(path, "bernvaz.qasm")
    shutil.copy(bernvaz_src, bernvaz_dst)

    # Replace variable placeholders with user-defined parameters
    replacements = _generate_replacements(bitstring)
    _prep_qasm_file(bernvaz_dst, replacements)

    if not quiet:
        print(f"Subroutine 'bernvaz' has been added to {bernvaz_dst}")


def generate_oracle(
    bitstring: Union[str, list[int]], quiet: bool = False, path: Optional[str] = None
) -> None:
    """
    Creates a Bernstein-Vazirani oracle encoded with user-defined hidden bitstring.

    Args:
        bitstring (Union[str, list[int]]): The hidden bitstring `s` as a string
                                   of '0's and '1's
        quiet (bool): If True, suppresses output messages.
        path (str): The directory path where the Bernstein-Vazirani oracle will be created.
                   If None, creates in the current working directory.

    Returns:
        None
    """
    # Copy the oracle QASM file to the specified or current working directory
    oracle_src = Path(__file__).parent / "oracle.qasm"
    if path is None:
        oracle_dst = os.path.join(os.getcwd(), "oracle.qasm")
    else:
        oracle_dst = os.path.join(path, "oracle.qasm")
    shutil.copy(oracle_src, oracle_dst)

    # Replace variable placeholders with user-defined parameters
    replacements = _generate_replacements(bitstring)
    _prep_qasm_file(oracle_dst, replacements)

    if not quiet:
        print(f"Oracle 'oracle' has been added to {oracle_dst}")


def _convert_bitstring_decimal(bitstring: Union[str, list[int]]) -> int:
    """
    Converts a bitstring (str or list of int) to its decimal integer representation.

    Args:
        bitstring (Union[str, list[int]]): The hidden bitstring of '0's and '1's

    Returns:
        int: Decimal integer representation of the bitstring
    """
    if isinstance(bitstring, list):
        bitstring = "".join(str(b) for b in bitstring)
    # Reverse bitstring for correct qubit ordering
    bitstring_reversed = bitstring[::-1]
    return int(bitstring_reversed, 2)


def _generate_replacements(bitstring: Union[str, list[int]]) -> dict[str, str]:
    """
    Generates a dictionary of replacements for QASM variable placeholders.

    Args:
        bitstring (Union[str, list[int]]): The hidden bitstring of '0's and '1's

    Returns:
        dict[str, str]: Dictionary mapping variable names to their string values
    """
    input_size = len(bitstring)
    decimal_value = _convert_bitstring_decimal(bitstring)
    return {"BERNVAZ_SIZE": str(input_size), "SECRET_BITSTRING": str(decimal_value)}
