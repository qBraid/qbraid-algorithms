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
Tests for Quantum Phase Estimation (QPE) algorithm implementation.
"""
import io
import os
import sys
import tempfile
from pathlib import Path

import pyqasm
from pyqasm.modules.base import QasmModule
import pytest

from qbraid_algorithms import qpe
from qbraid_algorithms.qpe.qpe import _get_unitary, _get_psi

from .local_device import LocalDevice

RESOURCE_DIR = Path(__file__).parent / "resources" / "qpe"

def test_load_program():
    """Test that load_program correctly returns a pyqasm module object."""
    qpe_module = qpe.load_program(
        unitary_filepath = f"{RESOURCE_DIR}/t.qasm",
        psi_filepath = f"{RESOURCE_DIR}/prepare_state.qasm",
        num_qubits = 3,
    )
    assert isinstance(qpe_module, QasmModule)

def test_valid_circuit_r_3pi4():
    """Test QPE with r_3pi4 unitary."""
    # Clean up any existing qpe.qasm file from previous test runs
    qpe_file = RESOURCE_DIR / "qpe.qasm"
    if qpe_file.exists():
        qpe_file.unlink()
    device = LocalDevice()
    qpe.generate_subroutine(
        unitary_filepath = f"{RESOURCE_DIR}/r_3pi4.qasm",
        num_qubits = 3,
        quiet = True,
        path = RESOURCE_DIR
    )
    program = pyqasm.load(f"{RESOURCE_DIR}/qpe_3.qasm")
    # delete the created subroutine file
    (RESOURCE_DIR / "qpe.qasm").unlink()
    # Unrolling is necessary for proper execution
    program.unroll()
    program_str = pyqasm.dumps(program)
    result = device.run(program_str, shots=10000)
    counts = result.data.get_counts()
    result = qpe.get_result(counts)
    expected = 3 / 8
    assert result == expected


def test_valid_circuit_t():
    """Test QPE with t unitary."""
    # Clean up any existing qpe.qasm file from previous test runs
    qpe_file = RESOURCE_DIR / "qpe.qasm"
    if qpe_file.exists():
        qpe_file.unlink()
    iqft_file = RESOURCE_DIR / "iqft.qasm"
    if iqft_file.exists():
        iqft_file.unlink()
    device = LocalDevice()
    qpe.generate_subroutine(
        unitary_filepath = f"{RESOURCE_DIR}/t.qasm",
        num_qubits = 3,
        quiet = True,
        path = RESOURCE_DIR
    )
    program = pyqasm.load(f"{RESOURCE_DIR}/qpe_3.qasm")
    # delete the created subroutine file
    (RESOURCE_DIR / "qpe.qasm").unlink()
    # delete the created iqft file
    (RESOURCE_DIR / "iqft.qasm").unlink()
    # Unrolling is necessary for proper execution
    program.unroll()
    program_str = pyqasm.dumps(program)
    result = device.run(program_str, shots=10000)
    counts = result.data.get_counts()
    result = qpe.get_result(counts)
    expected = 1 / 8
    assert result == expected


def test_valid_circuit_z():
    """Test QPE with Z gate."""
    # Clean up any existing qpe.qasm file from previous test runs
    qpe_file = RESOURCE_DIR / "qpe.qasm"
    if qpe_file.exists():
        qpe_file.unlink()
    iqft_file = RESOURCE_DIR / "iqft.qasm"
    if iqft_file.exists():
        iqft_file.unlink()
    device = LocalDevice()
    qpe.generate_subroutine(
        unitary_filepath = f"{RESOURCE_DIR}/z.qasm",
        num_qubits = 3,
        quiet = True,
        path = RESOURCE_DIR
    )
    program = pyqasm.load(f"{RESOURCE_DIR}/qpe_3.qasm")
    # delete the created subroutine file
    (RESOURCE_DIR / "qpe.qasm").unlink()
    # delete the created iqft file
    (RESOURCE_DIR / "iqft.qasm").unlink()
    # Unrolling is necessary for proper execution
    program.unroll()
    program_str = pyqasm.dumps(program)
    result = device.run(program_str, shots=10000)
    counts = result.data.get_counts()
    result = qpe.get_result(counts)
    expected = 0.5
    assert result == expected


def test_load_program_without_measurement():
    """Test load_program with include_measurement=False."""
    qpe_module = qpe.load_program(
        unitary_filepath=f"{RESOURCE_DIR}/t.qasm",
        psi_filepath=f"{RESOURCE_DIR}/prepare_state.qasm",
        num_qubits=3,
        include_measurement=False
    )
    assert isinstance(qpe_module, QasmModule)


def test_generate_subroutine_default_path():
    """Test generate_subroutine with default path (current working directory)."""
    original_cwd = os.getcwd()
    # Create temporary directory and change to it
    with tempfile.TemporaryDirectory() as test_dir:
        os.chdir(test_dir)
        try:
            qpe.generate_subroutine(
                unitary_filepath=f"{RESOURCE_DIR}/t.qasm",
                num_qubits=3,
                quiet=True,
                path=None
            )
            # Ensure the file was created in current directory
            qpe_qasm = Path(test_dir) / "qpe.qasm"
            iqft_qasm = Path(test_dir) / "iqft.qasm"
            assert qpe_qasm.exists()
            assert iqft_qasm.exists()
        finally:
            # Restore original working directory
            os.chdir(original_cwd)


def test_generate_subroutine_verbose():
    """Test generate_subroutine with verbose output (quiet=False)."""
    with tempfile.TemporaryDirectory() as test_dir:
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        try:
            qpe.generate_subroutine(
                unitary_filepath=f"{RESOURCE_DIR}/t.qasm",
                num_qubits=3,
                quiet=False,
                path=test_dir
            )
            # Get the captured output
            output = captured_output.getvalue()
            # Ensure the verbose message was printed
            assert "Subroutine 'qpe' has been added to" in output
            assert "qpe.qasm" in output
            # Ensure the files were created
            qpe_qasm = Path(test_dir) / "qpe.qasm"
            iqft_qasm = Path(test_dir) / "iqft.qasm"
            assert qpe_qasm.exists()
            assert iqft_qasm.exists()
        finally:
            # Restore stdout
            sys.stdout = sys.__stdout__


def test_get_unitary_invalid_file():
    """Test _get_unitary with invalid QASM file (no gate definitions)."""
    with tempfile.TemporaryDirectory() as test_dir:
        # Create an invalid QASM file with no gate definitions
        invalid_file = Path(test_dir) / "invalid.qasm"
        invalid_file.write_text("""OPENQASM 3.0;
include "stdgates.inc";

// This file has no gate definitions
qubit[1] q;
h q[0];
""")
        with pytest.raises(ValueError, match="No gate definitions found in the provided QASM file"):
            _get_unitary(str(invalid_file))


def test_get_psi_invalid_file():
    """Test _get_psi with invalid QASM file (no gate definitions)."""
    with tempfile.TemporaryDirectory() as test_dir:
        # Create an invalid QASM file with no gate definitions
        invalid_file = Path(test_dir) / "invalid.qasm"
        invalid_file.write_text("""OPENQASM 3.0;
include "stdgates.inc";

// This file has no gate definitions
qubit[1] q;
x q[0];
""")
        with pytest.raises(ValueError, match="No gate definitions found in the provided QASM file"):
            _get_psi(str(invalid_file))
