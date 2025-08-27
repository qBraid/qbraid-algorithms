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

from ..QTran import *


class AALibrary(GateLibrary):
    name = "AmplitudeAmplification"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.name = "AmplAmp"

    def Grover(self,H,qubits: list,depth:int):
        name = f'Grover{len(qubits)}{H.name}{depth}'
        if name in self.gate_ref:
            self.call_subroutine(name,[self.call_space.format("{"+" ,".join(str(i) for i in qubits)+"}")])
            # self.call_gate(name,qubits[-1],qubits[:-1])
            return
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        std.call_space = " {}"
        za = sys.import_library(H)
        names = string.ascii_letters
        qargs = [names[int(i/len(names))]+names[i%len(names)] for i in range(len(qubits))]

        # WIP! swap commenting of implementation if subroutine misbehaves/does not work with current parser
        # subroutine keeps the generated code compact whereas gates cannot use loops (thus following gate impl will need to be fixed with python loop)

        # std.begin_gate(name,qargs)
        # # first application of z prep
        # [std.h(i) for i in qargs]
        # #iterated expansion of Z Zp Z0 Zp
        # std.begin_loop(depth)
        # std.comment("Za")
        # za.apply(qargs)
        # [std.h(i) for i in qargs]
        # std.comment("Z0")
        # [std.x(i) for i in qargs]
        # std.controlled_op("z",(qargs[-1],qargs[:-1]),n=len(qubits)-1)
        # [std.x(i) for i in qargs]
        # [std.h(i) for i in qargs]
        # std.end_loop()
        # std.end_gate()


        register = "reg"
        std.begin_subroutine(name,[f"qubit[{len(qubits)}] {register}"])
        std.h(register)
        std.begin_loop(depth)
        std.comment("Za")
        za.apply([f"reg[{i}]" for i in range(len(qubits))])
        std.h(register)
        std.comment("Z0")
        std.x(register)
        std.controlled_op("z",(f"{register}[0]",[f"{register}[{i}]" for i in range(len(qubits)-1)]),n=len(qubits)-1)
        std.x(register)
        std.h(register)
        std.end_loop()
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
        # self.call_gate(name,qubits[-1],qubits[:-1])
        self.call_subroutine(name,[self.call_space.format("{" + " ,".join(str(i) for i in qubits)+"}")])

        
    def AA(self,Z,H,qubits: list,depth:int):
        name = f'AmplAmp{len(qubits)}{z.name}{depth}'
        if name in self.gate_ref:
            self.call_subroutine(name,[self.call_space.format("{" + " ,".join(str(i) for i in qubits)+"}")])
            # self.call_gate(name,qubits[-1],qubits[:-1])
            return
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        za = sys.import_library(Z)
        Ha = sys.import_library(H)
        names = string.ascii_letters
        qargs = [names[int(i/len(names))]+names[i%len(names)] for i in range(len(qubits))]

        
        # std.begin_gate(name,qargs)
        # std.call_space = " {} "
        # # first application of z prep
        # [std.h(i) for i in qargs]
        # #iterated expansion of Z Zp Z0 Zp
        # std.begin_loop(depth)
        # std.comment("Za")
        # Ha.apply(qargs)
        # [std.h(i) for i in qargs]
        # std.comment("Z0")
        # [std.x(i) for i in qargs]
        # std.controlled_op("cz",(qargs[-1],qargs[:-1]),n=len(qubits)-2)
        # [std.x(i) for i in qargs]
        # [std.h(i) for i in qargs]
        # std.end_loop()
        # std.end_gate()
        # for _ in range(depth):
        #     std.comment("Za")
        #     za.apply(qargs)
        #     [std.h(i) for i in qargs]
        #     std.comment("Z0")
        #     print((qargs[-1],qargs[:-1]))
        #     std.controlled_op("cp",(qargs[-1],qargs[:-1]),n=len(qubits)-2)
        #     [std.h(i) for i in qargs]
        
        
        register = "reg"
        std.begin_subroutine(name,[f"qubit[{len(qubits)}] {register}"])
        za.unapply([f"reg[{i}]" for i in range(len(qubits))])
        std.h(register)
        std.begin_loop(depth)
        std.comment("H")
        Ha.apply([f"reg[{i}]" for i in range(len(qubits))])
        std.comment("Zp*")
        za.unapply([f"reg[{i}]" for i in range(len(qubits))])
        std.comment("Z0")
        std.x(register)
        std.controlled_op("z",(f"{register}[0]",[f"{register}[{i}]" for i in range(len(qubits)-1)]),n=len(qubits)-1)
        std.x(register)
        std.comment("Zp")
        za.apply([f"reg[{i}]" for i in range(len(qubits))])
        std.end_loop()
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
        # self.call_gate(name,qubits[-1],qubits[:-1])
        self.call_subroutine(name,[self.call_space.format("{" + " ,".join(str(i) for i in qubits)+"}")])



