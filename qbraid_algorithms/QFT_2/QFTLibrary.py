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
import string

class QFTLibrary(GateLibrary):
    name = "QFT"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # self.call_space = "{}"

    def QFT(self, qubits:list, swap=True):
        name = f'QFT{len(qubits)}{'S' if swap else ''}'
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
            std.h(names[i+1])
            for j in range(i+1,len(qubits)):
                std.call_gate("cp",names[j+1],controls=names[i+1],phases=f"pi/{2**(j-i)}")
        if(swap):
            for i in range(len(qubits)//2):
                std.call_gate("swap",names[i],controls=names[-i-1])
    
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
        



        

    
