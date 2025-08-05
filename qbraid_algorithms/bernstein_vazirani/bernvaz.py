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
import tempfile
import shutil
from pathlib import Path
import pyqasm
from pyqasm.modules.base import QasmModule
from qbraid_algorithms.utils import _prep_qasm_file


def load_program(bitstring: str | list[int]) -> QasmModule:
    """
    Load the Bernstein-Vazirani circuit as a pyqasm module.

    Args:
        bitstring (str | list[int]): The hidden bitstring `s` as a string of '0's
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


def generate_subroutine(bitstring: str | list[int]) -> None:
    """
    Creates a Bernstein-Vazirani subroutine module with user-defined hidden bitstring
    within user's current working directory.
    Args:
        bitstring (str | list[int]): The hidden bitstring `s` as a string of
        '0's and '1's
    Returns:
        None
    """
    # Copy the B-V subroutine QASM file to the current working directory
    bernvaz_src = Path(__file__).parent / "bernvaz_subroutine.qasm"
    bernvaz_dst = os.path.join(os.getcwd(), "bernvaz.qasm")
    shutil.copy(bernvaz_src, bernvaz_dst)

    # Replace variable placeholders with user-defined parameters
    replacements = _generate_replacements(bitstring)
    _prep_qasm_file(bernvaz_dst, replacements)

    print(f"Subroutine 'bernvaz' has been added to {bernvaz_dst}")


def generate_oracle(bitstring: list[int]) -> None:
    """
    Creates an Bernstein-Vazirani oracle encoded with user-defined hidden bitstring
    within user's current working directory.

    Args:
        bitstring (list[int] | str): The hidden bitstring `s` as a string
        of '0's and '1's

    Returns:
        None
    """
    # Copy the oracle QASM file to the current working directory
    oracle_src = Path(__file__).parent / "oracle.qasm"
    oracle_dst = os.path.join(os.getcwd(), "oracle.qasm")
    shutil.copy(oracle_src, oracle_dst)

    # Replace variable placeholders with user-defined parameters
    replacements = _generate_replacements(bitstring)
    _prep_qasm_file(oracle_dst, replacements)

    print(f"Oracle 'oracle' has been added to {oracle_dst}")


def _convert_bitstring_decimal(bitstring: str | list[int]) -> int:
    """
    Converts a bitstring (str or list of int) to its decimal integer representation.

    Args:
        bitstring (str | list[int]): The hidden bitstring of '0's and '1's

    Returns:
        int: Decimal integer representation of the bitstring
    """
    if isinstance(bitstring, list):
        bitstring = "".join(str(b) for b in bitstring)
    # Reverse bitstring for correct qubit ordering
    bitstring_reversed = bitstring[::-1]
    return int(bitstring_reversed, 2)


def _generate_replacements(bitstring: str | list[int]) -> dict[str, str]:
    """
    Generates a dictionary of replacements for QASM variable placeholders.

    Args:
        bitstring (str | list[int]): The hidden bitstring of '0's and '1's

    Returns:
        dict[str, str]: Dictionary mapping variable names to their string values
    """
    input_size = len(bitstring)
    decimal_value = _convert_bitstring_decimal(bitstring)
    return {"BERNVAZ_SIZE": str(input_size), "SECRET_BITSTRING": str(decimal_value)}
