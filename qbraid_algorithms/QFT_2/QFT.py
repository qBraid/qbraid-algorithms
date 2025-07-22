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
Quantum Fourier Transform (QFT) implementation using AutoQASM.

This implementation is parameterized by the number of qubits and outputs the circuit as a Qasm3Module.
"""

import autoqasm as aq
import numpy as np
import pyqasm
from autoqasm.instructions import cphaseshift, h, swap

# from qbraid.transpiler.conversions.qasm3 import autoqasm_to_qasm3

Qasm3Module = pyqasm.modules.qasm3.Qasm3Module


def QFT(qubits: int |list,swaps: bool = True):
    """
    AutoQASM closure wrapper to create n-qubit QFT circuit.
    Note: implementation currently expects little endian qubit order

    Args:
        qubits (int | list[int ]) : Number of qubits for the QFT circuit, or list of qubit indices
        swaps (bool): indicate whether the final set of swaps is needed (if a final element in a circuit, classical bit reordering is more efficient and conserves fidelity)
    Returns: 
        autoqasm closure applying qft on provided qubits
    """
    if qubits is None or not isinstance(qubits,(int,list)):
        raise TypeError(f"Generator cannot accept {type(qubits)} as qubit arguument")
    elif isinstance(qubits, int) and qubits <1:
        raise ValueError("number of qubits must be a positive nonzero integer")
    
    indexing = [*range(qubits)] if isinstance(qubits,int) else qubits
    n_qubits = len(indexing)
    # predefining phases which are of order reducing powers of 2
    phases = np.pi/np.exp2(np.arange(n_qubits-1))
    
    @aq.subroutine()
    def qft_module():                #module function to define QFT circuit with respect to number of qubits
        #iter over all qubits from lsb to msb
        for i in range(n_qubits):
            h(indexing[i])
            for j in range(n_qubits-i-1):
                cphaseshift(indexing[i+j+1],indexing[i],phases[j])
        #insert final swaps for bits
        if swaps:
            for i in range(n_qubits//2):
                swap(indexing[i],indexing[qubits-i-1])

    return qft_module


def QFT_Demo(qubits: int):
    @aq.main(num_qubits=qubits)
    def qft_main():
        QFT(qubits)()
    return qft_main.build().to_ir()



    


