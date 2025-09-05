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
PhaseEstLibrary

This module defines the PhaseEstimationLibrary class, which provides methods for
constructing quantum phase estimation circuits. Supports both static and time-dependent
Hamiltonians, and is designed for direct implementation of classical phase estimation
algorithms. Iterative phase estimation is planned via the Rodeo package.
"""

import string

from qbraid_algorithms.qft import QFTLibrary

# TODO: regularize application of inverse op to another name for abstract hamiltonian
# or let this be acceptable behavior
# pylint: disable=arguments-differ
# mypy: disable_error_code="override,call-arg"
# from GateLibrary import GateLibrary, std_gates
from qbraid_algorithms.qtran import GateBuilder, GateLibrary, std_gates


class PhaseEstimationLibrary(GateLibrary):
    '''
    Library to implement phase estimation circuits directly related to classical
    phase estimation algorithms. Iterative phase estimation will be supported via
    the Rodeo package. This library supports both static and time-dependent Hamiltonians.
    '''
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def phase_estimation(self, qubits:list,spectra:list,hamiltonian, evolution=None):
        """
        Implements the quantum phase estimation algorithm using the provided qubits,
        ancilla clock register (spectra), and Hamiltonian.

        Parameters:
            qubits (list): List of qubits representing the input state.
            spectra (list): List of ancilla qubits used as the clock register.
            hamiltonian: Hamiltonian operator to be applied.
            evolution (optional): Time evolution parameter for time-dependent Hamiltonians.

        Returns:
            str: The name of the generated phase estimation gate.
        """
        # Implementation notes:
        # The current implementation requires gate call results for the Hamiltonian application to keep gate scope.
        # Phase estimation is currently at a limbo being gate level to support a much simpler form of HHL
        # application with an inverse gate call. The ideal procedure for an inverse controlled operation is not
        # yet established within this system and will need to be rewritten when that's established.
        # TODO: Change to work within subroutine scope for improved modularity.

        name = f'P_EST_{len(qubits)}_{hamiltonian.name}'
        if name in self.gate_ref:
            self.call_gate(name,spectra[-1],qubits+spectra[:-1])
            return name
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        ham = sys.import_library(hamiltonian)
        ham.call_space = " {}"
        qft = sys.import_library(QFTLibrary)
        qft.call_space = " {}"
        names = string.ascii_letters
        qargs = [names[int(i/len(names))]+names[i%len(names)] for i in range(len(qubits)+len(spectra))]
        # std.begin_gate(name,[f"qubit[{len(qubits)}] a",f"qubit[{len(spectra)}] b"])
        std.begin_gate(name,qargs)
        for i in range(len(spectra)):
            if evolution is not None:
                ham.controlled(evolution*2**i,qargs[:len(qubits)],qargs[len(qubits)+i])
            else:
                for _ in range(2**i):
                    ham.controlled(qargs[:len(qubits)],qargs[len(qubits)+i])
        qft.QFT(qargs[len(qubits):])
        std.end_gate()

        self.merge(*sys.build(),name)
        self.call_gate(name,spectra[-1],qubits+spectra[:-1])
        return name

    def inverse_op(self, qubits:list,spectra:list,hamiltonian, evolution=None):
        """
        Implements the inverse (reversed) sequence for the application of phase estimation.
        """
        name = f'Pest_INV_{len(qubits)}_{hamiltonian.name}'
        if name in self.gate_ref:
            self.call_gate(name,spectra[-1],qubits+spectra[:-1])
            return name
        sys = GateBuilder()
        std = sys.import_library(std_gates)
        ham = sys.import_library(hamiltonian)
        ham.call_space = " {}"
        qft = sys.import_library(QFTLibrary)
        qft.call_space = " {}"

        names = string.ascii_letters
        qargs = [names[int(i/len(names))]+names[i%len(names)] for i in range(len(qubits)+len(spectra))]
        # std.begin_gate(name,[f"qubit[{len(qubits)}] a",f"qubit[{len(spectra)}] b"])
        std.begin_gate(name,qargs)
        qft.inverse_op(qft.QFT, (qargs[len(qubits):],))
        for i in reversed(range(len(spectra))):
            if evolution is not None:
                ham.controlled(-evolution*2**i,qargs[:len(qubits)],qargs[len(qubits)+i])
            else:
                # Apply controlled gates in reverse order for proper inversion
                for _ in range(2**i):
                    ham.controlled(qargs[:len(qubits)],qargs[len(qubits)+i])
        std.end_gate()

        self.merge(*sys.build(),name)
        self.call_gate(name,spectra[-1],qubits+spectra[:-1])
        return name
