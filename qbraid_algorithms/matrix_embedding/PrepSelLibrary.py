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

"""
Quantum Gate Library for Preparation and Selection Operations

This module implements quantum gates for state preparation, operator selection,
and Pauli string decomposition using quantum compilation techniques.
"""

from ..QTran import *
import numpy as np
import itertools
from scipy.optimize import minimize
import string


class PrepSelLibrary(GateLibrary):
    """Library for combined preparation and selection quantum operations."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def prep_select(self, qubits, matrix, approximate=0):
        """
        Create a preparation-selection gate for a given matrix/operator chain.
        
        Args:
            qubits: Target qubits for the operation
            matrix: Either a matrix to decompose or pre-computed operator chain
            approximate: Approximation threshold for Pauli decomposition
            
        Returns:
            Gate name and operation counts (if new gate created)
        """
        # Handle both matrix and pre-computed operator chain inputs
        if len(np.array(matrix).shape) == 1:
            op_chain = matrix
            gate_id = abs(hash(tuple(matrix)))  # BUG FIX: Use tuple for abs(hashable
        else:
            op_chain = self.gen_pauli_string(matrix, approximate)
            gate_id = abs(hash(tuple(op_chain)))  # BUG FIX: Use tuple for abs(hashable
        
        # Calculate required ancilla qubits
        qb = int(np.ceil(np.log2(len(op_chain))))
        name = f"PS_{len(qubits)}_{gate_id}"
        print(op_chain)
        # Claim quantum resources
        anc_q = self.builder.claim_qubits(qb)
        anc_c = self.builder.claim_clbits(qb)
        
        # Use existing gate if available
        if name in self.gate_ref:
            self.call_gate(name, qubits[-1], anc_q + qubits[:-1])
            self.measure(anc_q, anc_c)
            return name
        
        # Build new gate
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        prep = sys.import_library(Prep)
        prep.call_space = "{}"
        sel = sys.import_library(Select)
        sel.call_space = "{}"
        
        # Generate unique qubit argument names
        names = string.ascii_letters
        qargs = [names[i // len(names)] + names[i % len(names)] 
                for i in range(len(qubits) + qb)]
        
        std.begin_gate(name,qargs)
        nprep, mapping = prep.prep(qargs[:qb],[a[1] for a in op_chain])
        nsel = sel.select(qargs[qb:],qargs[:qb],[a[0] for a in op_chain],mapping)
        prep.inverse_op(prep.prep,[qargs[:qb],[a[1] for a in op_chain]])
        std.end_gate()

        # Register and execute gate
        self.merge(*sys.build(), name)
        self.call_gate(name, qubits[-1], anc_q + qubits[:-1])
        self.measure(anc_q, anc_c)
        
        return name, nprep, nsel
       
    @staticmethod
    def gen_pauli_string(matrix, epsilon):
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


class Prep(GateLibrary):
    """Quantum state preparation library using amplitude encoding."""
    
    def prep(self, qubits, dist):
        """
        Prepare a quantum state with given amplitude distribution.
        
        Args:
            qubits: Target qubits for state preparation
            dist: Probability/amplitude distribution
            
        Returns:
            Gate name and state mapping
        """
        name = f"PREP_{abs(hash(tuple(dist)))}"  # BUG FIX: Use tuple for abs(hashing
        if name in self.gate_ref:
            self.call_gate(name, qubits[-1],qubits[:-1])  # BUG FIX: Simplified call
            return name, {}

        # Build preparation circuit
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        std.call_space = "{}"
        qb = int(np.ceil(np.log2(len(dist))))
        
        # Generate parameter angles and mapping
        angles, mapping = self.gen_prep_angles(dist)
        
        # Create qubit argument names
        names = string.ascii_letters
        qargs = [names[i // len(names)] + names[i % len(names)] 
                for i in range(qb)]
        
        std.begin_gate(name, qargs)
        
        # Apply rotation gates in structured pattern
        angle_idx = 0
        
        # Initial Y-rotations
        for i in range(qb):
            std.ry(angles[angle_idx], qargs[i])
            angle_idx += 1
        
        # Controlled Y-rotations in three layers
        for layer in range(2): 
            # Odd-indexed controls
            for j in range(1, qb, 2):
                if angle_idx < len(angles):  # BUG FIX: Bounds checking
                    std.cry(angles[angle_idx], qargs[j-1], qargs[j]) 
                    angle_idx += 1 
                
            # Even-indexed controls  
            for j in range(2, qb, 2):
                if angle_idx < len(angles):  # BUG FIX: Bounds checking
                    std.cry(angles[angle_idx], qargs[j-1], qargs[j])    
                    angle_idx += 1 
                    
        std.end_gate()

        self.merge(*sys.build(), name)
        self.call_gate(name, qubits[-1],qubits[:-1])  # BUG FIX: Simplified call
        return name, mapping
    
    def gen_prep_angles(self, dist):
        """
        Generate rotation angles for state preparation via optimization.
        
        Args:
            dist: Target probability distribution
            
        Returns:
            Optimized angles and index mapping
        """
        # Gate definitions
        y_rot = lambda t: np.array([[np.cos(t/2), -np.sin(t/2)], 
                                   [np.sin(t/2), np.cos(t/2)]])
        cy_rot = lambda t: np.block([[np.eye(2), np.zeros((2,2))], 
                                    [np.zeros((2,2)), y_rot(t)]])
        
        qb = int(np.ceil(np.log2(len(dist))))
        # Normalize and pad distribution
        padded_size = 2**qb
        ref_dist = np.pad(dist, (0, padded_size - len(dist)), 
                         mode="constant", constant_values=0)
        ref_dist = ref_dist / np.linalg.norm(ref_dist)
        sorted_dist = np.sort(ref_dist)
        sort_indices = np.argsort(ref_dist)
        
        def render_state(params):
            """Simulate quantum circuit with given parameters."""
            # Initial Y-rotations
            sy = y_rot(params[0])
            param_idx = 1
            
            for i in range(1, qb):
                if param_idx < len(params):
                    sy = np.kron(y_rot(params[param_idx]), sy)
                    param_idx += 1
            fit = sy
            if qb > 1:
                # Apply controlled rotations
                for layer in range(2):
                    # Build controlled gates
                    dy = cy_rot(params[param_idx]) if param_idx < len(params) else np.eye(4)
                    param_idx += 1
                    
                    for j in range(1, qb//2):
                        if param_idx < len(params):
                            dy = np.kron(cy_rot(params[param_idx]), dy)   
                            param_idx += 1
                            
                    if qb % 2 == 1:
                        dy = np.kron(np.eye(2), dy)
                        
                    # Upper controlled gates
                    uy = np.eye(2)
                    for j in range((qb-1)//2):
                        if param_idx < len(params):
                            uy = np.kron(cy_rot(params[param_idx]), uy)   
                            param_idx += 1
                            
                    if qb % 2 == 0:
                        uy = np.kron(np.eye(2), uy)
                    # print(uy.shape,dy.shape,fit.shape)
                    fit = uy @ dy @ fit
                    
            return fit[:, 0]
        
        def cost_function(params):
            """Optimization cost: 1 - fidelity with target distribution."""
            simulated = render_state(params)
            sorted_sim = np.sort(simulated)
            return 1 - np.abs(np.inner(sorted_dist, sorted_sim))
        
        # Optimize parameters
        num_params = qb + 2*2*(qb//2)  # BUG FIX: More accurate parameter count
        result = minimize(cost_function, x0=np.ones((num_params))*.1)
        print(result)


        # Create mapping from original to sorted indices
        final_state = render_state(result.x)
        mapping = dict(zip(sort_indices, np.argsort(final_state)))
        print(ref_dist)
        print(final_state)
        print([final_state[mapping[i]] for i in range(len(dist))])
        return result.x, mapping


class Select(GateLibrary): 
    """Quantum operator selection library for controlled operations."""
    
    def select(self, qubits, anc, operators, mapping):
        """
        Apply selected operators based on ancilla qubit states.
        
        Args:
            qubits: Target qubits for operations
            anc: Ancilla qubits encoding selection
            operators: List of operators to select from
            mapping: Index mapping for operator selection
            
        Returns:
            Gate name
        """
        gate_id = abs(hash((tuple(operators), tuple(mapping.items()))))
        name = f"SEL_{gate_id}"
        
        if name in self.gate_ref:
            self.call_gate(name,  qubits[-1],anc + qubits[:-1])  # BUG FIX: Proper argument order
            return name

        # Generate argument names
        names = string.ascii_letters  
        qargs = [names[i // len(names)] + names[i % len(names)] 
                for i in range(len(qubits) + len(anc))]
        
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        std.call_space = "{}"
        pauli_lib = sys.import_library(PauliOperator)
        pauli_lib.call_space = "{}"

        # Invert mapping for lookup
        pinv = {v: k for k, v in mapping.items()}
        
        std.begin_gate(name, qargs)
        
        prev_gray = None
        for i in range(len(operators)):
            # Gray code for efficient state transitions
            gray_code = i ^ (i >> 1)
            
            if prev_gray is not None:
                # Flip qubits that changed in Gray code
                diff = gray_code ^ prev_gray
                bit_pos = (diff & -diff).bit_length() - 1  # Find rightmost set bit
                if bit_pos < len(anc):
                    std.x(qargs[bit_pos])

            # Apply selected operator
            mapped_idx = pinv.get(i, i)  # BUG FIX: Handle missing mappings
            if mapped_idx < len(operators):
                op = operators[mapped_idx]
                
                if isinstance(op, str):
                    # Pauli string operator
                    pauli_lib.controlled_op(pauli_lib.pauli_operator, 
                                          [qargs, op], n=len(anc))
                else:
                    # Custom gate library operator
                    op_lib = sys.import_library(op)
                    op_lib.controlled(qargs[len(anc):], qargs[:len(anc)])
                    
            prev_gray = gray_code
        for j in range(len(anc)):
            if (prev_gray>>j)%2 == True:
                std.x(qargs[j])
        std.end_gate()
        
        self.merge(*sys.build(), name)
        self.call_gate(name,  qubits[-1],anc + qubits[:-1])  # BUG FIX: Proper argument order
        return name


class PauliOperator(GateLibrary):
    """Library for Pauli string operations."""
    
    def pauli_operator(self, qubits, op):
        """
        Apply a Pauli string operator to qubits.
        
        Args:
            qubits: Target qubits
            op: Pauli string (e.g., "XYZI")
            
        Returns:
            Gate name or None if invalid
        """
        if not isinstance(op, str):
            # Not a Pauli string - skip
            return None
        
        # Validate Pauli string
        valid_symbols = {'I', 'X', 'Y', 'Z'}
        if not all(ch in valid_symbols for ch in op):
            print(f"Invalid Pauli string: {op}")
            return None
        
        if op in self.gate_ref:
            self.call_gate(op, qubits[-1],qubits[:-1])
            return op

        # BUG FIX: Correct qubit count
        if len(op) > len(qubits):
            print(f"Pauli string length {len(op)} doesn't match qubit count {len(qubits)}")
            return None

        # Create new Pauli operator gate
        names = string.ascii_letters
        qargs = [names[i // len(names)] + names[i % len(names)] 
                for i in range(len(op))]  # BUG FIX: Use len(op)
        
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        std.begin_gate(op, qargs)
        std.call_space = "{}"
        
        # Apply Pauli gates
        for i, gate in enumerate(op):
            match gate: 
                case 'I':
                    pass  # Identity - no operation
                case 'X':
                    std.x(qargs[i])  # BUG FIX: Use qargs instead of index
                case 'Y':
                    std.y(qargs[i])
                case 'Z':
                    std.z(qargs[i])
                case _:
                    print(f"Unknown Pauli gate: {gate}")
                    
        std.end_gate()
        
        self.merge(*sys.build(), op)
        self.call_gate(op,  qubits[-1],qubits[:-1])
        return op