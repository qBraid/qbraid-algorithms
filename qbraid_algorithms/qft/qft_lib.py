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
This module provides the QFTLibrary class for constructing and managing Quantum
Fourier Transform (QFT) gates using the qBraid algorithms framework.
Classes:
    QFTLibrary(GateLibrary):
Dependencies:
    - string
    - qbraid_algorithms.qtran (GateBuilder, GateLibrary, std_gates)
"""

# from QasmBuilder import FileBuilder, QasmBuilder, GateBuilder
import string

# pylint: disable=invalid-name
# mypy: disable_error_code="call-arg"
from qbraid_algorithms.qtran import GateBuilder, GateLibrary, std_gates


class QFTLibrary(GateLibrary):
    """QFTLibrary provides methods to construct and manage 
    Quantum Fourier Transform (QFT) gates, extending GateLibrary 
    for use in quantum algorithms."""
    name = "QFT"
    def __init__(self,*args,**kwargs):
        """
        Initialize the QFTLibrary instance.

        Args:
            *args: Variable length argument list for parent GateLibrary.
            **kwargs: Arbitrary keyword arguments for parent GateLibrary.
        """
        super().__init__(*args,**kwargs)
        # self.call_space = "{}"

    def QFT(self, qubits:list, swap=True):
        """
        Constructs a Quantum Fourier Transform (QFT) gate for the specified qubits.

        Parameters:
            qubits (list of int): List of qubit indices (as integers) to apply the QFT on.
            swap (bool, optional): If True, applies swap gates at the end to reverse qubit order. Defaults to True.

        Behavior:
            - Builds and registers a QFT gate with optional swaps.
            - Calls the constructed gate on the provided qubits.
        """
        name = f'QFT{len(qubits)}{"S" if swap else ""}'
        if name in self.gate_ref:
            self.call_gate(name,qubits[-1],qubits[:-1])
            return
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        names = string.ascii_letters
        qargs = [names[int(i/len(names))]+names[i%len(names)] for i in range(len(qubits))]

        std.begin_gate(name,qargs)
        std.call_space = "{}"
        for i in range(len(qubits)):
            std.h(qargs[i])
            for j in range(i+1,len(qubits)):
                std.call_gate("cp",qargs[j],controls=qargs[i],phases=f"pi/{2**(j-i)}")
        if swap:
            for i in range(len(qubits)//2):
                std.call_gate("swap", qargs[i], qargs[-i-1])

        std.end_gate()

        # std.begin_gate(name,qargs)
        # std.begin_loop(len(qubits))
        # std.h("i")
        # std.begin_loop(f"j in [i+1:{len(qubits)}]")
        # std.call_gate("cp","j",controls="i",phases="pi>>(j-i)")
        # std.end_loop()
        # std.end_loop()
        # std.end_gate()

        # std.begin_subroutine(name,[f'qubit[{len(qubits)}] a'])
        # std.begin_loop(len(qubits))
        # std.h("i")
        # std.begin_loop(f"j in [i+1:{len(qubits)}]")
        # std.call_gate("cp","j",controls="i",phases="pi>>(j-i)")
        # std.end_loop()
        # std.end_loop()
        # std.end_subroutine()

        self.merge(*sys.build(),name)
        self.call_gate(name,qubits[-1],qubits[:-1])
