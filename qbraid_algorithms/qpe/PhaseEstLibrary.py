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

import string

# from GateLibrary import GateLibrary, std_gates
from qbraid_algorithms.QTran import GateBuilder, GateLibrary, std_gates

from ..qft import QFTLibrary


class PhaseEstimationLibrary(GateLibrary):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def phase_estimation(self, qubits:list,spectra:list,hamiltonian, evolution=None):
        name = f'P_EST_{len(qubits)}_{hamiltonian.name}'
        if name in self.gate_ref:
            self.call_gate(name,spectra[-1],qubits+spectra[:-1])
            return name
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        ham = sys.import_library(hamiltonian)
        ham.call_space = " {}"
        qft = sys.import_library(QFTLibrary)
        qft.call_space = " {}"
        # names = " " + string.ascii_letters
        qargs = [string.ascii_letters[int(i/len(string.ascii_letters))]+string.ascii_letters[i%len(string.ascii_letters)] for i in range(len(qubits)+len(spectra))]
        # std.begin_gate(name,[f"qubit[{len(qubits)}] a",f"qubit[{len(spectra)}] b"])
        std.begin_gate(name,qargs)
        for i in range(len(spectra)):
            if evolution is not None:
                ham.controlled(evolution*2**i,qargs[:len(qubits)],qargs[len(qubits)+i])
            else:
                for _ in range(2**i):
                    ham.controlled(qargs[:len(qubits)],qargs[len(qubits)+i])
        qft.QFT(qargs[len(qubits):])
        std.end_gate()
        
        self.merge(sys.build(),name)
        self.call_gate(name,spectra[-1],qubits+spectra[:-1])
        return name
    
        



        

    
