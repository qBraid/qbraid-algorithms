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

import autoqasm as aq
import pyqasm
from autoqasm.instructions import cnot, h, measure, x
from qbraid.transpiler.conversions.qasm3 import autoqasm_to_qasm3

Qasm3Module = pyqasm.modules.qasm3.Qasm3Module


# Secret string
s = "11010" # TODO: let user specify secret string


@aq.subroutine
def oracle():
    """
    Subroutine to implement oracle of Bernstein-Vazirani algorithm.
    Currently implements oracle for fixed hidden string '11010'.
    """
    cnot(0, 5)
    cnot(1, 5)
    cnot(3, 5)

@aq.subroutine
def measure_qubits():
    """
    Subroutine to measure the qubits.
    """
    for i in range(5):
        measure(i)

@aq.subroutine
def prep_ancilla():
    """
    Subroutine to prepare the ancilla qubit.
    """
    x(6)
    h(6)

@aq.main(num_qubits=6)
def bernstein_vazirani():
    """
    Bernstein-Vazirani Algorithm Implementation for hidden string `s`.
    """    
    # Initialize input qubits to |+> state
    for i in range(4):
        h(i)
    # Prepare ancilla qubit
    prep_ancilla()
    oracle()
    # Re-apply Hadamard gates to input qubits
    for i in range(4):
        h(i)
    # Measure input qubits
    measure_qubits()

def load_program() -> Qasm3Module:
    """
    Load the Bernstein-Vazirani circuit as a pyqasm module.
    
    Returns:
        pyqasm module containing the Bernstein-Vazirani circuit
    """
    program = bernstein_vazirani.build()
    qasm_str = autoqasm_to_qasm3(program)
    return pyqasm.loads(qasm_str)
