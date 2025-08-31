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
Generalized Quantum Signal Processing (GQSP) Module

Implements quantum signal processing techniques for polynomial approximation
of Hamiltonian functions using controlled rotation gates.

Reference: arXiv:2105.02859 - "Generalized Quantum Signal Processing"

Current implementation uses simplified generation scheme:
{rY(θ_2n) * rZ(θ_2n-1) * (|1⟩⟨1| ⊗ H + |0⟩⟨0| ⊗ I)}^n * rY(θ_0)

This generates arbitrary positive polynomials of H under normalization.
Works well for low-degree polynomials (degree < 5).
"""
# pylint: disable=invalid-name,broad-exception-caught
# mypy: disable_error_code="call-arg"
# mypy: disable_error_code="import-untyped"

import string

import numpy as np
import scipy as scp
import sympy as sp
from scipy.optimize import minimize

from qbraid_algorithms.QTran import GateBuilder, GateLibrary, std_gates


class GQSP(GateLibrary):
    """
    Generalized Quantum Signal Processing gate library.

    Implements GQSP circuits for approximating polynomial functions
    of Hamiltonians using quantum phase processing techniques.
    """

    # Class-level symbolic matrix for GQSP operations
    U = sp.Matrix([[sp.Symbol("id"), 0], [0, sp.Symbol('H')]])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def GQSP(self, qubits, phases, hamiltonian, depth=3):
        """
        Apply Generalized Quantum Signal Processing circuit.

        Args:
            qubits: Target qubits for the operation
            phases: Phase parameters for the GQSP sequence
            hamiltonian: Hamiltonian gate library to apply
            depth: Circuit depth (number of GQSP layers)

        Returns:
            Gate name
        """
        name = f'GQSP_{depth}_{hamiltonian.name}'

        # Claim ancilla resources
        anc_q = self.builder.claim_qubits(1)
        anc_c = self.builder.claim_clbits(1)

        # Use existing gate if available
        if name in self.gate_ref:
            self.call_gate(name,qubits[-1],anc_q+qubits[:-1],phases=phases)
            self.measure(anc_q, anc_c)
            return name  # BUG FIX: Add return statement

        # Build new GQSP gate
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        ham = sys.import_library(hamiltonian)

        # Generate unique qubit and parameter names
        names = string.ascii_letters
        qargs = [names[i // len(names)] + names[i % len(names)]
                for i in range(len(qubits) + 1)]
        angles = [f"θ{names[i]}" for i in range(depth * 2 + 1)]

        std.begin_gate(name, qargs, params=angles)

        # Initial Y-rotation on ancilla
        std.ry(angles[0], qargs[0])

        # GQSP sequence
        for i in range(depth):
            # Controlled Hamiltonian application
            ham.controlled(qargs[1:], qargs[0])

            # Phase gate (assuming 'p' is a phase gate)
            std.call_gate("p", qargs[0], phases=angles[i + 1])

            # Y-rotation
            std.ry(angles[depth + i + 1], qargs[0])

        std.end_gate()  # BUG FIX: Add missing end_gate call

        # Register and apply gate
        self.merge(*sys.build(), name)
        self.call_gate(name,qubits[-1],anc_q+qubits[:-1],phases=phases)
        self.measure(anc_q, anc_c)
        return name

    @staticmethod
    def GQSP_recurse(mat, depth):
        """
        Recursively construct symbolic GQSP matrix expression.

        Args:
            mat: Input symbolic matrix
            depth: Recursion depth

        Returns:
            Symbolic matrix expression for GQSP circuit
        """
        # Y-rotation matrix
        r = sp.Symbol(f'r{depth}')
        qr = sp.Matrix([[sp.cos(r/2), -sp.sin(r/2)],
                       [sp.sin(r/2), sp.cos(r/2)]])

        # Base case: just apply rotation
        if depth <= 0:
            return qr * mat

        # Phase rotation matrix
        p = sp.Symbol(f'p{depth}')
        rp = sp.Matrix([[1, 0], [0, sp.exp(1j * p)]])

        # Recursive GQSP construction
        return qr * rp * GQSP.U * GQSP.GQSP_recurse(mat, depth - 1)

    @staticmethod
    def gen_cost(depth, t=1):
        """
        Generate cost function for GQSP parameter optimization.

        Args:
            depth: Circuit depth
            t: Time parameter for target function

        Returns:
            Cost function and parameter names
        """
        # Get symbolic expression for GQSP circuit
        initial_state = sp.Matrix([[1], [0]])  # BUG FIX: Proper column vector
        expr = GQSP.GQSP_recurse(initial_state, depth)[0]  # Take first component

        # Evaluation points
        time = np.linspace(-1, 1, 50)

        # Target polynomial coefficients (Taylor series approximation)
        poly = np.flip(np.power(1j, range(depth + 1)) /
                      scp.special.factorial(range(depth + 1)))  # BUG FIX: Use scp

        # Extract and sort symbolic variables
        syms = expr.free_symbols
        names = sorted([(str(a), a) for a in syms])
        srefs = [name[1] for name in names]

        # Substitute identity symbol
        expr = expr.subs({srefs[1]: 1})  # substitute 'id' for 1

        # Target reference function
        ref = np.polyval(poly, time * t)

        def cost(x):
            """
            Cost function for parameter optimization.

            Args:
                x: Parameter values to evaluate

            Returns:
                Mean squared error between target and approximation
            """
            # BUG FIX: Handle case where not enough parameters provided
            param_dict = {}
            for i, sym in enumerate(srefs[2:]):  # Skip 'H' and 'id' symbols
                if i < len(x):
                    param_dict[sym] = x[i]

            resolved = expr.subs(param_dict)

            # Create numerical evaluator
            evaluator = sp.lambdify(srefs[0], resolved, "numpy")  # srefs[0] should be 'H'

            try:
                series = evaluator(time)

                # Normalize by first element if non-zero
                if np.abs(series[0]) > 1e-12:
                    series = series / np.abs(series[0])

                # Compute mean squared error
                diff = np.sum(np.abs(series - ref)**2)
                return float(diff)  # BUG FIX: Ensure scalar return

            except (ValueError, TypeError, ZeroDivisionError):
                # Return large penalty for invalid parameter values
                return 1e6

        return cost, names

    @staticmethod
    def find_gqsp_spectrum( depth):
        """
        Find optimal GQSP parameters across a spectrum of time values.

        Args:
            depth: Circuit depth for optimization

        Returns:
            List of optimal parameters and corresponding time points
        """
        # Initialize parameter guess
        x_init = np.ones(2 * depth + 1)
        x_init[0] = 0  # Initial angle often zero
        x_prev = x_init.copy()

        fits = []
        time = np.linspace(-1, 1, 100)

        print(f"Optimizing GQSP parameters for depth {depth}")

        for i, t in enumerate(time):
            if abs(t) < 1e-12:  # Handle t = 0 case
                fits.append(x_init)
                continue

            try:
                # Get cost function for current time
                cost_func = GQSP.gen_cost(depth, t)[0]

                # Optimize parameters
                result = minimize(cost_func, x0=x_prev,
                                method='BFGS',  # BUG FIX: Specify optimization method
                                options={'maxiter': 1000})

                if result.success:
                    fits.append(result.x)

                    # Update initial guess with momentum
                    if i > 0 and t != -1:
                        diff = result.x - x_prev
                        x_prev = result.x + 0.25 * diff  # Momentum factor
                    else:
                        x_prev = result.x
                        if t == -1:
                            print("Reset parameter tracking at t = -1")

                else:
                    # Optimization failed, use previous result
                    print(f"Optimization failed at t = {t:.3f}")
                    fits.append(x_prev)

            except Exception as e:
                print(f"Error at t = {t:.3f}: {e}")
                fits.append(x_prev)

        print(f"GQSP optimization complete. Final cost: {result.fun:.6f}")
        return fits, time
