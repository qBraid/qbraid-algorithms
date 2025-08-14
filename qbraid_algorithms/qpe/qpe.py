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
Module providing Quantum Phase Estimation algorithm implementation.

"""
import os
import tempfile
import shutil
from pathlib import Path

import pyqasm
from openqasm3 import dumps
from openqasm3.ast import QuantumGateDefinition
from pyqasm.modules.base import QasmModule

from qbraid_algorithms import iqft
from qbraid_algorithms.utils import _prep_qasm_file


def load_program(
    unitary_filepath: str,
    psi_filepath: str,
    num_qubits: int = 4,
    include_measurement=True,
) -> QasmModule:
    """
    Load the Quantum Phase Estimation (QPE) program as a pyqasm module.

    Args:
        num_qubits : int
            Number of qubits to use for the phase estimation register.
        unitary_filepath : str
            Path to a qasm file defining the unitary gate U.
        psi_filepath : str
            Path to a qasm file defining the eigenstate preparation gate.
        include_measurement : bool
            If True, includes measurement operations in the returned QPE circuit.

    Returns:
        (PyQasm Module) pyqasm module containing the QPE circuit
    """
    # Load the QPE QASM files into a staging directory
    temp_dir = tempfile.mkdtemp()
    qpe_src = Path(__file__).parent / "qpe.qasm"
    qpe_sub_src = Path(__file__).parent / "qpe_subroutine.qasm"
    qpe_dst = os.path.join(temp_dir, "qpe.qasm")
    qpe_sub_dst = os.path.join(temp_dir, "qpe_subroutine.qasm")
    shutil.copy(qpe_src, qpe_dst)
    shutil.copy(qpe_sub_src, qpe_sub_dst)
    iqft.generate_subroutine(num_qubits, quiet=True, path=temp_dir)
    # Get the string defining the custom gate and its controlled version
    custom_gate_str = _get_unitary(unitary_filepath)
    # Get the string defining the eigenstate preparation gate
    psi = "" if psi_filepath is None else _get_psi(psi_filepath)
    replacements = {
        "QPE_SIZE": str(num_qubits),
        "CUSTOM_GATE_DEFS": custom_gate_str,
        "PREP_EIGENSTATE": psi,
    }
    if not include_measurement:
        replacements["b = measure q;"] = ""  # remove measurement line

    _prep_qasm_file(qpe_dst, replacements)
    _prep_qasm_file(qpe_sub_dst, replacements)

    # Load the algorithm as a pyqasm module
    module = pyqasm.load(qpe_dst)

    return module


def generate_subroutine(
    unitary_filepath: str, num_qubits: int = 4, quiet: bool = False, path: str = None
) -> None:
    """
    Creates a QPE subroutine module with user-defined unitary and number of qubits.

    Args:
        unitary_filepath : str
            Path to a qasm file defining the unitary gate U.
        num_qubits : int
            Number of qubits to use for the phase estimation register.
        quiet (bool): If True, suppresses output messages.
        path (str): The directory path where the QPE subroutine will be created.
                   If None, creates in the current working directory.

    Returns:
        None
    """
    # Copy the QPE subroutine QASM file to the specified or current working directory
    qpe_src = Path(__file__).parent / "qpe_subroutine.qasm"
    if path is None:
        qpe_dst = os.path.join(os.getcwd(), "qpe.qasm")
    else:
        qpe_dst = os.path.join(path, "qpe.qasm")
    shutil.copy(qpe_src, qpe_dst)
    iqft.generate_subroutine(num_qubits, quiet=True, path=path)
    # Get the string defining the custom gate and its controlled version
    custom_gate_str = _get_unitary(unitary_filepath)
    # Replace variable placeholders with user-defined parameters
    replacements = {"QPE_SIZE": str(num_qubits), "CUSTOM_GATE_DEFS": custom_gate_str}
    _prep_qasm_file(qpe_dst, replacements)
    if not quiet:
        print(f"Subroutine 'qpe' has been added to {qpe_dst}")


def get_result(counts: dict[str, int]) -> float:
    """
    Extract the eigenvalue from Quantum Phase Estimation measurement counts.

    This function processes the measurement results from a QPE circuit to extract
    the estimated eigenvalue. It finds the most frequently measured bitstring,
    converts it to a decimal value, and normalizes it to get the eigenvalue estimate.

    Args:
        counts (dict[str, int]): Dictionary mapping measurement outcomes (bitstrings)
                                to their occurrence counts from the QPE circuit.

    Returns:
        float: The estimated eigenvalue as a fraction between 0 and 1.
               This represents the phase φ where the eigenvalue is e^(2πiφ).
    """
    # Get most frequent bitstring from counts
    bitstring = max(counts, key=counts.get)
    # Convert the result bitstring into a decimal integer
    decimal = int(bitstring, 2)
    # Divide by 2^n to get the fractional phase estimate
    result = decimal / (2 ** len(bitstring))
    return result


def _get_unitary(filepath: str) -> str:
    """
    Given a filepath to a qasm file defining a custom gate, create a controlled
    version of that gate, and return the combined string defing both the original gate
    and the controlled version.

    Note: Currently assumes U is a single-qubit unitary gate.

    Parameters:
    filepath : str
        Path to the qasm file defining the custom gate.

    Returns: str
        QASM string defining both the original gate and its controlled version.
    """
    module = pyqasm.load(filepath)
    # We assume the first custom gate definition is U
    statements = module._statements  # pylint: disable=protected-access
    gate_defs = [s for s in statements if isinstance(s, QuantumGateDefinition)]
    if not gate_defs:
        raise ValueError("No gate definitions found in the provided QASM file.")
    # Assume the first gate definition is the unitary U
    u = gate_defs[0]
    gate_str = dumps(u)
    gate_name = u.name.name
    # Create controlled version of the gate
    c_u = f"gate CU a, b {{\n  ctrl @ {gate_name} a, b;\n}}\n"
    # Create string for original gate and its controlled referenced version
    combined = gate_str + "\n" + c_u

    return combined


def _get_psi(filepath: str) -> str:
    """
    Given a filepath to a qasm file defining a custom gate to prepare the eigenstate,
    return the string defining that gate.

    Parameters:
    filepath : str
        Path to the qasm file defining the custom gate.

    Returns: str
        QASM string defining the eigenstate preparation gate.
    """
    module = pyqasm.load(filepath)
    # We assume the first custom gate definition is the eigenstate prep gate
    statements = module._statements  # pylint: disable=protected-access
    gate_defs = [s for s in statements if isinstance(s, QuantumGateDefinition)]
    if not gate_defs:
        raise ValueError("No gate definitions found in the provided QASM file.")
    # Assume the first gate definition is the eigenstate prep gate
    prep_gate = gate_defs[0]
    # replace gate name with "prep_eigenstate"
    prep_gate.name.name = "prep_eigenstate"
    gate_str = dumps(prep_gate)
    return gate_str
