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
Tests for Bernstein-Vazirani algorithm implementation.
"""
import io
import os
import sys
import tempfile
from pathlib import Path

import pyqasm
from pyqasm.modules.base import QasmModule

from qbraid_algorithms import bernstein_vazirani as bv
from qbraid_algorithms.utils import get_max_count

from .local_device import LocalDevice


def test_load_program():
    """Test that load_program correctly returns a pyqasm module object."""
    bv_module = bv.load_program("101")
    assert isinstance(bv_module, QasmModule)
    assert bv_module.num_qubits == 4 # 3 data qubits + 1 ancilla qubit


def test_generate_subroutine():
    """Test that generate_subroutine correctly generates the subroutine QASM."""
    s = "101"
    with tempfile.TemporaryDirectory() as test_dir:
        bv.generate_subroutine(s, quiet=True, path=test_dir)
        # Ensure the file was created
        subroutine_qasm = Path(test_dir) / "bernvaz.qasm"
        assert subroutine_qasm.exists()


def test_generate_subroutine_default_path():
    """Test generate_subroutine with default path (current working directory)."""
    s = "101"
    original_cwd = os.getcwd()
    # Create temporary directory and change to it
    with tempfile.TemporaryDirectory() as test_dir:
        os.chdir(test_dir)
        try:
            bv.generate_subroutine(s, quiet=True, path=None)
            # Ensure the file was created in current directory
            subroutine_qasm = Path(test_dir) / "bernvaz.qasm"
            assert subroutine_qasm.exists()
        finally:
            # Restore original working directory
            os.chdir(original_cwd)


def test_generate_subroutine_verbose():
    """Test generate_subroutine with verbose output (quiet=False)."""
    s = "101"
    with tempfile.TemporaryDirectory() as test_dir:
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        try:
            bv.generate_subroutine(s, quiet=False, path=test_dir)
            # Get the captured output
            output = captured_output.getvalue()
            # Ensure the verbose message was printed
            assert "Subroutine 'bernvaz' has been added to" in output
            assert "bernvaz.qasm" in output
            # Ensure the file was created
            subroutine_qasm = Path(test_dir) / "bernvaz.qasm"
            assert subroutine_qasm.exists()
        finally:
            # Restore stdout
            sys.stdout = sys.__stdout__


def test_generate_oracle():
    """Test that generate_oracle correctly generates the oracle QASM."""
    s = "101"
    with tempfile.TemporaryDirectory() as test_dir:
        bv.generate_oracle(s, quiet=True, path=test_dir)
        # Ensure the file was created
        oracle_qasm = Path(test_dir) / "oracle.qasm"
        assert oracle_qasm.exists()


def test_generate_oracle_default_path():
    """Test generate_oracle with default path (current working directory)."""
    s = "101"
    original_cwd = os.getcwd()
    # Create temporary directory and change to it
    with tempfile.TemporaryDirectory() as test_dir:
        os.chdir(test_dir)
        try:
            bv.generate_oracle(s, quiet=True, path=None)
            # Ensure the file was created in current directory
            oracle_qasm = Path(test_dir) / "oracle.qasm"
            assert oracle_qasm.exists()
        finally:
            # Restore original working directory
            os.chdir(original_cwd)


def test_generate_oracle_verbose():
    """Test generate_oracle with verbose output (quiet=False)."""
    s = "101"
    with tempfile.TemporaryDirectory() as test_dir:
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        try:
            bv.generate_oracle(s, quiet=False, path=test_dir)
            # Get the captured output
            output = captured_output.getvalue()
            # Ensure the verbose message was printed
            assert "Oracle 'oracle' has been added to" in output
            assert "oracle.qasm" in output
            # Ensure the file was created
            oracle_qasm = Path(test_dir) / "oracle.qasm"
            assert oracle_qasm.exists()
        finally:
            # Restore stdout
            sys.stdout = sys.__stdout__


def test_algorithm_101():
    """Test the Bernstein-Vazirani algorithm implementation for the input '101'."""
    s = "101"
    device = LocalDevice()
    module = bv.load_program(s)
    # Unrolling is necessary for proper execution
    module.unroll()
    program_str = pyqasm.dumps(module)
    result = device.run(program_str, shots=1000)
    counts = result.data.get_counts()
    max_str, _ = get_max_count(counts)
    assert max_str == s


def test_algorithm_10101():
    """Test the Bernstein-Vazirani algorithm implementation for the input '10101'."""
    s = "10101"
    device = LocalDevice()
    module = bv.load_program(s)
    # Unrolling is necessary for proper execution
    module.unroll()
    program_str = pyqasm.dumps(module)
    result = device.run(program_str, shots=1000)
    counts = result.data.get_counts()
    max_str, _ = get_max_count(counts)
    assert max_str == s
