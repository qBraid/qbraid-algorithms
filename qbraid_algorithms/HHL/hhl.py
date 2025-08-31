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
HHLLibrary class provides an implementation of the HHL (Harrow-Hassidim-Lloyd) quantum algorithm
 for solving linear systems using phase estimation techniques.
Methods:
    HHL(a: list, b: list, clock: list):
        Implements the main steps of the HHL algorithm:
"""

# Importing package modules
# pylint: disable=invalid-name
from qbraid_algorithms.qpe import PhaseEstimationLibrary


class HHLLibrary(PhaseEstimationLibrary):
    '''HHL library using base Phase Estimation implementation'''

    def HHL(self, a: list, b: list, clock: list):
        '''
        Main implementation of the HHL algorithm

        Args:
            a (list): Quantum register for eigenvectors (input state), e.g., list of qubit indices
            b (list): Quantum register for eigenvalues (ancilla for phase estimation), e.g., list of qubit indices
            clock (list): Quantum register for clock qubits used in phase estimation, e.g., list of qubit indices

        Returns:
            None
        '''
        sys = self.builder
        # Access to the quantum circuit builder (assumed to be defined in the parent class)

        # A = sys.import_library(a)

        # operation currently works within main method due to need of inverse op and use of ancillas
        # TODO: refactor this into a full subroutine once complex Hamiltonians for phase estimation are supported
        # rationale: simple evolution can be represented with negative time values,
        # but static Hamiltonians require explicitly implementing the inverse operation

        Phase = sys.import_library(PhaseEstimationLibrary)
        # Import the root Phase Estimation library for local application

        anc_q = sys.claim_qubits(1)
        # Allocate one ancilla qubit

        anc_c = sys.claim_clbits(1)
        # Allocate one classical bit for measurement result storage

        Phase.phase_estimation(b,clock,a)
        # Apply the phase estimation routine with registers (b, clock, a)

        for i in range(len(clock)-1):
            # Apply controlled rotations depending on clock qubits
            # Controlled rotation around Y-axis by angle pi/(2^{i+1}), where i is the clock qubit index
            self.controlled_op("ry", (anc_q[0], clock[i], f'pi/(2^{i+1})'))
            # Controlled rotation around Y-axis, scaling by power of 2 (pi / 2^(i+1))

        Phase.inverse_op(b,clock,a)
        # Apply the inverse of phase estimation to uncompute and restore registers

        self.measure(anc_q,anc_c)
        # Measure the ancilla qubit and store result in the classical bit
