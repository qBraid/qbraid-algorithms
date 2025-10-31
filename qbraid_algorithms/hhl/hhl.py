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
Harrow-Hassidim-Lloyd (HHL) Algorithm Implementation

"""

# Importing package modules
# pylint: disable=invalid-name
from typing import Any

from qbraid_algorithms.qpe import PhaseEstimationLibrary
from qbraid_algorithms.qtran import std_gates


class HHLLibrary(PhaseEstimationLibrary):
    """HHL library using base Phase Estimation implementation"""

    def HHL(self, a: Any, b: list, clock: list):  # pylint: disable=too-many-locals
        """
        Main implementation of the HHL algorithm

        Args:
            a (Any): Hamiltonian operator to be applied (Matrix - 'A').
            b (list): List of qubits representing the input state (Vector - 'b').
            clock (list): List of ancilla qubits used as the clock register.

        Returns:
            None
        """
        sys = self.builder
        # Access to the quantum circuit builder (assumed to be defined in the parent class)

        # A = sys.import_library(a)

        # operation currently works within main method due to need of inverse op and use of ancillas
        # TODO: refactor this into a full subroutine once complex Hamiltonians for phase estimation are supported
        # rationale: simple evolution can be represented with negative time values,
        # but static Hamiltonians require explicitly implementing the inverse operation

        if sys.qubits != len(b) + len(clock):
            raise ValueError(
                f"System qubits ({sys.qubits}) do not match the number of qubits in "
                f"the input state ({len(b)}) and clock ({len(clock)})"
            )

        # Check for duplicates within b and clock
        b_duplicates = [x for x in set(b) if b.count(x) > 1]
        clock_duplicates = [x for x in set(clock) if clock.count(x) > 1]
        overlap = list(set(b) & set(clock))

        if b_duplicates:
            raise ValueError(
                f"Input state {b} contains duplicate qubits {b_duplicates}"
            )
        if clock_duplicates:
            raise ValueError(
                f"Clock register {clock} contains duplicate "
                f"qubits {clock_duplicates}"
            )
        if overlap:
            raise ValueError(
                f"Input state {b} and clock register {clock} "
                f"contain overlapping qubits {overlap}"
            )

        # Validate qubit index ranges
        max_qubit_index = sys.qubits - 1
        invalid_b = [q for q in b if q > max_qubit_index or q < 0]
        invalid_clock = [q for q in clock if q > max_qubit_index or q < 0]

        if invalid_b:
            raise ValueError(
                f"Input state qubit indices {invalid_b} are "
                f"out of range for system qubits ({max_qubit_index})"
            )
        if invalid_clock:
            raise ValueError(
                f"Clock register qubit indices {invalid_clock} "
                f"are out of range for system qubits ({max_qubit_index})"
            )

        Phase = sys.import_library(PhaseEstimationLibrary)
        # Import the root Phase Estimation library for local application

        anc_q = sys.claim_qubits(1)
        # Allocate one ancilla qubit

        anc_c = sys.claim_clbits(1)
        # Allocate one classical bit for measurement result storage

        Phase.phase_estimation(b, clock, a)
        # Apply the phase estimation routine with registers (b, clock, a)

        sys.import_library(
            std_gates
        )  # Import standard gates library to make gates available

        for i, clock_qubit in enumerate(clock):
            # Apply controlled rotations depending on clock qubits
            # Controlled rotation around Y-axis by angle pi/(2^{i+1}), where i is the clock qubit index
            self.controlled_op("ry", (anc_q[0], clock_qubit, f"pi/(2**{i+1})"))
            # Controlled rotation around Y-axis, scaling by power of 2 (pi / 2^(i+1))

        Phase.inverse_op(b, clock, a)
        # Apply the inverse of phase estimation to uncompute and restore registers

        self.measure(anc_q, anc_c)
        # Measure the ancilla qubit and store result in the classical bit
