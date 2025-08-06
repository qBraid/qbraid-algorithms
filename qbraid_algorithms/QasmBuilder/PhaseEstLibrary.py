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

from GateLibrary import GateLibrary, std_gates
from QasmBuilder import FileBuilder, QasmBuilder, GateBuilder
from QFTLibrary import QFTLibrary
import string

class PhaseEstimationLibrary(GateLibrary):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def phase_estimation(self, qubits:list,spectra:list,hamiltonian, evolution=False):
        name = f'P_EST_{len(qubits)}_{hamiltonian.name}'
        if name in self.gate_ref:
            self.call_gate(name,qubits[-1],qubits[:-1])
            return
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        ham = sys.import_library(hamiltonian)
        qft = sys.import_library(QFTLibrary)
        # names = " " + string.ascii_letters
        # qargs = [names[int(i/len(string.ascii_letters))]+string.ascii_letters[i%len(string.ascii_letters)] for i in range(len(qubits))]
        std.begin_subroutine(name,[f"qubit[{len(qubits)}] a",f"qubit[{len(spectra)}] b"])
        for i in range(len(spectra)):
            for _ in range(2**i):
                qft.controlled_op(ham.apply,[qubits,spectra[i]])
        qft.QFT(spectra)
        std.end_subroutine()
        p, i, d = sys.build()
        for imps in i:
            if imps not in self.gate_import:
                self.gate_import.append(imps)
            
        for defs in d:
            if defs[0] not in self.gate_defs:
                self.gate_defs[defs[0]] = defs[1]
        self.gate_defs[name] = p
        self.gate_ref.append(name)
        self.call_gate(name,qubits[-1],qubits[:-1])
        



        

    
