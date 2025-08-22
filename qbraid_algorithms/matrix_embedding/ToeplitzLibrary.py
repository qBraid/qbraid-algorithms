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
from ..qft import QFTLibrary
import numpy as np
from itertools import combinations
import string

class Toeplitz(GateLibrary):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def real_toeplitz(qubits,coefficients,):
        name = f"r_top_{len(qubits)}_{abs(hash(tuple(coefficients)))}"

class diagonal(GateLibrary):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def diag_scale(self,qubits,coe):
        name = f"diag{len(qubits)}_s_{hash(tuple(coe))}"
        anc_q = self.builder.claim_qubits(1)
        anc_c = self.builder.claim_clbits(1)
        if name in self.gate_ref:
            self.call_gate(name,  qubits[-1],anc_q+qubits[:-1]) 
            self.measure(anc_q,anc_c)
            return name


    def diag(self,qubits,vals,depth=3):
        name = f"diag{len(qubits)}_{hash(tuple(vals))}"

        if name in self.gate_ref:
            self.call_gate(name,  qubits[-1],qubits[:-1]) 
            return name
        
        # Generate argument names
        names = string.ascii_letters  
        qargs = [names[i // len(names)] + names[i % len(names)] for i in range(len(qubits))]
        
        qb = int(np.log2(len(vals))+.01)
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        projection = self.phase_projector(vals,depth)
        std.begin_gate(name,qargs)
        std.x(0)
        std.p(projection[0],0)
        std.x(0)
        pindex = 1
        for i in range(depth):
            for c in [list(combo) for combo in combinations(range(qb), i+1)]:
                if(np.abs(projection[pindex])<.1):
                    pindex +=1 
                    continue
                if len(c) == 1:
                    std.p(projection[pindex],qargs[c[0]])
                else:
                    # print(c)
                    std.controlled_op("p",(projection[pindex],qargs[c[0]],[qargs[n] for n in c[1:]]),n=len(c)-1)
                pindex +=1 
        
        std.end_gate()
        self.merge(sys.build(),name)
        self.call_gate(name,  qubits[-1],qubits[:-1]) 
        return name        

    def phase_projector(target,depth,plot=False):
        qb = int(np.log2(len(target))+.01)
        basis = np.arange(2**qb)
        space = []
        for i in range(depth):
            for c in [list(combo) for combo in combinations(range(qb), i+1)]:
                r = np.ones(2**qb)
                for e in c:
                    r *= ((basis/(2**e)).astype(int)%2)

                if i == 0 and c== [0]:
                    space.append(np.logical_xor(r,np.ones(2**qb)))
                space.append(r)
        sysmat = np.linalg.pinv(np.array(space).T)
        return sysmat@target  


