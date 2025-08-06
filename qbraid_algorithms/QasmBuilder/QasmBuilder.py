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

class FileBuilder():
    def __init__(self):
        self.imports = []  # name -> import statement
        self.gate_defs = {}  # name -> definition string
        self.gate_refs = []  # name -> ref tag to avoid redefining
        self.program = ""
        self.scope = 0

    def import_library(self, lib_class,annotated=False): 
        '''
        setup library module with environent data
        '''
        return lib_class(
            gate_import=self.imports,
            gate_ref=self.gate_refs,
            gate_defs=self.gate_defs,
            program_append=self.program_append,
            builder = self,
            annotated = annotated
        )
    
    def program_append(self, line):
        self.program += self.scope*'\t' +line + "\n"

class GateBuilder(FileBuilder):
    def __init__(self):
        super().__init__()

    def build(self):
        if self.scope != 0:
            print("Warning (GateBuilder): built qasm has unclosed scope, string will fail compile in native")
        return self.program, self.imports, self.gate_defs

class QasmBuilder(FileBuilder):
    def __init__(self,qubits,clbits = None, version=3):
        self.qasm_header = f"OPENQASM {version};\n"
        self.qubits = qubits
        if clbits is not None:
            self.clbits = clbits
        else:
            self.clbits = qubits
        super().__init__()

    def claim_qubits(self,number: int):
        indexing = [*range(self.qubits,self.qubits+number)]
        self.qubits += number
        return indexing

    def claim_clbits(self,number: int):
        indexing = [*range(self.clbits,self.clbits+number)]
        self.clbits += number
        return indexing

    def build(self):
        if self.scope != 0:
            print("Warning (QasmBuilder): built qasm has unclosed scope, string will fail compile in native")
        qasm_code = self.qasm_header
        for import_line in self.imports:
            qasm_code += f"include \"{import_line}\";\n"
        
        circuit_def = f"qubit[{int(self.qubits)}] qb;\n"
        if self.clbits > 0:
            circuit_def += f"bit[{int(self.clbits)}] cb;\n"
        qasm_code += circuit_def
        for gate_def in self.gate_defs.values():
            qasm_code += gate_def + "\n"
        qasm_code += self.program
        return qasm_code
    

class IncludeBuilder(FileBuilder):
    def __init__(self):
        super().__init__()

    def build(self):
        if self.scope != 0:
            print("Warning (IncludeBuilder): built include has unclosed scope, string will fail compile in native")
        for import_line in self.imports:
            qasm_code += f"include {import_line};\n"
        
        for gate_def in self.gate_defs:
            qasm_code += gate_def + "\n"
        qasm_code += self.program
        return qasm_code







    

        
 
