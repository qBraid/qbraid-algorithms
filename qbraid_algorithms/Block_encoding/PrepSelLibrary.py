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

class PrepSelLibrary(GateBuilder):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def prep_select(self,qubits,matrix,approximate=0):
        if isinstance(matrix,tuple):
            id = hash(matrix)
            PauliString = matrix
        else:
            PauliString = self.gen_pauli_string(matrix,approximate )
            id = hash(PauliString)
        name = f"PS_{id}"
        if name in self.gate_ref:
            self.call_gate(name,qubits[-1],qubits[:-1])
            return name

    def gen_prepare_circuit(self,dist):
        y = lambda t: np.array([[np.cos(t/2),-np.sin(t/2)],[np.sin(t/2),np.cos(t/2)]])
        cy = lambda t: np.block([[np.eye(2),np.zeros(2)],[np.zeros(2),y(t)]])
        qb = np.ceil(np.log2(len(dist)))
        ref = np.pad(dist,(0,2**qb-len(dist)))/np.linalg.norm(dist)
        def cost(params):
            sy = y(params[0])
            index = 1
            for i in range(1,qb):
                sy = np.kron(y(params[index]),sy)
                index +=1
            dy = cy(params[index])  
            index +=1
            for j in range(1,qb//2):
                dy = np.kron(cy(params[index]),dy)   
                index +=1 
            if qb%2 == 1:
                dy = np.kron(np.eye(2),dy)
            fit = (dy@sy)[:,0]     


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