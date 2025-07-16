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
Oracle agnostic amplitude amplification implementation

Parameterized by number of qubits, and optional oracle and outputting as a qasm3Module
"""

import autoqasm as aq
import pyqasm
import numpy as np
from autoqasm.instructions import cphaseshift, h, swap
from qbraid.transpiler.conversions.qasm3 import autoqasm_to_qasm3

Qasm3Module = pyqasm.modules.qasm3.Qasm3Module


def Amplification(n_qubits: int,depth: int,oracle = None)->Qasm3Module:
    """
    AutoQASM closure wrapper to create n-qubit QFT circuit.
    Note: implementation currently expects little endian qubit order

    Args:
        n_qubits (int): Number of qubits for the QFT circuit.
        depth (int): number of amplification iterations
        oracle: blind function aq subroutine expecting range of qubits to apply to
    Returns:
        Qasm3Module: qBraid native representation of OpenQASM3 circuits
    """
    if n_qubits is None or n_qubits <1:
        raise ValueError(f"n_qubits {n_qubits} is not a valid positive integer")
    
    @aq.subroutine
    def Z0():
        [h(i) for i in aq.range(n_qubits)]  
        

    @aq.main(num_qubits=n_qubits)
    def ampl_module():
        [h(i) for i in aq.range(n_qubits)]            
        for i in aq.Range(depth):
            oracle(aq.range(n_qubits))


    qft = qft_module.build()
    return autoqasm_to_qasm3(qft)


    


