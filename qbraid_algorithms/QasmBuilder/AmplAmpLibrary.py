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


class AALibrary(GateLibrary):
    name = "AmplitudeAmplification"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.name = "AmplAmp"

    def AA(self,z,qubits: list,depth:int):
        name = f'AmplAmp{len(qubits)}{z.name}{depth}'
        if name in self.gate_ref:
            self.call_gate(name,qubits[-1],qubits[:-1])
            return
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        za = sys.import_library(z)
        names = " " + string.ascii_letters
        qargs = [names[int(i/len(string.ascii_letters))]+string.ascii_letters[i%len(string.ascii_letters)] for i in range(len(qubits))]

        
        std.begin_gate(name,qargs)
        std.call_space = " {} "
        # first application of z prep
        [std.h(i) for i in name[1:len(qubits)+1]]
        #iterated expansion of Z Zp Z0 Zp
        for _ in range(depth):
            za.apply(qubits)
            [sys.h(i) for i in name[1:len(qubits)+1]]
            std.controlled_op("cphase",[names[len(qubits)+1],names[1:len(qubits)+1]])
            [sys.h(i) for i in name[1:len(qubits)+1]]
        std.end_gate()



