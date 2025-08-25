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


from ..QTran import *
import numpy as np
import string

"""
generalized trotterization module
accepts several hamiltonians statements and uses Suzuki Trotter decomposition to expand out the evolution
requires fractional application of given hamils
notable about this implementation is its used of Suzuki's 1992/2005 recursive symmetric fractal formulation for the expansion
"""
class Trotter(GateLibrary):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def trot_suz(self, qubits,t, Hp, Hq,depth):
        name = f"trot_suz_{len(qubits)}_{Hp.name}_{Hq.name}"

        if name in self.gate_ref:
            self.call_subroutine(name,[qubits,t,depth])
            return
        
        self.gate_ref.append(name)
        sys = self.builder
        std = sys.import_library(std_gates)
        Ha = sys.import_library(Hp)
        Hb = sys.import_library(Hq)

        std.begin_subroutine(name,[f"qubit[{len(qubits)}] a","float r","int d"])
        std.begin_if("d < 2")
        Ha.apply("r/2",[f"a[{i}]" for i in range(len(qubits))])
        Hb.apply("r",[f"a[{i}]" for i in range(len(qubits))])
        Ha.apply("r/2",[f"a[{i}]" for i in range(len(qubits))])
        std.program("return;")
        std.end_if()
        Uk = std.add_var("Uk",assignment="1/(4-4**(1/(2*d-1)))",type="float")
        std.call_subroutine(name,["a",f'{Uk}*r',"d-1"])
        std.call_subroutine(name,["a",f'{Uk}*r',"d-1"])
        std.call_subroutine(name,["a",f'(1-4*{Uk})*r',"d-1"])
        std.call_subroutine(name,["a",f'{Uk}*r',"d-1"])
        std.call_subroutine(name,["a",f'{Uk}*r',"d-1"])
        std.end_subroutine()

        
        self.call_subroutine(name,[qubits,t,depth])



        