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
Tests for Quantum Fourier Transform (QFT) algorithm implementation.
"""
# pylint: disable=missing-function-docstring,too-many-locals,duplicate-code
from pathlib import Path

import pyqasm
from pyqasm.modules.base import QasmModule

from qbraid_algorithms import iqft, qft

from .local_device import LocalDevice

RESOURCES_DIR = Path(__file__).parent / "resources" / "qft"


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


def test_load_program():
    """Test that load_program correctly returns a pyqasm module object."""
    qft_module = qft.load_program(3)
    assert isinstance(qft_module, QasmModule)
    assert qft_module.num_qubits == 3


def test_generate_subroutine():
    """Placeholder test for QFT generate_subroutine (to be implemented)."""
    # TODO: Implement this test
    assert True  # Placeholder assertion


def test_valid_circuit_0():
    """Test 1-qubit QFT (Hadamard) yields ~uniform distribution over |0>, |1>."""
    # Clean up any existing qft.qasm file from previous test runs
    qft_file = RESOURCES_DIR / "qft.qasm"
    if qft_file.exists():
        qft_file.unlink()

    # Single qubit QFT circuit should just be H gate
    device = LocalDevice()
    # generate single qubit QFT circuit
    qft.generate_subroutine(1, path=RESOURCES_DIR, quiet=True)
    program = pyqasm.load(f"{RESOURCES_DIR}/qft_0.qasm")
    # delete the created subroutine file
    (RESOURCES_DIR / "qft.qasm").unlink()
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
    """Test 1-qubit QFT starting from |1> yields ~uniform distribution."""
    # Clean up any existing qft.qasm file from previous test runs
    qft_file = RESOURCES_DIR / "qft.qasm"
    if qft_file.exists():
        qft_file.unlink()

    # Single qubit QFT circuit should just be H gate
    device = LocalDevice()
    # generate single qubit QFT circuit
    qft.generate_subroutine(1, path=RESOURCES_DIR, quiet=True)
    program = pyqasm.load(f"{RESOURCES_DIR}/qft_1.qasm")
    # delete the created subroutine file
    (RESOURCES_DIR / "qft.qasm").unlink()
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
    """Test 2-qubit QFT on |00> gives ~uniform distribution over 4 states."""
    # we want to take in some binary number as a state - ie |00>
    device = LocalDevice()
    # generate two qubit QFT circuit
    qft.generate_subroutine(2, path=RESOURCES_DIR, quiet=True)
    program = pyqasm.load(f"{RESOURCES_DIR}/qft_00.qasm")
    # delete the created subroutine file
    (RESOURCES_DIR / "qft.qasm").unlink()
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
    """Test 2-qubit QFT on prepared superposition state meets expected counts."""
    # we want to take in some binary number as a state - ie 2 = |10>
    device = LocalDevice()
    # generate two qubit QFT circuit
    qft.generate_subroutine(2, path=RESOURCES_DIR, quiet=True)
    program = pyqasm.load(f"{RESOURCES_DIR}/qft_2qubit_superposn.qasm")
    # delete the created subroutine file
    (RESOURCES_DIR / "qft.qasm").unlink()
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


def test_valid_circuit_01():
    """Test 2-qubit QFT on |01> gives ~uniform distribution after transform."""
    # we want to take in some binary number as a state - ie |01>
    device = LocalDevice()
    # generate two qubit QFT circuit
    qft.generate_subroutine(2, path=RESOURCES_DIR, quiet=True)
    program = pyqasm.load(f"{RESOURCES_DIR}/qft_01.qasm")
    # delete the created subroutine file
    (RESOURCES_DIR / "qft.qasm").unlink()
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


def test_valid_circuit_000():
    """Test 3-qubit QFT on |000> yields ~uniform distribution over 8 states."""
    # we want to take in some binary number as a state - ie |000>
    device = LocalDevice()
    # generate three qubit QFT circuit
    qft.generate_subroutine(3, path=RESOURCES_DIR, quiet=True)
    program = pyqasm.load(f"{RESOURCES_DIR}/qft_000.qasm")
    # delete the created subroutine file
    (RESOURCES_DIR / "qft.qasm").unlink()
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
    """Test 3-qubit QFT on |010> yields ~uniform distribution over 8 states."""
    # we want to take in some binary number as a state - ie |010>
    device = LocalDevice()
    # generate three qubit QFT circuit
    qft.generate_subroutine(3, path=RESOURCES_DIR, quiet=True)
    program = pyqasm.load(f"{RESOURCES_DIR}/qft_010.qasm")
    # delete the created subroutine file
    (RESOURCES_DIR / "qft.qasm").unlink()
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
    """Test 3-qubit QFT on |001> yields ~uniform distribution over 8 states."""
    # we want to take in some binary number as a state - ie 3 = |011>
    device = LocalDevice()
    # generate two qubit QFT circuit
    qft.generate_subroutine(3, path=RESOURCES_DIR, quiet=True)
    program = pyqasm.load(f"{RESOURCES_DIR}/qft_001.qasm")
    # delete the created subroutine file
    (RESOURCES_DIR / "qft.qasm").unlink()
    # Unrolling is necessary for proper execution
    program.unroll()
    program_str = pyqasm.dumps(program)
    shots = 1000
    result = device.run(program_str, shots=shots)
    counts = result.data.get_counts()
    value = 1000 / 8
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


def test_undo_iqft_00():
    """Test that QFT followed by IQFT on |00> returns original state |00>.

    Undo IQFT using QFT
    """
    device = LocalDevice()

    qft_file = RESOURCES_DIR / "qft.qasm"
    if qft_file.exists():
        qft_file.unlink()

    iqft_file = RESOURCES_DIR / "iqft.qasm"
    if iqft_file.exists():
        iqft_file.unlink()
    qft.generate_subroutine(2, path=RESOURCES_DIR, quiet=True)
    iqft.generate_subroutine(2, path=RESOURCES_DIR, quiet=True)
    program = pyqasm.load(f"{RESOURCES_DIR}/undo_iqft_00.qasm")
    (RESOURCES_DIR / "qft.qasm").unlink()
    (RESOURCES_DIR / "iqft.qasm").unlink()

    program.unroll()
    program_str = pyqasm.dumps(program)
    result = device.run(program_str, shots=1000)
    counts = result.data.get_counts()
    expected_counts = {"00": 1000, "01": 0, "10": 0, "11": 0}
    tolerance = 0.1
    error = tolerance * 1000
    for state, count in counts.items():
        expected = expected_counts[state]
        lower = expected - error
        upper = expected + error
        assert lower <= count <= upper


def test_undo_iqft_superposition():
    """Test that QFT then IQFT on equal superposition returns superposition.

    Undo IQFT using QFT
    """
    device = LocalDevice()

    qft_file = RESOURCES_DIR / "qft.qasm"
    if qft_file.exists():
        qft_file.unlink()

    iqft_file = RESOURCES_DIR / "iqft.qasm"
    if iqft_file.exists():
        iqft_file.unlink()
    qft.generate_subroutine(2, path=RESOURCES_DIR, quiet=True)
    iqft.generate_subroutine(2, path=RESOURCES_DIR, quiet=True)
    program = pyqasm.load(f"{RESOURCES_DIR}/undo_iqft_00_superposition.qasm")
    (RESOURCES_DIR / "qft.qasm").unlink()
    (RESOURCES_DIR / "iqft.qasm").unlink()

    program.unroll()
    program_str = pyqasm.dumps(program)
    result = device.run(program_str, shots=1000)
    counts = result.data.get_counts()
    expected_counts = {"00": 250, "01": 250, "10": 250, "11": 250}
    tolerance = 0.1
    error = tolerance * 1000
    for state, count in counts.items():
        expected = expected_counts[state]
        lower = expected - error
        upper = expected + error
        assert lower <= count <= upper
