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

import math
import autoqasm as aq
import matplotlib.pyplot as plt
import autoqasm as aq
import autoqasm.instructions as ins

# TODO: REPLACE WITH QBRAID LOCALSIM
from braket.devices import LocalSimulator

AQProgram = aq.program.MainProgram

def load_program(num_qubits: int) -> AQProgram: 
    """Load the AutoQASM QFT Program with a specified number of qubits"""
    
    @aq.main(num_qubits=num_qubits)
    def qft():
        """Quantum Fourier Transform"""
        result = aq.BitVar(size=num_qubits)

        for i in aq.range(num_qubits):
            ins.h(i)
            for j in aq.range(i+1, num_qubits):
                k = j - i
                ins.cphaseshift(j, i, (2 * math.pi) / (2 ** (k + 1)))

        for i in aq.range(num_qubits // 2):
            ins.swap(i, num_qubits - i - 1)

        result = ins.measure(range(num_qubits))
    
    return qft



def run_program(program: AQProgram, plot=True, device=None, shots=100):
    """
    Run the QFT circuit on a specified device.
    
    Args:
        program (QasmModule): The QFT circuit to run.
        device: The quantum device to run the circuit on.
        shots (int): Number of shots for the execution.
    
    Returns:
        Result of the execution.
    """
    if device is None:
        # TODO: Replace with qBraid LocalSimulator
        device = LocalSimulator()
    result = device.run(program, shots=1000).result()

    print("Measurement Counts: ", counts)

    if plot:
        plt.bar(counts.keys(), counts.values())
        plt.xlabel("bitstrings")
        plt.ylabel("counts")
        plt.show()

    return result