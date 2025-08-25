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
import itertools
from scipy.optimize import minimize
import string
import sympy as sp

class GQSP(GateLibrary):
    '''
    use this paper for future work, to be more in line with the actual gqsp implementation:
    arXiv:2105.02859 <https://arxiv.org/abs/2105.02859>
    this current work is essentially an incomplete derivative, but it works okay for any low degree polynomial  (ie less than 5)

    this formulation operates on a simpler generation sceme of {rY(tn2) * rZ(tn1) * (|1><1|@ H + |0><0|@I)  }^n * rY(t0)     *am using @ as tensor symbol
    ... which can generate largely arbitrary positive polynomials of H under normalization
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def GQSP(self,qubits,phases,hamiltonian,depth=3):
        name=  f'GQSP_{depth}_{hamiltonian.name}'
        anc_q = self.builder.claim_qubits(1)
        anc_c = self.builder.claim_clbits(1)
        if name in self.gate_ref:
            self.call_gate(name,qubits[-1],anc_q+qubits[:-1],phases=phases)
            self.measure(anc_q,anc_c)

        sys = GateBuilder()
        std =  sys.import_library(std_gates)
        ham = sys.import_library(hamiltonian)

        # Generate unique qubit argument names
        names = string.ascii_letters
        qargs = [names[i // len(names)] + names[i % len(names)] 
                for i in range(len(qubits) + 1)]
        angles = [f"θ{names[i]}" for i in range(depth*2+1)]

        std.begin_gate(name,qargs,params=angles)
        std.ry(angles[0],qargs[0])
        for i in range(depth):
            ham.controlled(qargs[1:],qargs[0])
            std.call_gate("p",qargs[0],phases=angles[i+1])
            std.ry(angles[depth+i+1],qargs[0])

    
    U = sp.Matrix([[sp.Symbol("id"),0],[0,sp.Symbol('H')]])
    def GQSP_recurse(self,mat,depth):
        r = sp.Symbol(f'r{depth}')
        qr = sp.Matrix([[sp.cos(r/2),-sp.sin(r/2)],[sp.sin(r/2),sp.cos(r/2)]])
        if depth <= 0:
            return qr*mat
        
        p = sp.Symbol(f'p{depth}')
        rp = sp.Matrix([[1,0],[0,sp.exp(1j*p)]])
        return qr*rp*GQSP.U*self.GQSP_recurse(mat,depth-1)

    def gen_cost(self,depth,t=1):
        expr = self.GQSP_recurse(sp.Matrix([1,0]),depth)[0]
        time = np.linspace(-1,1,50)
        poly = np.flip(np.pow(1j,range(depth+1))/(scp.special.factorial(range(depth+1))))
        syms = expr.free_symbols
        names = sorted([(str(a),a) for a in syms])
        srefs = [name[1] for name in names]
        expr = expr.subs({srefs[1]:1})  # substitute id for 1
        # weight = time**2
        ref = np.polyval(poly,time*t)
        # ref = np.exp(1j*time*t)
        def cost(x):
            resolved = expr.subs(dict(zip(srefs[2:],x)))
            evaluator = sp.lambdify(srefs[0],resolved,"numpy")
            series = evaluator(time)
            series = series/np.abs(series[0])  # normalize
            diff = np.sum((np.abs(series-ref)**2))
            return diff
            # print(resolved)
        return cost, names

    def find_gqsp_spectrum(self,depth):
        x = np.ones(2*depth+1)
        x[0] = 0
        xr= x
        fits = []
        time = np.linspace(-1,1,100)
        for t in time:
            if t == 0:
                fits.append(x)
                continue
            c, _ = self.gen_cost(depth,t)
            res = minimize(c,x0=xr)
            fits.append(res.x)
            # print(res.fun)
            if t != -1:
                diff =  (res.x-xr)
                xr = res.x +.25*diff
            else:
                xr = res.x
                print("reset xr")
            # xr = res.x*.33+.33*xr+.33*x
            # c(res.x,out=True)
        # print(res)
        return fits, time
