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
Generalized Trotterization Module

Implements Suzuki-Trotter decomposition for Hamiltonian evolution using
Suzuki's 1992/2005 recursive symmetric fractal formulation.

The algorithm decomposes the evolution operator exp(-iHt) where H = Hp + Hq
into a sequence of simpler evolution operators that can be implemented
with fractional applications of individual Hamiltonians.

Reference: Suzuki's symmetric decomposition formulas for higher-order
approximations of time evolution operators.

Key features:
- Recursive symmetric fractal structure
- Higher-order accuracy with increased depth
- Requires fractional time evolution of individual Hamiltonians
"""
# TODO: change names from physics notation to python standard naming convention
# pylint: disable=invalid-name,too-many-positional-arguments

from qbraid_algorithms.QTran import GateLibrary, std_gates


class Trotter(GateLibrary):
    """
    Trotter decomposition gate library for Hamiltonian evolution.

    Implements Suzuki's recursive symmetric decomposition for approximating
    exp(-i(Hp + Hq)t) using sequences of exp(-iHp*τ) and exp(-iHq*τ).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def trot_suz(self, qubits, t, Hp, Hq, depth):
        """
        Apply Suzuki-Trotter decomposition for two-Hamiltonian evolution.

        Args:
            qubits: List of qubits to apply evolution to
            t: Evolution time parameter
            Hp: First Hamiltonian gate library (must have 'apply' method)
            Hq: Second Hamiltonian gate library (must have 'apply' method)
            depth: Recursion depth (higher = more accurate, more gates)

        The decomposition approximates exp(-i(Hp + Hq)t) using Suzuki's
        symmetric fractal formula with O(t^(2*depth+1)) error.
        """
        # Generate unique subroutine name
        name = f"trot_suz_{len(qubits)}_{Hp.name}_{Hq.name}_{depth}"  # BUG FIX: Include depth in name


        qubit_list = "{" + ",".join([str(q) for q in qubits]) + "}"
        # Use existing subroutine if available
        if name in self.gate_ref:
            self.call_subroutine(name, [qubit_list, t, depth])
            return name  # BUG FIX: Return subroutine name

        # Get builder reference (operates in root scope)
        sys = self.builder
        std = sys.import_library(std_gates)
        Ha = sys.import_library(Hp)
        Hb = sys.import_library(Hq)

        # Define subroutine signature
        qubit_array_param = f"qubit[{len(qubits)}] qubits"

        std.begin_subroutine(name, [qubit_array_param, "float time", "int recursion_depth"])

        # Register subroutine to prevent infinite recursion
        self.gate_ref.append(name)  # BUG FIX: Should use set or dict for O(1) lookup

        # Base case: depth < 2, use simple first-order Trotter step
        # Formula: exp(-iHp*t/2) * exp(-iHq*t) * exp(-iHp*t/2)
        std.begin_if("recursion_depth < 2")

        # Apply first half of Hp evolution
        Ha.apply("time/2", [f"qubits[{i}]" for i in range(len(qubits))])

        # Apply full Hq evolution
        Hb.apply("time", [f"qubits[{i}]" for i in range(len(qubits))])

        # Apply second half of Hp evolution
        Ha.apply("time/2", [f"qubits[{i}]" for i in range(len(qubits))])

        std.program("return;")
        std.end_if()

        # Recursive case: Suzuki's symmetric decomposition
        # Calculate Suzuki coefficient: Uk = 1/(4 - 4^(1/(2k-1)))
        # BUG FIX: More robust variable naming and type specification
        uk_var = std.add_var("suzuki_coeff",
                           assignment="1.0/(4.0 - pow(4.0, 1.0/(2.0*recursion_depth - 1.0)))",
                           qtype="float")

        # Suzuki's 5-step symmetric decomposition:
        # S_k = U_k * S_{k-1} * U_k * S_{k-1} * (1-4*U_k) * S_{k-1} * U_k * S_{k-1} * U_k * S_{k-1}
        # where S_{k-1} represents the (k-1)th order approximation

        # First U_k * S_{k-1} step
        std.call_subroutine(name, ["qubits", f"{uk_var}*time", "recursion_depth-1"])

        # Second U_k * S_{k-1} step
        std.call_subroutine(name, ["qubits", f"{uk_var}*time", "recursion_depth-1"])

        # Middle (1-4*U_k) * S_{k-1} step (this is the negative weight step)
        std.call_subroutine(name, ["qubits", f"(1.0-4.0*{uk_var})*time", "recursion_depth-1"])

        # Fourth U_k * S_{k-1} step
        std.call_subroutine(name, ["qubits", f"{uk_var}*time", "recursion_depth-1"])

        # Fifth U_k * S_{k-1} step
        std.call_subroutine(name, ["qubits", f"{uk_var}*time", "recursion_depth-1"])

        std.end_subroutine()

        # Execute the subroutine with provided parameters
        self.call_subroutine(name, [qubit_list, t, depth])

        return name

    def multi_trot_suz(self, qubits, t, hamiltonians, depth):
        """
        Apply Suzuki-Trotter decomposition for multiple Hamiltonians.

        For more than two Hamiltonians, recursively pairs them using
        binary tree decomposition.

        Args:
            qubits: List of qubits to apply evolution to
            t: Evolution time parameter
            hamiltonians: List of Hamiltonian gate libraries
            depth: Recursion depth for each pairwise decomposition

        Returns:
            constructed anonymous gatebuilder
        """

        if len(hamiltonians) == 2:
            self.trot_suz(qubits, t, hamiltonians[0], hamiltonians[1], depth)
            class Ha(Trotter):
                '''casting class to abstract hamiltonian interface operation'''
                name = f"M_trot_suz_{abs(hash(hamiltonians[0].name))}_{abs(hash(hamiltonians[1].name))}"
                def apply(self,t,qubits):
                    """abstract hamiltonian apply"""
                    self.trot_suz(qubits, t, hamiltonians[0], hamiltonians[1], depth)
            return Ha

        # For multiple Hamiltonians, use binary tree approach
        # Split into two groups and recursively apply Trotter
        mid = len(hamiltonians) // 2
        left_hams = hamiltonians[:mid]
        right_hams = hamiltonians[mid:]

        # Create composite Hamiltonian subroutines
        left = self.multi_trot_suz(qubits, t, left_hams, depth) if len(left_hams) > 1 else left_hams[0]
        right = self.multi_trot_suz(qubits, t, right_hams, depth) if len(right_hams) > 1 else right_hams[0]

        # Apply Trotter to the two composite groups
        self.trot_suz(qubits, t, left, right, depth)
        m_name = f"M_trot_suz_{abs(hash(left.name))}_{abs(hash(right.name))}"
        class Hb(Trotter):
            '''casting class to abstract hamiltonian interface operation'''
            name = m_name
            def apply(self,t,qubits):
                """abstract hamiltonian apply"""
                self.trot_suz(qubits, t, left, right, depth)
        return Hb

    def trot_linear(self, qubits, t, hamiltonians, steps=1):
        """
        Apply simple first-order linear Trotter decomposition.

        Implements: Prod| exp(-iH_j * t/steps) repeated 'steps' times
        This is the simplest Trotter decomposition with O((t/d)^2) error.

        Args:
            qubits: List of qubits to apply evolution to
            t: Evolution time parameter
            hamiltonians: List of Hamiltonian gate libraries
            steps: Number of Trotter steps (higher = more accurate)

        Returns:
            Name of the constructed subroutine
        """
        ham_names = [H.name for H in hamiltonians]
        name = f"trot_linear_{len(qubits)}_{'_'.join(ham_names)}_{steps}"

        if name in self.gate_ref:
            self.call_subroutine(name, [qubits, t])
            return name

        # Build linear Trotter subroutine
        sys = self.builder
        std = sys.import_library(std_gates)

        # Import all Hamiltonian libraries
        ham_libs = [sys.import_library(H) for H in hamiltonians]

        std.begin_subroutine(name, [f"qubit[{len(qubits)}] qubits", "float time"])
        self.gate_ref.append(name)

        # Apply Trotter steps
        dt_var = std.add_var("dt", assignment=f"time/{steps}", qtype="float")

        for step in range(steps):
            std.comment(f"Trotter step {step + 1}")

            # Apply each Hamiltonian for time dt
            for ham_lib in ham_libs:
                ham_lib.apply(dt_var, [f"qubits[{j}]" for j in range(len(qubits))])

        std.end_subroutine()

        # Execute the subroutine
        qubit_list = "{" + ",".join([str(q) for q in qubits]) + "}"
        self.call_subroutine(name, [qubit_list, t])

        return name
