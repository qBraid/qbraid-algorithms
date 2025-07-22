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
Oracle-agnostic amplitude amplification implementation.

This script defines an amplitude amplification circuit using AutoQASM,
parameterized by the number of qubits, depth (number of amplification rounds),
and an optional user-defined oracle.

Returns the circuit as a Qasm3Module
"""

import autoqasm as aq
import numpy as np
import pyqasm
from autoqasm.instructions import cphaseshift, h, x

# Qasm3Module: A container for representing OpenQASM 3 circuits using pyqasm
Qasm3Module = pyqasm.modules.qasm3.Qasm3Module


def Amplification(n_qubits: int = 2, depth: int = 2, oracle=None) -> Qasm3Module:
    """
    Creates an amplitude amplification circuit using AutoQASM.

    Args:
        n_qubits (int): Number of qubits used in the circuit.
        depth (int): Number of Grover-like iterations.
        oracle (callable, optional): An AutoQASM subroutine representing the oracle.
                                     If not provided, a default oracle is used.

    Returns:
        Qasm3Module: The compiled OpenQASM3 representation of the circuit.
    """

    # Validate input
    if n_qubits is None or n_qubits < 1:
        raise ValueError(f"n_qubits {n_qubits} is not a valid positive integer")

    # If no oracle is provided, define a default phase oracle
    if oracle is None:
        @aq.subroutine
        def Oracle():
            cphaseshift(0, 1, np.pi)  # Phase shift between qubits 0 and 1
        oracle = Oracle

    # Define the diffusion operator (Z0)
    @aq.subroutine
    def Z0():
        # Apply Hadamard and X gates to all qubits
        for i in aq.range(n_qubits):
            h(i)
            x(i)

        # Apply a controlled phase shift between qubits 0 and 1
        cphaseshift(0, 1, np.pi)

        # Undo the X and Hadamard gates (inverse of above)
        for i in aq.range(n_qubits):
            x(i)
            h(i)

    # Define the main amplitude amplification module
    @aq.main(num_qubits=n_qubits)
    def ampl_module():
        # Initialize all qubits in superposition
        for i in aq.range(n_qubits):
            h(i)

        # Apply amplitude amplification steps (oracle + diffusion)
        for _ in aq.range(depth):
            oracle()
            Z0()

    # Compile the module into qasm code
    boost = ampl_module.build().to_ir()

    return pyqasm.loads(boost)
