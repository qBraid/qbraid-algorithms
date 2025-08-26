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
Enhanced Hamiltonian Test Definitions

These Hamiltonian classes provide non-trivial, non-commuting quantum operations
suitable for testing GQSP, Trotter decomposition, and other quantum algorithms.
They primarily implement the expected interfaces for arbitrary circuit application:
data member: name
apply
controlled

Each Hamiltonian implements:
- Complex multi-qubit interactions
- Non-commuting rotations (RX, RY, RZ)
- Controlled operations with different targets
- Proper parameterization for time evolution

Designed for semantic testing (compilation) and integration testing (correctness).
#####WARNING#####
These are not true embeddings of their namesake, they are ancilla free representations 
for product formula use and semi namesake testing of bare ancilla. True, blind ancilla 
collecting versions will be added at a later date
"""



import string
from ..QTran import *


class TransverseFieldIsing(GateLibrary):
    """
    Transverse Field Ising Model Hamiltonian: H = -J∑ZZ + h∑X
    
    Combines nearest-neighbor ZZ interactions with transverse X fields.
    This creates strong non-commutativity between different terms.
    formulation is not a direct matrix embedding but is intended for use 
    in series product formulation under small time steps
    """
    name = "TFIM"
    
    def __init__(self, reg=3, J=1.0, h=0.5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reg_size = reg
        self.J = J  # Coupling strength
        self.h = h  # Transverse field strength
        self.name = f"TFIM_{self.reg_size}q_J{int(J*100)}_h{int(h*100)}"
        
        # Generate unique qubit argument names
        names = string.ascii_letters
        qargs = [names[i // len(names)] + names[i % len(names)] 
                for i in range(self.reg_size)]
        
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        std.call_space = " {}"
        
        std.begin_gate(self.name, qargs, params=["time"])
        
        # ZZ interactions between nearest neighbors
        for i in range(self.reg_size - 1):
            # Implement exp(-i * J * ZZ * time) using CNOT + RZ + CNOT
            std.cnot(qargs[i], qargs[i + 1])
            std.rz(f"{2 * J} * time", qargs[i + 1])
            std.cnot(qargs[i], qargs[i + 1])
        
        # Add periodic boundary condition for closed chain
        if self.reg_size > 2:
            std.cnot(qargs[-1], qargs[0])
            std.rz(f"{2 * J} * time", qargs[0])
            std.cnot(qargs[-1], qargs[0])
        
        # Transverse field X rotations
        for i in range(self.reg_size):
            std.rx(f"{2 * h} * time", qargs[i])
            
        std.end_gate()
        # self.call_space = " {}"
        
        # Register the gate
        self.merge(*sys.build(),self.name)

    def apply(self, time, qubits):
        """Apply TFIM evolution for given time."""
        self.call_gate(self.name, qubits[-1],qubits[:-1], phases=[time])
        
    def controlled(self, time, qubits, control):
        """Apply controlled TFIM evolution."""
        self.controlled_op(self.name, (qubits[-1],[control]+qubits[:-1], time), n=1)



class HeisenbergXYZ(GateLibrary):
    """
    Heisenberg XYZ Model: H = Jx[XX + Jy[YY + Jz[ZZ
    
    Implements all three Pauli interactions between neighboring qubits.
    Highly non-commuting due to different Pauli matrices on same qubits.
    """
    name = "HeisenbergXYZ"
    
    def __init__(self, reg=3, Jx=1.0, Jy=1.0, Jz=1.0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reg_size = reg
        self.Jx, self.Jy, self.Jz = Jx, Jy, Jz
        self.name = f"HeisenbergXYZ_{self.reg_size}q_Jx{int(100*Jx)}_Jy{int(100*Jy)}_Jz{int(100*Jz)}"
        
        names = string.ascii_letters
        qargs = [names[i // len(names)] + names[i % len(names)] 
                for i in range(self.reg_size)]
        
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        std.call_space = " {}"
        
        std.begin_gate(self.name, qargs, params=["time"])
        
        for i in range(self.reg_size - 1):
            # XX interaction: exp(-i * Jx * XX * time)
            std.ry("pi/2", qargs[i])      # X basis rotation
            std.ry("pi/2", qargs[i + 1])
            std.cnot(qargs[i], qargs[i + 1])
            std.rz(f"{2 * Jx} * time", qargs[i + 1])
            std.cnot(qargs[i], qargs[i + 1])
            std.ry("-pi/2", qargs[i])     # Inverse rotation
            std.ry("-pi/2", qargs[i + 1])
            
            # YY interaction: exp(-i * Jy * YY * time)  
            std.rx("-pi/2", qargs[i])     # Y basis rotation
            std.rx("-pi/2", qargs[i + 1])
            std.cnot(qargs[i], qargs[i + 1])
            std.rz(f"{2 * Jy} * time", qargs[i + 1])
            std.cnot(qargs[i], qargs[i + 1])
            std.rx("pi/2", qargs[i])      # Inverse rotation
            std.rx("pi/2", qargs[i + 1])
            
            # ZZ interaction: exp(-i * Jz * ZZ * time)
            std.cnot(qargs[i], qargs[i + 1])
            std.rz(f"{2 * Jz} * time", qargs[i + 1])
            std.cnot(qargs[i], qargs[i + 1])
            
        std.end_gate()
        # self.call_space = " {}"
        self.merge(*sys.build(),self.name)

    def apply(self, time, qubits):
        """Apply Heisenberg XYZ evolution for given time."""
        self.call_gate(self.name, qubits[-1],qubits[:-1], phases=[time])
        
    def controlled(self, time, qubits, control):
        """Apply controlled Heisenberg evolution."""
        self.controlled_op(self.name, (qubits[-1],[control]+qubits[:-1], time), n=1)



class RandomizedHamiltonian(GateLibrary):
    """
    Randomized Non-Commuting Hamiltonian for stress testing.
    
    Applies random combinations of single and two-qubit rotations
    with controlled dependencies. Designed to test algorithm robustness.
    """
    name = "RandomHam"
    
    def __init__(self, reg=3, seed=42, density=0.7, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reg_size = reg
        self.seed = seed
        self.density = density  # Fraction of possible interactions to include
        self.name = f"RandomHam_{self.reg_size}q_s{seed}_d{int(100*density)}"
        
        # Use seed for reproducible randomness in testing
        import random
        random.seed(seed)
        
        names = string.ascii_letters
        qargs = [names[i // len(names)] + names[i % len(names)] 
                for i in range(self.reg_size)]
        
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        std.call_space = " {}"
        
        std.begin_gate(self.name, qargs, params=["time"])
        
        # Random single-qubit rotations
        pauli_gates = ['rx', 'ry', 'rz']
        for i in range(self.reg_size):
            if random.random() < density:
                gate_type = random.choice(pauli_gates)
                angle = random.uniform(0.1, 2.0)  # Random coupling strength
                std.call_gate(gate_type, qargs[i], phases=[f"{angle} * time"])
        
        # Random two-qubit interactions
        for i in range(self.reg_size):
            for j in range(i + 1, self.reg_size):
                if random.random() < density * 0.5:  # Lower density for 2-qubit
                    # Random ZZ-type interaction with basis rotation
                    basis_rot = random.choice(['rx', 'ry', 'rz'])
                    angle = random.uniform(0.1, 1.5)
                    
                    # Apply random basis rotations
                    std.call_gate(basis_rot, qargs[i], phases=["pi/2"])
                    std.call_gate(basis_rot, qargs[j], phases=["pi/2"])
                    
                    # Controlled interaction
                    std.cnot(qargs[i], qargs[j])
                    std.rz(f"{angle} * time", qargs[j])
                    std.cnot(qargs[i], qargs[j])
                    
                    # Inverse basis rotations
                    std.call_gate(basis_rot, qargs[i], phases=["-pi/2"])
                    std.call_gate(basis_rot, qargs[j], phases=["-pi/2"])
        
        # Add some controlled single-qubit operations for extra complexity
        for i in range(self.reg_size - 1):
            if random.random() < density * 0.3:
                ctrl_gate = random.choice(['cry', 'crx', 'crz'])
                angle = random.uniform(0.1, 1.0)
                std.call_gate(ctrl_gate, qargs[i], qargs[i + 1], phases=[f"{angle} * time"])
                
        std.end_gate()
        # self.call_space = " {}"
        self.merge(*sys.build(),self.name)

    def apply(self, time, qubits):
        """Apply Heisenberg XYZ evolution for given time."""
        self.call_gate(self.name, qubits[-1],qubits[:-1], phases=[time])
        
    def controlled(self, time, qubits, control):
        """Apply controlled Heisenberg evolution."""
        self.controlled_op(self.name, (qubits[-1],[control]+qubits[:-1], time), n=1)
        

class FermionicHubbard(GateLibrary):
    """
    Simplified Fermionic Hubbard Model for testing.
    
    Implements hopping and on-site interaction terms using Jordan-Wigner
    transformation. Creates complex non-local interactions through string
    of Pauli operations.
    """
    name = "FermionicHubbard"
    
    def __init__(self, reg=3, t=1.0, U=2.0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reg_size = reg
        self.t = t  # Hopping parameter
        self.U = U  # On-site interaction
        self.name = f"FermionicHubbard_{self.reg_size}q_t{int(100*t)}_U{int(100*U)}"
        
        names = string.ascii_letters
        qargs = [names[i // len(names)] + names[i % len(names)] 
                for i in range(self.reg_size)]
        
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        std.call_space = " {}"
        
        std.begin_gate(self.name, qargs, params=["time"])
        
        # Hopping terms with Jordan-Wigner strings
        for i in range(self.reg_size - 1):
            # Forward hopping: c†_i c_{i+1}
            # Implement as (X_i - iY_i)(X_{i+1} + iY_{i+1})/4 with JW string
            
            # Apply Jordan-Wigner Z string between sites
            for k in range(i + 1, i + 1):  # No string needed for nearest neighbor
                pass
            
            # XX term
            std.ry("pi/2", qargs[i])
            std.ry("pi/2", qargs[i + 1])
            std.cnot(qargs[i], qargs[i + 1])
            std.rz(f"{self.t} * time", qargs[i + 1])
            std.cnot(qargs[i], qargs[i + 1])
            std.ry("-pi/2", qargs[i])
            std.ry("-pi/2", qargs[i + 1])
            
            # YY term (with opposite sign)
            std.rx("-pi/2", qargs[i])
            std.rx("-pi/2", qargs[i + 1])
            std.cnot(qargs[i], qargs[i + 1])
            std.rz(f"{self.t} * time", qargs[i + 1])
            std.cnot(qargs[i], qargs[i + 1])
            std.rx("pi/2", qargs[i])
            std.rx("pi/2", qargs[i + 1])
            
            # XY term
            std.ry("pi/2", qargs[i])
            std.rx("-pi/2", qargs[i + 1])
            std.cnot(qargs[i], qargs[i + 1])
            std.rz(f"-{self.t} * time", qargs[i + 1])
            std.cnot(qargs[i], qargs[i + 1])
            std.ry("-pi/2", qargs[i])
            std.rx("pi/2", qargs[i + 1])
            
            # YX term
            std.rx("-pi/2", qargs[i])
            std.ry("pi/2", qargs[i + 1])
            std.cnot(qargs[i], qargs[i + 1])
            std.rz(f"{self.t} * time", qargs[i + 1])
            std.cnot(qargs[i], qargs[i + 1])
            std.rx("pi/2", qargs[i])
            std.ry("-pi/2", qargs[i + 1])
        
        # On-site interaction terms: U n_i n_j (for different spin species)
        # Simplified as local Z rotations
        for i in range(0, self.reg_size - 1, 2):  # Assume even sites are spin up
            if i + 1 < self.reg_size:  # Adjacent site is spin down
                # Implement as ZZ interaction
                std.cnot(qargs[i], qargs[i + 1])
                std.rz(f"{self.U} * time", qargs[i + 1])
                std.cnot(qargs[i], qargs[i + 1])
                
        std.end_gate()
        # self.call_space = " {}"
        self.merge(*sys.build(),self.name)

    def apply(self, time, qubits):
        """Apply Heisenberg XYZ evolution for given time."""
        self.call_gate(self.name, qubits[-1],qubits[:-1], phases=[time])
        
    def controlled(self, time, qubits, control):
        """Apply controlled Heisenberg evolution."""
        self.controlled_op(self.name, (qubits[-1],[control]+qubits[:-1], time), n=1)

        
# Test suite factory function
def create_test_hamiltonians(reg_size=4):
    """
    Factory function to create a suite of test Hamiltonians.
    
    Args:
        reg_size: Number of qubits for the test register
        
    Returns:
        Dictionary of Hamiltonian instances for testing
    """
    # test_reg = list(range(reg_size))
    def anonymize(lib,aparams):
        class anon(lib):    
            def __init__(self,*args,**kwargs):
                super().__init__(*aparams,*args,**kwargs)
        return anon
    
    hamiltonians = {
        'tfim': (TransverseFieldIsing,(reg_size, 1.0, 0.7)),  #reg, j , h
        'heisenberg': (HeisenbergXYZ,(reg_size, 1.0, 1.2, 0.8)), # reg, jx , jy, jz
        'random_dense': (RandomizedHamiltonian,(reg_size, 42, 0.8)), #reg, seed, density
        'random_sparse': (RandomizedHamiltonian,(reg_size, 123, 0.4)), #reg, seed, density
        'hubbard': (FermionicHubbard,(reg_size, 1.0, 2.0))  # reg, t, U
    }
    
    return {k : anonymize(v[0],v[1]) for k, v in hamiltonians.items()}
