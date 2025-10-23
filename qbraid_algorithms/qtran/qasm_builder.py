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
complete quantum circuits, gate definitions, and include files.
Built on top of the the root FileBuilder class which seperates text content from
structure/semantics requirements unique to each file

Key Features:

    - Automatic scope and indentation management
    - Library import and gate definition tracking
    - Multiple output formats (QASM circuits, includes, gate definitions)
    - Resource allocation for qubits and classical bits
    - Extensible design for custom quantum libraries

Class Extensions:
    - GateBuilder
    - QasmBuilder
    - IncludeBuilder
"""


class FileBuilder:
    """
    Base class for all OpenQASM code builders.

    Provides core functionality for managing imports, gate definitions,
    program content, and scope tracking. This class serves as the foundation
    for specialized builders that generate different types of OpenQASM output.

    The FileBuilder maintains several key data structures:

        - imports: List of library files to include
        - gate_defs: Dictionary mapping gate names to their definitions
        - gate_refs: List of available gate names for validation
        - program: Accumulated program code with proper indentation
        - scope: Current nesting level for proper code formatting
    """

    def __init__(self):
        """
        Initialize the base file builder with empty data structures.

        Sets up the foundational components needed for code generation:

            - Empty import list for library dependencies
            - Empty gate definitions dictionary for custom gates
            - Empty gate references list for scope validation
            - Empty program string for accumulating generated code
            - Zero scope level for proper indentation tracking
        """
        self.imports = []  # List of library names to import (e.g., "std_gates.inc")
        self.gate_defs = {}  # Dictionary mapping gate names to definition strings
        self.gate_refs = []  # List of available gate names for validation
        self.program = ""  # Accumulated OpenQASM program code
        self.scope = 0  # Current indentation/nesting level

    def import_library(self, lib_class, annotated=False):
        """
        Import and initialize a quantum gate library.

        This method creates an instance of the specified library class and connects
        it to the current builder's data structures. The library gains access to
        the builder's import list, gate references, definitions, and program
        appending functionality.

        Args:
            lib_class: The library class to instantiate (e.g., std_gates)
            annotated: Whether to enable annotated syntax mode

        Returns:
            Configured library instance ready for use

        Example:
            program = builder.import_library(std_gates)
            program.x(0)  # Apply X gate to qubit 0
        """
        return lib_class(
            gate_import=self.imports,  # Share import list with library
            gate_ref=self.gate_refs,  # Share gate references for validation
            gate_defs=self.gate_defs,  # Share gate definitions dictionary
            program_append=self.program_append,  # Provide code appending function
            builder=self,  # Pass reference to this builder
            annotated=annotated,  # Set annotation mode
        )

    def program_append(self, line):
        """
        Append a line of code to the program with proper indentation.

        This method handles the formatting of generated code by applying
        the appropriate indentation level based on the current scope.
        Each scope level adds one tab character for proper nesting.

        Args:
            line: The code line to append (without indentation)

        Note:
            Indentation is automatically applied based on self.scope.
            Each scope level contributes one tab character.
        """
        self.program += self.scope * "\t" + line + "\n"


class GateBuilder(FileBuilder):
    """
    Specialized builder for generating gate definition files.

    This builder is designed to create standalone gate definition files
    that can be included in other OpenQASM programs. It focuses on
    generating reusable gate definitions without the overhead of
    complete circuit structure.

    Use cases:

        - Creating custom gate libraries
        - Generating reusable quantum subroutines
        - Building modular quantum components
    """

    def import_library(self, lib_class, annotated=False):
        ret = super().import_library(lib_class, annotated)
        ret.call_space = " {}"
        return ret

    def build(self):
        """
        Generate the final gate definition output.

        Produces a tuple containing the generated program code,
        list of required imports, and dictionary of gate definitions.
        This format is suitable for creating include files or
        embedding in larger programs.

        Returns:
            tuple: (program_code, imports_list, gate_definitions_dict)

        Warnings:
            Prints warning if scope is not zero (unclosed blocks)
        """
        if self.scope != 0:
            print(
                "Warning (GateBuilder): built qasm has unclosed scope, "
                "string will fail compile in native"
            )
        return self.program, self.imports, self.gate_defs


class QasmBuilder(FileBuilder):
    """
    Complete OpenQASM circuit builder for quantum programs.

    This is the primary builder for creating full quantum circuits with
    proper OpenQASM headers, qubit/classical bit declarations, library
    imports, and the complete program structure. It automatically manages
    resource allocation and generates standards-compliant OpenQASM code.

    Features:

        - Automatic OpenQASM version header generation
        - Qubit and classical bit resource management
        - Dynamic resource allocation with claim methods
        - Complete circuit structure generation
        - Library import management
        - Gate definition embedding
    """

    def __init__(self, qubits, clbits=None, version=3):
        """
        Initialize a complete quantum circuit builder.

        Creates a builder configured for generating full OpenQASM programs
        with the specified resources and version compatibility.

        Args:
            qubits: Number of qubits to allocate initially
            clbits: Number of classical bits (defaults to qubit count if None)
            version: OpenQASM version number (default: 3)

        The builder automatically generates appropriate headers and
        resource declarations based on these parameters.
        """
        # Generate OpenQASM version header
        self.qasm_header = f"OPENQASM {version};\n"

        # Initialize quantum resource counters
        self.qubits = qubits
        if clbits is not None:
            self.clbits = clbits
        else:
            # Default classical bits to match qubit count
            self.clbits = qubits

        # Initialize base builder functionality
        super().__init__()

    def claim_qubits(self, number: int):
        """
        Dynamically allocate additional qubits to the circuit.

        This method allows libraries and algorithms to request additional
        quantum resources beyond the initial allocation. It returns the
        indices of the newly allocated qubits for use in gate operations.

        Args:
            number: How many additional qubits to allocate

        Returns:
            list: Indices of the newly allocated qubits

        Example:
            ancilla_qubits = builder.claim_qubits(3)  # Get 3 ancilla qubits
            # ancilla_qubits might be [5, 6, 7] if 5 qubits were already allocated
        """
        # Generate indices for new qubits starting from current count
        indexing = [*range(self.qubits, self.qubits + number)]
        # Update total qubit count
        self.qubits += number
        return indexing

    def claim_clbits(self, number: int):
        """
        Dynamically allocate additional classical bits to the circuit.

        Similar to claim_qubits but for classical bit resources used
        for measurement results and classical computation.

        Args:
            number: How many additional classical bits to allocate

        Returns:
            list: Indices of the newly allocated classical bits

        Example:
            result_bits = builder.claim_clbits(2)  # Get 2 measurement bits
        """
        # Generate indices for new classical bits
        indexing = [*range(self.clbits, self.clbits + number)]
        # Update total classical bit count
        self.clbits += number
        return indexing

    def build(self):
        """
        Generate the complete OpenQASM circuit code.

        Assembles all components into a valid OpenQASM program including:

            1. Version header (OPENQASM 3;)
            2. Include statements for imported libraries
            3. Qubit and classical bit declarations
            4. Custom gate definitions
            5. Main program code

        Returns:
            str: Complete OpenQASM program ready for execution

        The generated code follows this structure:
        ```
        OPENQASM 3;
        include "std_gates.inc";
        qubit[10] qb;
        bit[10] cb;
        // Custom gate definitions
        // Main program code
        ```

        Warnings:
            Prints warning if scope is not zero (unclosed blocks)
        """
        if self.scope != 0:
            print(
                "Warning (QasmBuilder): built qasm has unclosed scope, "
                "string will fail compile in native"
            )

        # Start with version header
        qasm_code = self.qasm_header

        # Add all library includes
        qasm_code += "\n".join(
            f'include "{import_line}";' for import_line in self.imports
        )
        if self.imports:  # Add newline after includes if there are any
            qasm_code += "\n"

        # Add qubit declaration
        circuit_def = f"qubit[{int(self.qubits)}] qb;\n"

        # Add classical bit declaration if needed
        if self.clbits > 0:
            circuit_def += f"bit[{int(self.clbits)}] cb;\n"
        qasm_code += circuit_def

        # Add all custom gate definitions
        for gate_def in self.gate_defs.values():
            qasm_code += gate_def + "\n"

        # Add main program content
        qasm_code += self.program

        return qasm_code


class IncludeBuilder(FileBuilder):
    """
    Builder for generating OpenQASM include files.

    Creates include files that can be imported by other OpenQASM programs.
    These files typically contain gate definitions, constants, and reusable
    subroutines but do not include qubit declarations or main program logic.

    Include files are useful for:

        - Sharing gate definitions across multiple circuits
        - Creating domain-specific gate libraries
        - Modular quantum program development
        - Standardizing common quantum operations
    """

    def build(self):
        """
        Generate the include file content.

        Creates a properly formatted include file containing all
        imported libraries, gate definitions, and associated code.
        The output is suitable for saving as a .inc file and
        including in other OpenQASM programs.

        Returns:
            str: Complete include file content

        Format:
        ```
        include "dependency.inc";
        // Gate definitions
        // Utility code
        ```

        Warnings:
            Prints warning if scope is not zero (unclosed blocks)
        """
        if self.scope != 0:
            print(
                "Warning (IncludeBuilder): built include has unclosed scope, "
                "string will fail compile in native"
            )

        # Initialize with empty string (note: original code had bug with undefined qasm_code)
        qasm_code = ""

        # Add all library includes
        qasm_code += "\n".join(
            f'include "{import_line}";' for import_line in self.imports
        )

        # Add all gate definitions
        for gate_def in self.gate_defs.values():
            qasm_code += gate_def + "\n"

        # Add main program content
        qasm_code += self.program

        return qasm_code
