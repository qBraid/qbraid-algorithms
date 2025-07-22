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

from typing import Union

import autoqasm as aq
import numpy as np
import pyqasm
from autoqasm.instructions import cphaseshift, h, swap

# from qbraid.transpiler.conversions.qasm3 import autoqasm_to_qasm3

Qasm3Module = pyqasm.modules.qasm3.Qasm3Module


def QFT(n_qubits: Union[int,list[int]]):
    """
    AutoQASM closure wrapper to create n-qubit QFT circuit.
    Note: implementation currently expects little endian qubit order

    Args:
        n_qubits (int): Number of qubits for the QFT circuit.

    Returns:
        autoqasm closure applying qft on provided qubits
    """
    if n_qubits is None or n_qubits <1:
        raise ValueError(f"n_qubits {n_qubits} is not a valid positive integer")
    
    # predefining phases which are of oreder reducing powers of 2
    phases = np.pi/np.exp2(np.arange(n_qubits-1))
    
    @aq.main(num_qubits=n_qubits)
    def qft_module():                #module function to define QFT circuit with respect to number of qubits
        #type conversion to autoqasm native arrays
        angles = aq.arrayVar(phases)
        
        #iter over all qubits from lsb to msb
        for i in aq.Range(n_qubits):
            h(i)
            for j in aq.Range(n_qubits-i-1):
                cphaseshift(i+j+1,i,angles[j])

        for i in aq.Range(n_qubits//2):
            swap(i,n_qubits-i-1)

    return qft_module

def QFT_Demo(n_qubits: int)->Qasm3Module:
    return QFT(n_qubits).build().to_ir()



    


