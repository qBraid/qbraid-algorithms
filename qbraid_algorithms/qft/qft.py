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

import numpy as np
import autoqasm as aq
import pyqasm
from autoqasm.instructions import h, cphaseshift, swap
from pyqasm.modules.base import QasmModule
from qbraid.transpiler.conversions.qasm3 import autoqasm_to_qasm3


def create_qft_prog(n_qubits: int) -> aq.Program:
    """
    AutoQASM wrapper function to create n-qubit QFT circuit.

    Args:
        n_qubits (int): Number of qubits for the QFT circuit.

    Returns:
        aq.Program: AutoQASM program implementing the QFT circuit.
    """
    # Pre-compute all necessary angle values
    unique_angles = []
    
    for j in range(1, n_qubits):
        divisor = 2 ** (j + 1)
        r_angle = float(2 * np.pi / divisor)
        unique_angles.append(r_angle)

    @aq.main(num_qubits=n_qubits)
    def qft():
        # Convert angles array to autoqasm type
        angles = aq.ArrayVar(unique_angles, base_type=aq.FloatVar)
        
        for i in aq.range(n_qubits):
            h(i)
            # Apply controlled phase shift gates to all qubits below i
            for j in aq.range(1, n_qubits - i):
                angle_idx = j - 1
                cphaseshift(i + j, i, angles[angle_idx])
        
        # Swap qubits to reverse order
        for i in aq.range(n_qubits // 2):
            swap(i, n_qubits - i - 1)

    return qft


def load_program(n_qubits: int) -> QasmModule:
    """
    Load the QFT circuit as a pyqasm module.

    Args:
        n_qubits (int): Number of qubits for the QFT circuit.
    
    Returns:
        pyqasm module containing the QFT circuit
    """
    program = create_qft_prog(n_qubits)
    qasm_str = autoqasm_to_qasm3(program)
    return pyqasm.loads(qasm_str)


def run_program(program: QasmModule, device, shots=100):
    """
    Run the QFT circuit on a specified device.
    
    Args:
        program (QasmModule): The QFT circuit to run.
        device: The quantum device to run the circuit on.
        shots (int): Number of shots for the execution.
    
    Returns:
        Result of the execution.
    """
    qasm_str = pyqasm.dumps(program)
    job = device.run(qasm_str, shots=shots)
    return job.result()