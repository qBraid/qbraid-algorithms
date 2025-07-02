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
from autoqasm import Qubit
from autoqasm.instructions import h, cphaseshift, swap
from autoqasm.types import FloatVar
from pyqasm.modules.base import QasmModule
from qbraid.transpiler.conversions.qasm3 import autoqasm_to_qasm3
from autoqasm.program.program import MainProgram
# We will start with a 5-qubit QFT example

def create_qft_prog(n_qubits: int) -> MainProgram:
    angles_by_i = []

    for i in range(n_qubits):
        angles_for_i = []
        for j in range(1, n_qubits - i):
            divisor = 2 ** (j + 1)
            r_angle = float(2 * np.pi / divisor)
            angles_for_i.append(r_angle)
        angles_by_i.append(angles_for_i)

    @aq.main(num_qubits=n_qubits)
    def qft():
        for i in aq.range(n_qubits):
            h(i)
            for j, r_angle in enumerate(angles_by_i[i], start=1):
                cphaseshift(i + j, i, r_angle)
        for i in aq.range(n_qubits // 2):
            swap(i, n_qubits - i - 1)

    return qft


def load_program(n_qubits: int) -> QasmModule:
    """
    Load the QFT circuit as a pyqasm module.
    
    Returns:
        pyqasm module containing the QFT circuit
    """
    program = create_qft_prog(n_qubits)
    qasm_str = autoqasm_to_qasm3(program)
    return pyqasm.loads(qasm_str)
