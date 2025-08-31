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
'''
Module: rodeo.py
This module implements the Rodeo algorithm for quantum state preparation and
amplitude amplification using the qBraid quantum programming framework.
It provides a specialized quantum gate library, `RodeoLibrary`, which extends the
base `GateLibrary` to support Rodeo-based quantum operations.
Classes:
    RodeoLibrary(GateLibrary):
Dependencies:
    - random
    - string
    - qbraid_algorithms.QTran (GateBuilder, GateLibrary, std_gates)
'''
import random
import string

# pylint: disable=too-many-positional-arguments,too-many-locals
# mypy: disable_error_code="call-arg"
from qbraid_algorithms.QTran import GateBuilder, GateLibrary, std_gates


class RodeoLibrary(GateLibrary):
    """
    A quantum gate library implementing the Rodeo algorithm for quantum state preparation.

    The Rodeo algorithm is a quantum algorithm used for amplitude amplification and
    quantum state preparation. It uses ancilla qubits and controlled operations to
    selectively amplify desired quantum states.
    """
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def rodeo(self, qubits:list,t,depth: int,hamiltonian, evolution=None):
        """
        Implement the Rodeo algorithm with multiple ancilla qubits.

        This method creates a quantum gate that implements the Rodeo algorithm using
        a specified number of ancilla qubits (depth). Each ancilla qubit goes through
        a Hadamard-controlled operation-phase-Hadamard sequence.

        Args:
            qubits: List of qubit indices to operate on. The last qubit is treated specially.
            t: Time evolution parameter for the phase gates
            depth: Number of ancilla qubits to use (also determines algorithm depth)
            hamiltonian: Hamiltonian object defining the controlled evolution
            evolution: Optional parameter to control evolution behavior

        Returns:
            str: Name of the created gate for potential reuse
        """
        name = f'Rodeo{depth}_{len(qubits)}_{hamiltonian.name}'
        anc_q = self.builder.claim_qubits(depth)
        anc_c = self.builder.claim_clbits(depth)
        self.comment(f'rodeo call {name} ancillas q:{anc_q} c:{anc_c}')
        if name in self.gate_ref:
            self.call_gate(name,qubits[-1],anc_q+qubits[:-1],t)
            self.measure(anc_q,anc_c)
            return name
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        std.call_space = " {}"
        ham = sys.import_library(hamiltonian)
        ham.call_space = " {}"
        names = string.ascii_letters
        qargs = [names[int(i/len(names))]+names[i%len(names)] for i in range(len(qubits)+depth)]

        s = [2*random.random()-2 for d in range(depth)]
        std.begin_gate(name,qargs,params='t')
        for i in range(depth):
            std.h(qargs[i])
            if evolution is not None:
                ham.controlled(s[i],qargs[depth:],qargs[i])
                std.phase(f'{s[i]}*{t}',qargs[i])
            else:
                ham.controlled(qargs[depth:],qargs[i])
                std.phase(f'{t}',qargs[i])
            std.h(qargs[i])
        std.end_gate()

        self.merge(*sys.build(),name)

        self.call_gate(name,qubits[-1],anc_q+qubits[:-1],t)
        self.measure(anc_q,anc_c)
        return name

    def rodeo_mcm(self, qubits:list,t,depth: int,hamiltonian, evolution=None):
        """
        Implement the Rodeo algorithm with mid-circuit measurements (MCM).

        This is an optimized version that uses only one ancilla qubit but repeats
        the process multiple times with mid-circuit measurements. The algorithm
        breaks early if a successful measurement is obtained.

        Args:
            qubits: List of qubit indices to operate on. The last qubit is treated specially.
            t: Time evolution parameter for the phase gates
            depth: Number of iterations to perform
            hamiltonian: Hamiltonian object defining the controlled evolution
            evolution: Optional parameter to control evolution behavior

        Returns:
            str: Name of the created gate for potential reuse
        """
        name = f'Rodeo_{len(qubits)}_{hamiltonian.name}'
        anc_q = self.builder.claim_qubits(1)
        anc_c = self.builder.claim_clbits(1)
        self.comment(f'rodeo call {name} ancillas q:{anc_q} c:{anc_c}')
        s = [str(2*random.random()-1) for d in range(depth)]
        # TODO: re-add var once array initializations work so the full cnf of rodeo is actually
        # applied (otherwise its just novel kitaev phase est)
        # ts= self.add_var(
        #     f"R{len(qubits)}_{hamiltonian.name}",
        #     "{"+" ,".join(s)+"}",
        #     type=f"array[float[32],{depth}]"
        # )
        if name in self.gate_ref:
            # self.begin_loop(("float",ts))
            self.begin_loop(depth)
            self.call_gate(name,qubits[-1],anc_q+qubits[:-1],t)
            self.measure(anc_q,anc_c)
            self.begin_if(f"cb{anc_c} == true")
            self.program("break;")
            self.end_if()
            self.end_loop()
            return name

        sys = GateBuilder()
        std = sys.import_library(std_gates)
        std.call_space = " {}"
        ham = sys.import_library(hamiltonian)
        ham.call_space = " {}"
        names = string.ascii_letters
        qargs = [names[int(i/len(names))]+names[i%len(names)] for i in range(len(qubits)+1)]
        std.begin_gate(name,qargs,params='t')
        std.h(qargs[0])
        if evolution is not None:
            ham.controlled(s[0],qargs[1:],qargs[0])
            std.phase(f'{s[0]}*{t}',qargs[0])
        else:
            ham.controlled(qargs[1:],qargs[0])
            std.phase(f'{t}',qargs[0])
        std.h(qargs[0])
        std.end_gate()

        self.merge(*sys.build(),name)

        # self.begin_loop(("float",ts))
        self.begin_loop(depth)
        self.call_gate(name,qubits[-1],anc_q+qubits[:-1],t)
        self.measure(anc_q,anc_c)
        self.begin_if(f"cb{anc_c} == true")
        self.program("break;")
        self.end_if()
        self.end_loop()
        return name
