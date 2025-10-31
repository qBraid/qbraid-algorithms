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
Tests for Inverse Quantum Fourier Transform (IQFT) algorithm implementation.
"""
# pylint: disable=missing-function-docstring,too-many-locals,duplicate-code
from pathlib import Path

import pyqasm
from pyqasm.modules.base import QasmModule

from qbraid_algorithms import iqft

from .local_device import LocalDevice

RESOURCES_DIR = Path(__file__).parent / "resources" / "iqft"


def _run_circuit_and_check_counts(
    device, program_path, expected_counts, shots=1000, tolerance=0.1
):
    """Helper function to run a circuit and check the measurement counts."""
    program = pyqasm.load(program_path)
    program.unroll()
    program_str = pyqasm.dumps(program)
    result = device.run(program_str, shots=shots)
    counts = result.data.get_counts()

    error = tolerance * shots
    for state, count in counts.items():
        expected = expected_counts[state]
        lower = expected - error
        upper = expected + error
        assert lower <= count <= upper


def test_generate_program():
    """Test that generate_program correctly returns a pyqasm module object."""
    iqft_module = iqft.generate_program(3)
    assert isinstance(iqft_module, QasmModule)
    assert iqft_module.num_qubits == 3


def test_valid_circuit_0():
    """Test 1-qubit IQFT (Hadamard) yields ~uniform distribution over |0>, |1>."""
    # Single qubit QFT circuit should just be H gate
    device = LocalDevice()

    # Clean up any existing iqft.qasm file from previous tests
    iqft_file = RESOURCES_DIR / "iqft.qasm"
    if iqft_file.exists():
        iqft_file.unlink()

    # generate single qubit QFT circuit
    iqft.save_to_qasm(1, path=RESOURCES_DIR, quiet=True)
    program = pyqasm.load(f"{RESOURCES_DIR}/iqft_0.qasm")
    # delete the created subroutine file
    (RESOURCES_DIR / "iqft.qasm").unlink()
    # Unrolling is necessary for proper execution
    program.unroll()
    program_str = pyqasm.dumps(program)
    shots = 1000
    result = device.run(program_str, shots=shots)
    counts = result.data.get_counts()

    expected_counts = {"0": 500, "1": 500}
    tolerance = 0.1
    error = tolerance * shots
    for state, count in counts.items():
        expected = expected_counts[state]
        lower = expected - error
        upper = expected + error
        assert lower <= count <= upper


def test_valid_circuit_1():
    """Test 1-qubit IQFT starting from |1> yields ~uniform distribution."""
    # Single qubit QFT circuit should just be H gate
    device = LocalDevice()

    # Clean up any existing iqft.qasm file from previous tests
    iqft_file = RESOURCES_DIR / "iqft.qasm"
    if iqft_file.exists():
        iqft_file.unlink()

    # generate single qubit QFT circuit
    iqft.save_to_qasm(1, path=RESOURCES_DIR, quiet=True)
    program = pyqasm.load(f"{RESOURCES_DIR}/iqft_1.qasm")
    # delete the created subroutine file
    (RESOURCES_DIR / "iqft.qasm").unlink()
    # Unrolling is necessary for proper execution
    program.unroll()
    program_str = pyqasm.dumps(program)
    shots = 1000
    result = device.run(program_str, shots=shots)
    counts = result.data.get_counts()

    expected_counts = {"0": 500, "1": 500}
    tolerance = 0.1
    error = tolerance * shots
    for state, count in counts.items():
        expected = expected_counts[state]
        lower = expected - error
        upper = expected + error
        assert lower <= count <= upper


def test_valid_circuit_00():
    """Test 2-qubit IQFT starting from |00> state."""
    # we want to take in some binary number as a state - ie |00>
    device = LocalDevice()

    # Clean up any existing iqft.qasm file from previous tests
    iqft_file = RESOURCES_DIR / "iqft.qasm"
    if iqft_file.exists():
        iqft_file.unlink()

    # generate two qubit QFT circuit
    iqft.save_to_qasm(2, path=RESOURCES_DIR, quiet=True)
    program = pyqasm.load(f"{RESOURCES_DIR}/iqft_00.qasm")
    # delete the created subroutine file
    (RESOURCES_DIR / "iqft.qasm").unlink()
    # Unrolling is necessary for proper execution
    program.unroll()
    program_str = pyqasm.dumps(program)
    shots = 1000
    result = device.run(program_str, shots=shots)
    counts = result.data.get_counts()

    expected_counts = {"00": 250, "01": 250, "10": 250, "11": 250}
    tolerance = 0.1
    error = tolerance * shots
    for state, count in counts.items():
        expected = expected_counts[state]
        lower = expected - error
        upper = expected + error
        assert lower <= count <= upper


def test_valid_circuit_2qubit_superposition():
    """Test 2-qubit IQFT on equal superposition state."""
    # we want to take in some binary number as a state - ie 2 = |10>
    device = LocalDevice()

    # Clean up any existing iqft.qasm file from previous tests
    iqft_file = RESOURCES_DIR / "iqft.qasm"
    if iqft_file.exists():
        iqft_file.unlink()

    # generate two qubit QFT circuit
    iqft.save_to_qasm(2, path=RESOURCES_DIR, quiet=True)
    program = pyqasm.load(f"{RESOURCES_DIR}/iqft_2qubit_superposn.qasm")
    # delete the created subroutine file
    (RESOURCES_DIR / "iqft.qasm").unlink()
    # Unrolling is necessary for proper execution
    program.unroll()
    program_str = pyqasm.dumps(program)
    shots = 1000
    result = device.run(program_str, shots=shots)
    counts = result.data.get_counts()

    expected_counts = {"00": 1000, "01": 10, "10": 10, "11": 10}
    tolerance = 0.1
    error = tolerance * shots
    for state, count in counts.items():
        expected = expected_counts[state]
        lower = expected - error
        upper = expected + error
        assert lower <= count <= upper


def test_valid_circuit_000():
    # we want to take in some binary number as a state - ie |000>
    device = LocalDevice()

    # Clean up any existing iqft.qasm file from previous tests
    iqft_file = RESOURCES_DIR / "iqft.qasm"
    if iqft_file.exists():
        iqft_file.unlink()

    # generate three qubit QFT circuit
    iqft.save_to_qasm(3, path=RESOURCES_DIR, quiet=True)
    program = pyqasm.load(f"{RESOURCES_DIR}/iqft_000.qasm")
    # delete the created subroutine file
    (RESOURCES_DIR / "iqft.qasm").unlink()
    # Unrolling is necessary for proper execution
    program.unroll()
    program_str = pyqasm.dumps(program)
    shots = 1000
    result = device.run(program_str, shots=shots)
    counts = result.data.get_counts()
    value = shots / 8
    expected_counts = {
        "000": value,
        "001": value,
        "010": value,
        "011": value,
        "100": value,
        "101": value,
        "110": value,
        "111": value,
    }

    tolerance = 0.1
    error = tolerance * shots
    for state, count in counts.items():
        expected = expected_counts[state]
        lower = expected - error
        upper = expected + error
        assert lower <= count <= upper


def test_valid_circuit_010():
    # we want to take in some binary number as a state - ie |010>
    device = LocalDevice()

    # Clean up any existing iqft.qasm file from previous tests
    iqft_file = RESOURCES_DIR / "iqft.qasm"
    if iqft_file.exists():
        iqft_file.unlink()

    # generate three qubit QFT circuit
    iqft.save_to_qasm(3, path=RESOURCES_DIR, quiet=True)
    program = pyqasm.load(f"{RESOURCES_DIR}/iqft_010.qasm")
    # delete the create
    # d subroutine file
    (RESOURCES_DIR / "iqft.qasm").unlink()
    # Unrolling is necessary for proper execution
    program.unroll()
    program_str = pyqasm.dumps(program)
    shots = 1000
    result = device.run(program_str, shots=shots)
    counts = result.data.get_counts()
    value = shots / 8
    expected_counts = {
        "000": value,
        "001": value,
        "010": value,
        "011": value,
        "100": value,
        "101": value,
        "110": value,
        "111": value,
    }

    tolerance = 0.1
    error = tolerance * shots
    for state, count in counts.items():
        expected = expected_counts[state]
        lower = expected - error
        upper = expected + error
        assert lower <= count <= upper


def test_valid_circuit_001():
    # we want to take in some binary number as a state - ie |001>
    device = LocalDevice()

    # Clean up any existing iqft.qasm file from previous tests
    iqft_file = RESOURCES_DIR / "iqft.qasm"
    if iqft_file.exists():
        iqft_file.unlink()

    # generate three qubit QFT circuit
    iqft.save_to_qasm(3, path=RESOURCES_DIR, quiet=True)
    program = pyqasm.load(f"{RESOURCES_DIR}/iqft_001.qasm")
    # delete the created subroutine file
    (RESOURCES_DIR / "iqft.qasm").unlink()
    # Unrolling is necessary for proper execution
    program.unroll()
    program_str = pyqasm.dumps(program)
    shots = 1000
    result = device.run(program_str, shots=shots)
    counts = result.data.get_counts()
    value = shots / 8
    expected_counts = {
        "000": value,
        "001": value,
        "010": value,
        "011": value,
        "100": value,
        "101": value,
        "110": value,
        "111": value,
    }

    tolerance = 0.1
    error = tolerance * shots
    for state, count in counts.items():
        expected = expected_counts[state]
        lower = expected - error
        upper = expected + error
        assert lower <= count <= upper
