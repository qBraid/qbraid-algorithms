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

# from GateLibrary import GateLibrary, std_gates
from qbraid_algorithms.QasmBuilder import *
# from qbraid_algorithms.QFT_2 import QFTLibrary
import string


class AALibrary(GateLibrary):
    name = "AmplitudeAmplification"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.name = "AmplAmp"

    def Grover(self,H,qubits: list,depth:int):
        name = f'AmplAmp{len(qubits)}{H.name}{depth}'
        if name in self.gate_ref:
            self.call_gate(name,qubits[-1],qubits[:-1])
            return
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        za = sys.import_library(H)
        names = string.ascii_letters
        qargs = [names[int(i/len(names))]+names[i%len(names)] for i in range(len(qubits))]

        
        std.begin_gate(name,qargs)
        std.call_space = " {}"
        # first application of z prep
        [std.h(i) for i in qargs]
        #iterated expansion of Z Zp Z0 Zp
        std.begin_loop(depth)
        std.comment("Za")
        za.apply(qargs)
        [std.h(i) for i in qargs]
        std.comment("Z0")
        [std.x(i) for i in qargs]
        std.controlled_op("z",(qargs[-1],qargs[:-1]),n=len(qubits)-1)
        [std.x(i) for i in qargs]
        [std.h(i) for i in qargs]
        std.end_loop()
        # for _ in range(depth):
        #     std.comment("Za")
        #     za.apply(qargs)
        #     [std.h(i) for i in qargs]
        #     std.comment("Z0")
        #     print((qargs[-1],qargs[:-1]))
        #     std.controlled_op("cp",(qargs[-1],qargs[:-1]),n=len(qubits)-2)
        #     [std.h(i) for i in qargs]
        std.end_gate()

        
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

        
    def AA(self,Z,H,qubits: list,depth:int):
        name = f'AmplAmp{len(qubits)}{z.name}{depth}'
        if name in self.gate_ref:
            self.call_gate(name,qubits[-1],qubits[:-1])
            return
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        za = sys.import_library(Z)
        Ha = sys.import_library(H)
        names = string.ascii_letters
        qargs = [names[int(i/len(names))]+names[i%len(names)] for i in range(len(qubits))]

        
        std.begin_gate(name,qargs)
        std.call_space = " {} "
        # first application of z prep
        [std.h(i) for i in qargs]
        #iterated expansion of Z Zp Z0 Zp
        std.begin_loop(depth)
        std.comment("Za")
        Ha.apply(qargs)
        [std.h(i) for i in qargs]
        std.comment("Z0")
        [std.x(i) for i in qargs]
        std.controlled_op("cz",(qargs[-1],qargs[:-1]),n=len(qubits)-2)
        [std.x(i) for i in qargs]
        [std.h(i) for i in qargs]
        std.end_loop()

        # for _ in range(depth):
        #     std.comment("Za")
        #     za.apply(qargs)
        #     [std.h(i) for i in qargs]
        #     std.comment("Z0")
        #     print((qargs[-1],qargs[:-1]))
        #     std.controlled_op("cp",(qargs[-1],qargs[:-1]),n=len(qubits)-2)
        #     [std.h(i) for i in qargs]
        std.end_gate()

        
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



