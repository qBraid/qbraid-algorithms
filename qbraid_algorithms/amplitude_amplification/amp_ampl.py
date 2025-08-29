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
from typing import List

from qbraid_algorithms.QTran import GateBuilder, GateLibrary, std_gates


class AALibrary(GateLibrary):
    """
    Amplitude Amplification Library implementing Grover's algorithm and general amplitude amplification.
    
    This library provides quantum algorithms for amplitude amplification, including:
    - Grover's algorithm for unstructured search
    - General amplitude amplification for arbitrary oracles
    
    Both algorithms use the principle of selective phase rotation to amplify desired
    quantum state amplitudes while suppressing unwanted ones.
    """
    
    name = "AmplitudeAmplification"
    
    def __init__(self, *args, **kwargs):
        """Initialize the AALibrary by calling the parent GateLibrary constructor."""
        super().__init__(*args, **kwargs)
        self.name = "AmplAmp"

    def grover(self, H, qubits: List[int], depth: int) -> None:
        """
        Implement Grover's algorithm for quantum search.
        
        Grover's algorithm provides a quadratic speedup for searching unsorted databases.
        It uses amplitude amplification with a specific oracle (H) to amplify the amplitude
        of target states while suppressing others.
        
        The algorithm structure:
        1. Initialize qubits in superposition with Hadamard gates
        2. Repeat depth times:
           - Apply oracle H (marks target states)
           - Apply diffusion operator (inverts amplitudes about average)
        
        Args:
            H: Oracle/Hamiltonian that marks target states
            qubits: List of qubit indices to operate on
            depth: Number of Grover iterations to perform
        """
        # Generate unique subroutine name based on parameters
        name = f'Grover{len(qubits)}{H.name}{depth}'
        
        # Check if subroutine already exists to avoid regeneration
        if name in self.gate_ref:
            qubit_list = "{" + " ,".join(str(i) for i in qubits) + "}"
            self.call_subroutine(name, [self.call_space.format(qubit_list)])
            # Alternative gate-based call (currently commented out):
            # self.call_gate(name, qubits[-1], qubits[:-1])
            return
        
        # Create new gate builder for defining the subroutine
        gate_system = GateBuilder()
        std_library = gate_system.import_library(std_gates)
        std_library.call_space = " {}"
        oracle_library = gate_system.import_library(H)
        
        # NOTE: Alternative gate-based implementation is commented out below.
        # The current subroutine approach keeps generated code compact,
        # whereas gates cannot use loops (would require Python loops instead).
        
        # Alternative gate implementation (commented out):
        # std_library.begin_gate(name, qargs)
        # # Initial superposition
        # [std_library.h(i) for i in qargs]
        # # Grover iteration: Za -> Z0
        # std_library.begin_loop(depth)
        # std_library.comment("Za")
        # oracle_library.apply(qargs)
        # [std_library.h(i) for i in qargs]
        # std_library.comment("Z0")
        # [std_library.x(i) for i in qargs]
        # std_library.controlled_op("z", (qargs[-1], qargs[:-1]), n=len(qubits)-1)
        # [std_library.x(i) for i in qargs]
        # [std_library.h(i) for i in qargs]
        # std_library.end_loop()
        # std_library.end_gate()
        
        # Current subroutine-based implementation
        register = "reg"
        std_library.begin_subroutine(name, [f"qubit[{len(qubits)}] {register}"])
        
        # Initialize all qubits in superposition
        std_library.h(register)
        
        # Main Grover iteration loop
        std_library.begin_loop(depth)
        
        # Apply oracle (marks target states with phase flip)
        std_library.comment("Za")
        oracle_library.apply([f"reg[{i}]" for i in range(len(qubits))])
        
        # Apply diffusion operator (inverts amplitudes about average)
        std_library.h(register)
        std_library.comment("Z0")
        std_library.x(register)  # Flip all qubits
        # Multi-controlled Z gate (phase flip when all qubits are |1⟩)
        std_library.controlled_op("z",(f"{register}[0]", [f"{register}[{i}]" for i in range(len(qubits) - 1)]), 
        n=len(qubits) - 1
        )
        std_library.x(register)  # Flip back
        std_library.h(register)
        
        std_library.end_loop()
        std_library.end_subroutine()
        
        # Build and merge the subroutine into main library
        self.merge(*gate_system.build(), name)
        
        # Call the created subroutine
        qubit_list = "{" + " ,".join(str(i) for i in qubits) + "}"
        self.call_subroutine(name, [self.call_space.format(qubit_list)])

    def amp_ampl(self, Z, H, qubits: List[int], depth: int) -> None:
        """
        Implement general amplitude amplification algorithm.
        
        This is a generalization of Grover's algorithm that works with arbitrary
        oracles Z and state preparation operators H. It amplifies amplitudes of
        states marked by oracle Z after preparation by operator H.
        
        The algorithm structure:
        1. Unapply state preparation Z†
        2. Initialize superposition
        3. Repeat depth times:
           - Apply state preparation H
           - Unapply oracle Z†
           - Apply diffusion operator Z0
           - Apply oracle Z
        
        Args:
            Z: Oracle operator that marks target states
            H: State preparation operator
            qubits: List of qubit indices to operate on
            depth: Number of amplitude amplification iterations
            
        Note:
            There's a bug in the original code where 'z' is used instead of 'Z'
            in the name generation. This is preserved to maintain exact logic.
        """
        name = f'AmplAmp{len(qubits)}{Z.name}{depth}'
        
        # Check if subroutine already exists
        if name in self.gate_ref:
            qubit_list = "{" + " ,".join(str(i) for i in qubits) + "}"
            self.call_subroutine(name, [self.call_space.format(qubit_list)])
            # Alternative gate-based call (currently commented out):
            # self.call_gate(name, qubits[-1], qubits[:-1])
            return
        
        # Create new gate builder for defining the subroutine
        gate_system = GateBuilder()
        std_library = gate_system.import_library(std_gates)
        oracle_z = gate_system.import_library(Z)
        state_prep_h = gate_system.import_library(H)
        
        # NOTE: Alternative gate-based implementations are commented out below.
        # Multiple different approaches were tried during development.
        
        # Alternative gate implementation attempt 1 (commented out):
        # std_library.begin_gate(name, qargs)
        # std_library.call_space = " {} "
        # # Initial superposition
        # [std_library.h(i) for i in qargs]
        # # Amplitude amplification iteration
        # std_library.begin_loop(depth)
        # std_library.comment("Za")
        # state_prep_h.apply(qargs)
        # [std_library.h(i) for i in qargs]
        # std_library.comment("Z0")
        # [std_library.x(i) for i in qargs]
        # std_library.controlled_op("cz", (qargs[-1], qargs[:-1]), n=len(qubits)-2)
        # [std_library.x(i) for i in qargs]
        # [std_library.h(i) for i in qargs]
        # std_library.end_loop()
        # std_library.end_gate()
        
        # Alternative gate implementation attempt 2 (commented out):
        # for _ in range(depth):
        #     std_library.comment("Za")
        #     oracle_z.apply(qargs)
        #     [std_library.h(i) for i in qargs]
        #     std_library.comment("Z0")
        #     print((qargs[-1], qargs[:-1]))  # Debug print
        #     std_library.controlled_op("cp", (qargs[-1], qargs[:-1]), n=len(qubits)-2)
        #     [std_library.h(i) for i in qargs]
        
        # Current subroutine-based implementation
        register = "reg"
        std_library.begin_subroutine(name, [f"qubit[{len(qubits)}] {register}"])
        
        # Initial unapplication of oracle (inverse preparation)
        oracle_z.unapply([f"reg[{i}]" for i in range(len(qubits))])
        
        # Initialize superposition
        std_library.h(register)
        
        # Main amplitude amplification loop
        std_library.begin_loop(depth)
        
        # Apply state preparation operator
        std_library.comment("H")
        state_prep_h.apply([f"reg[{i}]" for i in range(len(qubits))])
        
        # Unapply oracle (Z†)
        std_library.comment("Zp*")
        oracle_z.unapply([f"reg[{i}]" for i in range(len(qubits))])
        
        # Apply diffusion operator (same as Grover)
        std_library.comment("Z0")
        std_library.x(register)
        std_library.controlled_op(
            "z",
            (f"{register}[0]", [f"{register}[{i}]" for i in range(len(qubits) - 1)]),
            n=len(qubits) - 1
        )
        std_library.x(register)
        
        # Reapply oracle (Z)
        std_library.comment("Zp")
        oracle_z.apply([f"reg[{i}]" for i in range(len(qubits))])
        
        std_library.end_loop()
        std_library.end_subroutine()
        
        # Build and merge the subroutine
        self.merge(*gate_system.build(), name)
        
        # Call the created subroutine
        # Alternative gate-based call (commented out):
        # self.call_gate(name, qubits[-1], qubits[:-1])
        qubit_list = "{" + " ,".join(str(i) for i in qubits) + "}"
        self.call_subroutine(name, [self.call_space.format(qubit_list)])