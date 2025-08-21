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

class PrepSelLibrary(GateLibrary):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def prep_select(self,qubits,matrix,approximate=0):
        if len(np.array(matrix).shape)==1:
            id = hash(matrix)
            PauliString = matrix
        else:
            PauliString = self.gen_pauli_string(matrix,approximate )
            id = hash(PauliString)
        name = f"PS_{id}"
        if name in self.gate_ref:
            self.call_gate(name,qubits[-1],qubits[:-1])
            return name

    def prep(self,qubits,dist):
        name = f"PREP_{hash(dist)}"
        if name in self.gate_ref:
            self.call_gate(name,qubits[-1],qubits[:-1])
            return name, mapping

        sys = GateBuilder()
        std = sys.import_library(std_gates)
        qb = int(np.ceil(np.log2(len(dist))))
        names = string.ascii_letters
        angles, mapping = self.gen_prep_angles(dist)
        qargs = [names[int(i/len(names))]+names[i%len(names)] for i in range(qb)]
        std.begin_gate(name,qargs)
        index = 0
        for i in range(qb):
            std.ry(angles[index],qargs[i])
            index +=1
        for x in range(3): 
            for j in range(1,qb,2):
                std.cry(angles[index],qargs[j-1],qargs[j]) 
                index +=1 
                
            for j in range(2,qb,2):
                std.cry(angles[index],qargs[j-1],qargs[j])    
                index +=1 
        std.end_gate()

        self.merge(*sys.build(),name)
        self.call_gate(name,qubits[-1],qubits[:-1])
        return name, mapping
    
    def select(self,reg,operators,mapping):
        pinv = {v:k for k,v in mapping.items()}
        for i in range(len(operators)):
            pass

    
    def Apply_operator(self,op,reg,anc,index):
        if not isinstance(op,str):
            #operator is a gate library object
            pass

        

        # Process each symbol
        for i, gate in enumerate(op):
            match gate:  # Python 3.10+ (pattern matching)
                case 'I':
                    print(f"Step {i}: Identity gate (I)")
                case 'X':
                    print(f"Step {i}: Pauli-X gate")
                case 'Y':
                    print(f"Step {i}: Pauli-Y gate")
                case 'Z':
                    print(f"Step {i}: Pauli-Z gate")
                case _:
                    print(f"Step {i}: Unknown gate (should not happen)")


    def gen_prep_angles(self,dist):
        y = lambda t: np.array([[np.cos(t/2),-np.sin(t/2)],[np.sin(t/2),np.cos(t/2)]])
        cy = lambda t: np.block([[np.eye(2),np.zeros((2,2))],[np.zeros((2,2)),y(t)]])
        qb = int(np.ceil(np.log2(len(dist))))
        cdist = np.sort(dist)
        indist = np.argsort(dist)
        ref = np.pad(cdist,(0,int(2**qb-len(dist))),mode="constant",constant_values=0)/np.linalg.norm(dist)
        def render_mat(params):
            sy = y(params[0])
            index = 1
            for i in range(1,qb):
                sy = np.kron(y(params[index]),sy)
                index +=1
            fit = sy
            for x in range(3):
                dy = cy(params[index])  
                index +=1
                for j in range(1,qb//2):
                    dy = np.kron(cy(params[index]),dy)   
                    index +=1 
                if qb%2 == 1:
                    dy = np.kron(np.eye(2),dy)
                    
                uy = np.eye(2)
                for j in range((qb-1)//2):
                    uy = np.kron(cy(params[index]),uy)   
                    index +=1 
                if qb%2 == 0:
                    uy = np.kron(np.eye(2),uy)

                fit = uy@dy@fit
            return fit[:,0]
            # plt.plot(fit)
        def cost(params):
            fit = render_mat(params)
            sety = np.sort(fit)
            return 1-np.inner(ref,sety)
        res = minimize(cost,x0=np.zeros(int(qb*4)))
        diff = np.zip(indist,np.argsort(render_mat(res.x)))
        return res.x, diff

    def gen_pauli_string(self,matrix, epsilon):
        """
        Decompose a square matrix into tensor products of Pauli matrices.

        Args:
            matrix (np.ndarray): A 2^n x 2^n complex matrix.
            epsilon (float): Threshold parameter for filtering.

        Returns:
            List[Tuple[str, float]]: Sorted list of (Pauli string, coefficient).
        """
        # Define Pauli matrices
        paulis = {
            "I": np.array([[1, 0], [0, 1]], dtype=complex),
            "X": np.array([[0, 1], [1, 0]], dtype=complex),
            "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
            "Z": np.array([[1, 0], [0, -1]], dtype=complex),
        }

        # Check size
        dim = matrix.shape[0]
        n = int(np.log2(dim))
        if 2**n != dim:
            raise ValueError("Matrix size must be a power of 2.")

        # Generate all Pauli tensor products
        pauli_labels = list(paulis.keys())
        basis = list(itertools.product(pauli_labels, repeat=n))

        result = []
        threshold = epsilon / np.log2(dim)

        for label_tuple in basis:
            # Build the tensor product matrix
            op = paulis[label_tuple[0]]
            for l in label_tuple[1:]:
                op = np.kron(op, paulis[l])

            # Compute coefficient: Tr(P^† M) / 2^n
            coef = np.trace(op.conj().T @ matrix) / (2**n)

            if abs(coef) > threshold:
                pauli_str = "".join(label_tuple)
                result.append((pauli_str, coef))

        # Sort by absolute value of coefficient (descending)
        result.sort(key=lambda x: abs(x[1]), reverse=True)
        return result