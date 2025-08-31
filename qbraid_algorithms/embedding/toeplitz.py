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
Toeplitz and Diagonal Gate Libraries for Quantum Algorithms.

NOTE (WIP, untested): This implementation requires claiming ancilla qubits/clbits 
to operate. Ancilla claiming embeddings are a future completion task once 
QASM subroutines have been fully debugged in PyQASM.

This module provides:
- Toeplitz: real Toeplitz matrix embedding via circulant diagonalization.
- Diagonal: diagonal scaling and phase projection methods.

Dependencies:
    numpy, scipy, qbraid_algorithms (QFTLibrary, GateBuilder, GateLibrary, std_gates)

author: Rhys Takahashi
"""
# pylint: disable=too-many-locals
# mypy: disable_error_code="import-untyped"
import string
from itertools import combinations

import numpy as np
import scipy as scp

from qbraid_algorithms.qft import QFTLibrary
from qbraid_algorithms.QTran import GateBuilder, GateLibrary, std_gates


class Toeplitz(GateLibrary):
    """Gate library for real Toeplitz embeddings via circulant diagonalization."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def real_toeplitz(self, qubits, vals, ancilla=True):
        """
        Build a real Toeplitz operator using circulant diagonalization.

        Args:
            qubits (list): Target qubits for operation.
            vals (array-like): Vector defining Toeplitz structure.
            ancilla (bool): Whether to allocate ancilla qubits/clbits.

        Returns:
            str: Gate name.
        """
        qb = int(np.log2(len(vals)) + 0.01 + (1 if ancilla else 0))
        name = f"r_top_{qb}_{abs(hash(tuple(vals)))}"

        # Claim ancilla qubits/clbits
        anc_q = self.builder.claim_qubits(2 if ancilla else 1)
        anc_c = self.builder.claim_clbits(2 if ancilla else 1)

        # If already defined, just call it
        if name in self.gate_ref:
            self.call_gate(name, qubits[-1], anc_q + qubits[:-1])
            self.measure(anc_q, anc_c)
            return name

        # Construct circulant embedding
        if ancilla:
            if len(np.array(vals).shape) > 1:
                line = np.concatenate((vals[0], [0], np.conj(np.flip(vals[0]))))
            else:
                line = np.concatenate((vals, [0], np.flip(vals)))
            circ_mat = scp.linalg.circulant(line[:-1])
        else:
            if len(np.array(vals).shape) > 1:
                circ_mat = vals
            else:
                line = np.concatenate((vals, [0], np.flip(vals)))
                circ_mat = scp.linalg.circulant(line[:-1])
                circ_mat = circ_mat[:len(vals), :len(vals)]

        # Diagonalize via FFT
        dft = np.fft.fft(np.eye(2 * len(vals)))
        idft = np.fft.ifft(np.eye(2 * len(vals)))
        diag = dft @ circ_mat @ idft
        diag_vals = np.diag(diag)

        # Argument names
        names = string.ascii_letters
        qargs = [
            names[i // len(names)] + names[i % len(names)]
            for i in range(qb + (2 if ancilla else 1))
        ]

        # Build subcircuit
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        diagonal = sys.import_library(Diagonal)
        qft = sys.import_library(QFTLibrary)

        std.begin_gate(name, qargs)
        qft.inverse_op(qft.QFT, (qargs[1:],))
        diagonal.controlled_op(diagonal.diag_scale, (qargs[1:], diag_vals, ([qargs[0]], 0)))
        qft.QFT(qargs[1:])
        std.end_gate()

        self.merge(*sys.build(), name)
        # Finalize
        self.call_gate(name, qubits[-1], anc_q + qubits[:-1])
        self.measure(anc_q, anc_c)
        return name


class Diagonal(GateLibrary):
    """Gate library for diagonal scaling and phase projection."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def diag_scale(self, qubits, vals, anc=None):
        """
        Apply diagonal scaling with optional ancilla qubits.

        Args:
            qubits (list): Target qubits.
            vals (array-like): Scaling values.
            anc (tuple or None): Pre-allocated (anc_qubits, anc_clbits).

        Returns:
            str: Gate name.
        """
        qb = int(np.log2(len(vals)) + 0.01)
        name = f"diag{qb}_s_{abs(hash(tuple(vals)))}"

        # Claim ancilla if none provided
        if anc is None:
            anc_q = self.builder.claim_qubits(1)
            anc_c = self.builder.claim_clbits(1)
        else:
            anc_q, anc_c = anc

        # If already defined
        if name in self.gate_ref:
            self.call_gate(name, qubits[-1], anc_q + qubits[:-1])
            if anc is None:
                self.measure(anc_q, anc_c)
            return name

        # Generate argument names
        names = string.ascii_letters
        qargs = [
            names[i // len(names)] + names[i % len(names)]
            for i in range(len(qubits) + 1)
        ]

        # Normalize values
        norm = np.max(np.abs(vals))
        diag = vals / norm

        # Step 1: Approximate amplitudes using arccos trick
        ddiag = 2 * np.arccos(np.abs(diag))

        # Step 2: Correct residual phase
        phasor = np.angle(diag)
        phase_corr = phasor - ddiag / 2

        # Build subcircuit
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        diagonal = sys.import_library(Diagonal)

        std.begin_gate(name, qargs)
        std.h(qargs[0])
        diagonal.controlled_op(diagonal.diag, (qargs, ddiag), n=1)
        std.h(qargs[0])
        diagonal.diag(qargs[1:], phase_corr)
        std.end_gate()

        self.merge(*sys.build(), name)
        self.call_gate(name, qubits[-1], anc_q + qubits[:-1])
        if anc is None:
            self.measure(anc_q, anc_c)
        return name

    def diag(self, qubits, vals, depth=3):
        """
        Build a diagonal gate with phase decomposition.

        Args:
            qubits (list): Target qubits.
            vals (array-like): Diagonal values.
            depth (int): Phase projector expansion depth.

        Returns:
            str: Gate name.
        """
        print("building diagonal gate:",qubits, vals, depth)
        qb = int(np.log2(len(vals)) + 0.01)
        name = f"diag{qb}_{np.abs(hash(tuple(vals)))}"

        if name in self.gate_ref:
            self.call_gate(name, qubits[-1], qubits[:-1])
            return name

        # Argument names
        names = string.ascii_letters
        qargs = [
            names[i // len(names)] + names[i % len(names)]
            for i in range(qb)
        ]

        # Build subcircuit
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        projection = self.phase_projector(vals, depth)

        std.begin_gate(name, qargs)
        std.x(qargs[0])
        std.call_gate("p",qargs[0],phases=projection[0] )
        std.x(qargs[0])

        # Apply projections
        pindex = 1
        for i in range(depth):
            for c in [list(combo) for combo in combinations(range(qb), i + 1)]:
                if np.abs(projection[pindex]) < 0.1:
                    pindex += 1
                    continue
                if len(c) == 1:
                    std.call_gate("p",qargs[c[0]],phases=projection[pindex] )
                else:
                    std.controlled_op(
                        "p",
                        ( qargs[c[0]], [qargs[n] for n in c[1:]], projection[pindex]),
                        n=len(c) - 1,
                    )
                pindex += 1

        std.end_gate()
        self.merge(*sys.build(), name)
        self.call_gate(name, qubits[-1], qubits[:-1])
        return name

    def phase_projector(self,target, depth):
        """
        Construct a phase projector decomposition.

        Args:
            target (array-like): Target diagonal.
            depth (int): Expansion depth.

        Returns:
            np.ndarray: Projection coefficients.
        """
        qb = int(np.log2(len(target)) + 0.01)
        basis = np.arange(2**qb)
        space = []

        for i in range(depth):
            for c in [list(combo) for combo in combinations(range(qb), i + 1)]:
                r = np.ones(2**qb)
                for e in c:
                    r *= ((basis / (2**e)).astype(int) % 2)

                if i == 0 and c == [0]:
                    space.append(np.logical_xor(r, np.ones(2**qb)))
                space.append(r)

        sysmat = np.linalg.pinv(np.array(space).T)
        return sysmat @ target
