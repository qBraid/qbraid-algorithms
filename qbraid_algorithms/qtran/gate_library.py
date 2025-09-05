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
QasmBuilder Library - OpenQASM Code Generation Framework

This library provides a flexible framework for generating OpenQASM code through
a hierarchical builder pattern. It supports different output formats including
complete quantum circuits, gate definitions, and include files. GateLibrary is
a base framework for macroing gate, import, and algorithm generation and is
built to inject definitions into whatever FileBuilder class it is connected to.

Key (Base) Features:
- Gate application with controls and phases
- Measurements and classical bit operations
- Control flow (loops, conditionals)
- Gate and subroutine definitions
- Code generation and scope management

Class Extensions:
- std_gates
"""
# pylint: disable=too-many-positional-arguments,invalid-name
# im sticking to std_gates as it needs to be viewed as a default name and matches the qasm name
class GateLibrary:
    """
    BASE GATE LIBRARY

    Core class for quantum gate operations and circuit building.
    Provides fundamental operations for:
    - Gate application with controls and phases
    - Measurements and classical bit operations
    - Control flow (loops, conditionals)
    - Gate and subroutine definitions
    - Code generation and scope management

    """

    def __init__(self, gate_import, gate_ref, gate_defs, program_append, builder, annotated=False):
        """
        Initialize the gate library with necessary components.

        Args:
            gate_import: List of imported gate libraries
            gate_ref: List of available gate names
            gate_defs: Dictionary of gate definitions
            program_append: Function to append code to the program
            builder: Reference to the circuit builder
            annotated: Whether to use annotated syntax
        """
        self.gate_import = gate_import      # Libraries to import
        self.gate_ref = gate_ref           # Available gate names
        self.gate_defs = gate_defs         # Gate definitions dictionary
        self.program = program_append      # Function to append code
        self.builder = builder             # Circuit builder reference
        self.annotated = annotated         # Annotation flag
        self.prefix = ""                   # Gate modifier (e.g., "ctrl @")
        self.call_space = "qb[{}]"         # for namespace (e.g. global qubit register vs gate aliases)
        self.name = "GATE_LIB"             # Library identifier

    def call_gate(self, gate, target, controls=None, phases=None, prefix=""):
        """
        GATE APPLICATION

        Apply a quantum gate with optional controls and phase parameters.

        Format: [prefix][gate]([phases]) [controls...] [target];


        Args:
            gate: Name of the gate to apply
            target: Target qubit index
            controls: Control qubit(s) - single int or list
            phases: Phase parameter(s) - single value or list
            prefix: Optional prefix (e.g., for controlled gates)
        """
        # Validate gate exists in current scope
        if gate not in self.gate_ref:
            print(f"stdgates: gate {gate} is not part of visible scope, "
                  f"make sure that this isn't a floating reference / malformed statement, "
                  f"or is at least previously defined within untracked environment definitions")

        # Build gate call string
        call = prefix + str(gate)

        # Add phase parameters if provided
        if phases is not None:
            call += '('
            if isinstance(phases, list):
                call += str(phases[0])  # Fixed: was phase[0]
                for phase in phases[1:]:
                    call += f",{phase}"
            else:
                call += str(phases)
            call += ')'
        call += " "
        # Add control qubits if provided
        if controls is not None:
            if isinstance(controls, list):
                for control in controls:
                    call += self.call_space.format(control) + ","

            else:
                call += self.call_space.format(controls) + ','

        # Add target qubit and complete the statement
        call += self.call_space.format(target) + ";"
        self.program(self.prefix + call)

    def call_subroutine(self,subroutine,parameters,capture=None):
        """
        SUBROUTINE APPLICATION

        Apply a subroutine with parameters and optionally specify a target
        variable to return value to

        Format: [capture] = [subroutine](parameters);


        Args:
            subroutine: Name of the gate to apply
            parameters: list of all parameters to apply
        """
        if subroutine not in self.gate_ref:
            print(f"stdgates: subroutine {subroutine} is not part of visible scope, "
                  f"make sure that this isn't a floating reference / malformed statement, "
                  f"or is at least previously defined within untracked environment definitions")

        call = f"{capture + ' = ' if capture is not None else ''}{subroutine}({', '.join(str(a) for a in parameters)});"
        self.program(call)


    def measure(self, qubits: list, clbits: list):
        """
        MEASUREMENT

        Measure quantum bits and store results in classical bits.

        Format: cb[{clbit_indices}] = measure qb[{qubit_indices}];


        Args:
            qubits: List of qubit indices to measure
            clbits: List of classical bit indices for storing results
        """
        # Format classical and quantum bit indices
        cindex = "cb[{" + str(clbits)[1:-1] + "}]"
        qindex = "qb[{" + str(qubits)[1:-1] + "}]"
        call = f"{cindex} = measure {qindex};"
        self.program(call)

    def comment(self, line: str):
        """
        COMMENTS

         Add comments to the generated code for documentation.
         Supports both single-line (//) and multi-line (/* */) comments.


        Args:
            line: Comment text (can contain newlines for multi-line)
        """
        call = ""
        if "\n" in line:
            # Multi-line comment
            call += "/*\n" + line + "\n*/"
        else:
            # Single-line comment
            call += "//" + line
        self.program(call)

    def begin_if(self, conditional: str):
        """
        CONDITIONAL BLOCK

        Start a conditional execution block.

        Format: if (condition) { ... }


        Args:
            conditional: Boolean expression string
        """
        call = f"if ({conditional})" + "{"
        self.program(call)
        self.builder.scope += 1  # Increase indentation level

    def begin_loop(self, iterator, ident: str = "i"):
        """
        LOOPS

        Start a loop block with various iteration patterns:
        - int: for int i in [0:n]
        - (start, end): for int i in [start:end]
        - (start, step, end): for int i in [start:end:step]
        - string: custom loop syntax

        Args:
            iterator: Loop specification (int, tuple, or string)
            ident: Loop variable identifier
        """
        if isinstance(iterator, int):
            # Simple range from 0 to iterator
            base = "int"
            dom = f"[0:{int(iterator)-1}]"
        elif isinstance(iterator, tuple):
            if len(iterator) == 2:
                if isinstance(iterator[0], str):
                    # Custom type and domain
                    base = iterator[0]
                    dom = iterator[1]
                else:
                    # Range from start to end
                    base = "int"
                    dom = f"[{int(iterator[0])}:{int(iterator[1])}]"
            else:
                # Range with step or custom float range
                if isinstance(iterator[1], int):
                    # Integer range with step
                    base = "int"
                    dom = f"[{int(iterator[0])}:{int(iterator[2])}:{int(iterator[1])}]"
                else:
                    # Float range with explicit values
                    base = "float"
                    r = int(iterator[2])
                    dom = "{" + str([iterator[0] + float(i)/(r-1) for i in range(r)])[1:-1] + "}"
        elif isinstance(iterator, str):
            # Custom loop syntax
            call = "for " + iterator + "{"
            self.program(call)
            self.builder.scope += 1
            return ident
        else:
            print(f"loop has improper parameterization with: {iterator}")
            return None

        call = f"for {base} {ident} in {dom} " + "{"
        self.program(call)
        self.builder.scope += 1
        return ident

    def begin_gate(self, name, qargs, params=None):
        """
        GATE DEFINITION

        Define a custom quantum gate.

        Format: gate name(params) qargs { ... }

        Args:
            name: Gate name
            qargs: Quantum arguments (qubit parameters)
            params: Optional classical parameters
        """
        if name in self.gate_ref:
            print(f"warning: gate {name} replacing existing namespace")
        call = f"gate {name}{'('+','.join(params)+')' if params is not None else ''} {','.join(qargs)}" +"{"
        self.program(call)
        self.builder.scope += 1


    def begin_subroutine(self, name, parameters: list[str], return_type=None):
        """
        SUBROUTINE DEFINITION

        Define a classical subroutine with optional return type.

        Format: def name(parameters) -> return_type { ... }


        Args:
            name: Subroutine name
            parameters: List of parameter names
            return_type: Optional return type specification
        """
        if name in self.gate_ref:
            print(f"warning:  subroutine {name} replacing existing namespace")
        call = f"def {name}({','.join(parameters)}) {' -> ' + return_type if return_type is not None else ''}" + "{"
        self.program(call)
        self.builder.scope += 1

    def close_scope(self):
        """Close the current scope block and decrease indentation level."""
        self.builder.scope -= 1
        self.program("}")

    def end_if(self):
        """End conditional block."""
        self.close_scope()

    def end_loop(self):
        """End loop block."""
        self.close_scope()

    def end_gate(self):
        """End gate definition block."""
        self.close_scope()

    def end_subroutine(self):
        """End subroutine definition block."""
        self.close_scope()

    def controlled_op(self, gate_call, params, n=0):
        """
        CONTROLLED OPERATIONS

        Apply gates with control qubits using the ctrl modifier.

        Format: ctrl(n) @ gate_operation


        Args:
            gate_call: Gate name (string) or gate function
            params: Gate parameters
            n: Number of control qubits
        """
        if isinstance(gate_call, str):
            # Direct gate name - call with control prefix
            self.call_gate(gate_call, *params, prefix=f"ctrl{'' if n == 0 else f'({n})'} @ ")
        else:
            # Gate function - set modifier and call
            self.prefix = f"ctrl{'' if n<2 else f'({n})'} @ "
            gate_call(*params)
            self.prefix = ""

    def inverse_op(self, gate_call, params):
        """
        INVERSE OPERATIONS

        Apply inverse of gute using the inv modifier.

        Format: inv @ gate_operation


        Args:
            gate_call: Gate name (string) or gate function
            params: Gate parameters
        """
        if isinstance(gate_call, str):
            # Direct gate name - call with inv prefix
            self.call_gate(gate_call, *params, prefix="inv @")
        else:
            # Gate function - set modifier and call
            self.prefix = "inv @ "
            gate_call(*params)
            self.prefix = ""

    def add_gate(self, name: str, gate_def: str):
        """
        Add a custom gate definition to the library.

        Args:
            name: Gate name
            gate_def: Gate definition string
        """
        if name in self.gate_ref:
            print(f"warning:  gate {name} replacing existing namespace")
        self.gate_defs[name] = gate_def
        self.gate_ref.append(name)

    def add_var(self,name,assignment = None,qtype= None):
        '''
        simple stub for programatically adding a variable

        Args:
            name: variable name
            Assignment: whatever definition you want as long as it resolves to a string
        '''
        if name in self.gate_ref:
            print(f"warning:  gate {name} replacing existing namespace")
        call = f"{qtype if qtype is not None else 'let'} {name} {f'= {assignment}' if assignment is not None else ''};"
        self.program(call)
        return name

    def merge(self,program,imports,definitions,name):
        """
        Merges data from a built library/GateBuilder into the current library bases scope
        Args:
            program: Gate body which is added into definitions
            imports: all imports the gate depends on
            gate_def: Gate definitions for any child gates/dynamic libraries used

        """
        for imps in imports:
            if imps not in self.gate_import:
                self.gate_import.append(imps)

        for nem, defs in definitions.items():
            if nem not in self.gate_defs:
                self.gate_defs[nem] = defs
        self.gate_defs[name] = program
        self.gate_ref.append(name)


class std_gates(GateLibrary):
    """
    STANDARD GATES LIBRARY

    Implementation of std_lib quantum gates following OpenQASM 3.0 standards.

    Available Gates:
    - Single-qubit: phase, x, y, z, h, s, sdg, sx
    - Two-qubit: cx, cy, cz, cp, crx, cry, crz, swap
    - Multi-qubit: ccx (Toffoli), cswap (Fredkin)
    """

    # Standard gate set from OpenQASM 3.0 specification
    gates = ["phase", "x", "y", "z", "h", "s", "sdg", "sx",
             'rx','ry','rz', 'p',
             'cx', 'cy', 'cz', 'cp', 'crx', 'cry', 'crz', 'cnot',
             'swap', 'ccx', 'cswap']

    name = 'stdgates.inc'  # Standard library file name

    def __init__(self, *args, **kwargs):
        """Initialize standard gates library and register all gates."""
        super().__init__(*args, **kwargs)
        # Import standard gates library if not already imported
        if std_gates.name not in self.gate_import:
            self.gate_import.append(std_gates.name)

        # Register all standard gates
        for gate in std_gates.gates:
            if gate not in self.gate_ref:
                self.gate_ref.append(gate)

    # ═══════════════════════════════════════════════════════════════════════════
    #                           SINGLE-QUBIT GATES
    # ═══════════════════════════════════════════════════════════════════════════

    def phase(self, theta, targ):
        """Apply phase gate: !0⟩>!0⟩, !1⟩>e^(iθ)!1⟩"""
        self.call_gate("phase", targ, phases=theta)

    def x(self, targ):
        """Apply Pauli-X gate (bit flip): !0⟩> !1⟩, !1⟩> !0⟩"""
        self.call_gate('x', targ)

    def y(self, targ):
        """Apply Pauli-Y gate: !0⟩>i!1⟩, !1⟩>-i!0⟩"""
        self.call_gate('y', targ)

    def z(self, targ):
        """Apply Pauli-Z gate (phase flip): !0⟩> !0⟩, !1⟩>-!1⟩"""
        self.call_gate('z', targ)

    def h(self, targ):
        """Apply Hadamard gate: creates superposition"""
        self.call_gate('h', targ)

    def s(self, targ):
        """Apply S gate (phase): !1⟩>i!1⟩"""
        self.call_gate('s', targ)

    def sdg(self, targ):
        """Apply S-dagger gate (inverse phase): !1⟩>-i!1⟩"""
        self.call_gate('sdg', targ)

    def sx(self, targ):
        """Apply square root of X gate"""
        self.call_gate('sx', targ)

    def rx(self,theta,targ):
        """Apply rx gate"""
        self.call_gate("rx", targ, phases=theta)

    def ry(self,theta,targ):
        """Apply ry gate"""
        self.call_gate("ry", targ, phases=theta)

    def rz(self,theta,targ):
        """Apply rz gate"""
        self.call_gate("rz", targ, phases=theta)


    # ═══════════════════════════════════════════════════════════════════════════
    #                           Two-QUBIT GATES
    # ═══════════════════════════════════════════════════════════════════════════
    def cnot(self,control,targ):
        '''Apply CNOT gate'''
        self.call_gate("cnot",targ,controls=control)

    def cry(self,theta,control,targ):
        """Apply controlled ry gate"""
        self.call_gate("cry", targ,controls=control, phases=theta)
