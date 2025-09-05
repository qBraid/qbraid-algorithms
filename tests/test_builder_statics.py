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
Test Algorithms - Semantic Validation

This module tests the implementations of several semi static algorithms which 
dont accept a arbitrary oracle/hamiltonian.
Tests include:
1. Grovers
2. Toeplitz
3. HHL
"""

# TODO: remove unused variable lint once namespace (ie imports and defs) tests are implemented
# ruff: noqa: F841
# pylint: disable=C0303,unused-variable,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-locals,duplicate-code
import string

import numpy as np
import pyqasm as pq

from qbraid_algorithms.amplitude_amplification import AALibrary
from qbraid_algorithms.embedding import Toeplitz

#package modules
from qbraid_algorithms.qtran import GateBuilder, GateLibrary, QasmBuilder, std_gates
from qbraid_algorithms.rodeo import RodeoLibrary


class Za(GateLibrary):
    """Custom gate: controlled-Z on all qubits except index 2."""
    name = "Z_on_two"
    reg = [*range(3)]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = f"Z_on_two{len(self.reg)}"
        names = string.ascii_letters
        qargs = [
            names[i // len(names)] + names[i % len(names)]
            for i in range(len(self.reg))
        ]

        sys = GateBuilder()
        std = sys.import_library(std_gates)
        std.call_space = " {}"

        ind = dict(zip(range(len(self.reg)), qargs))
        ind.pop(2)

        # Gate definition
        std.begin_gate(self.name, qargs)
        std.x(qargs[2])
        std.controlled_op("z", (qargs[2], list(ind.values())), n=len(self.reg) - 1)
        std.x(qargs[2])
        std.end_gate()

        # Collect gate definitions and imports
        p, i, d = sys.build()
        for imps in i:
            if imps not in self.gate_import:
                self.gate_import.append(imps)

        for defs in d:
            if defs[0] not in self.gate_defs:
                self.gate_defs[defs[0]] = defs[1]

        self.gate_defs[self.name] = p
        self.gate_ref.append(self.name)

    def apply(self, qubits):
        """Apply the custom gate to a set of qubits."""
        self.call_gate(self.name, qubits[-1], qubits[:-1])

    def controlled(self, qubits, control):
        """Controlled version of the custom gate."""
        self.controlled_op(self.name, (qubits[-1], [control] + qubits[:-1]))

class TestGrover:
    def test_full_algorithm_builds(self):
        """Ensure full algorithm builds and pq.loads() runs."""

        # Build algorithm with 3 qubits
        alg = QasmBuilder(3, 0, version="3")
        reg = list(range(3))

        # Import standard gates and Grover
        program = alg.import_library(std_gates)
        ampl = alg.import_library(AALibrary)

        # Add Grover with custom gate
        ampl.grover(Za, reg, 3)

        # Build OpenQASM code
        prog = alg.build()

        # Parse into pq object
        res = pq.loads(prog)

        # Basic assertion
        assert res is not None

        # Validation (commented for now)
        # res.validate()

class TestToeplitz():
    def test_full_algorithm_builds(self):
        """Ensure full algorithm builds and pq.loads() runs."""
        t= np.linspace(0.01, 4*2*np.pi, 8,endpoint=True)
        f = np.sin(t)/t

        # Build algorithm with 3 qubits
        alg = QasmBuilder(3, 0, version="3")
        reg = list(range(3))

        # Import standard gates and Toeplitz
        program = alg.import_library(std_gates)
        toeplitz_lib = alg.import_library(Toeplitz)

        # Add Toeplitz operator
        toeplitz_lib.real_toeplitz(reg,f)

        # Build OpenQASM code
        prog = alg.build()

        # Parse into pq object
        res = pq.loads(prog)

        # Basic assertion
        assert res is not None

        # Validation (commented for now)
        # res.validate()

class TestRodeo():
    def test_mcm_builds(self):
        """Ensure full algorithm builds and pq.loads() runs."""
        t = np.linspace(0.01, 4 * 2 * np.pi, 8, endpoint=True)
        f = np.sin(t) / t

        # Build algorithm with 3 qubits
        alg = QasmBuilder(3, 0, version="3")
        reg = list(range(3))

        # Import standard gates and Rodeo
        program = alg.import_library(std_gates)
        rodeo_lib = alg.import_library(RodeoLibrary)

        # Add Rodeo operator
        rodeo_lib.rodeo_mcm(reg, 1, 3, Za)
        # make sure it doesn't redefine
        rodeo_lib.rodeo_mcm(reg, 1, 3, Za)

        # Build OpenQASM code
        prog = alg.build()

        # Parse into pq object
        res = pq.loads(prog)

        # Basic assertion
        assert res is not None

        # Validation (commented for now)
        # res.validate()

    def test_ancilla_builds(self):
        """Ensure full algorithm builds and pq.loads() runs."""
        t = np.linspace(0.01, 4 * 2 * np.pi, 8, endpoint=True)
        f = np.sin(t) / t

        # Build algorithm with 3 qubits
        alg = QasmBuilder(3, 0, version="3")
        reg = list(range(3))

        # Import standard gates and Rodeo
        program = alg.import_library(std_gates)
        rodeo_lib = alg.import_library(RodeoLibrary)

        # Add Rodeo operator
        rodeo_lib.rodeo(reg, 1, 3, Za)
        # make sure it doesn't redefine
        rodeo_lib.rodeo(reg, 1, 3, Za)

        # Build OpenQASM code
        prog = alg.build()

        # Parse into pq object
        res = pq.loads(prog)

        # Basic assertion
        assert res is not None

        # Validation (commented for now)
        # res.validate()
