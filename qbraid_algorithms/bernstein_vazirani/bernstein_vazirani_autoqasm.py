import autoqasm as aq
from autoqasm.instructions import cnot, h, x, measure
from qbraid import QbraidProvider
from qbraid.programs import register_program_type
from qbraid.transpiler import Conversion, ConversionGraph

s = "11010" # hidden string


@aq.subroutine
def oracle(s: str):
    """
    Subroutine to implement oracle of Bernstein-Vazirani algorithm.
    """
    n = len(s)
    for i, bit in enumerate(s):
        if bit == '1':
            cnot(i, n)

@aq.subroutine
def measure(qubits: list):
    """
    Subroutine to measure the qubits.
    """
    for qubit in qubits:
        measure(qubit)

@aq.subroutine
def prep_ancilla(q: int):
    """
    Subroutine to prepare the ancilla qubit.
    """
    x(q)
    h(q)

@aq.main(num_qubits=len(s))
def bernstein_vazirani(s: str):
    """
    Bernstein-Vazirani Algorithm Implementation for hidden string `s`.
    """
    n = len(s)
    
    # Initialize input qubits to |+> state
    for i in range(n):
        h(i)
    # Prepare ancilla qubit
    prep_ancilla(n)
    oracle(s)
    # Re-apply Hadamard gates to input qubits
    for i in range(n):
        h(i)
    # Measure input qubits
    measure(range(n))

"""
Need to figure out AutoQASM Conversion
"""

provider = QbraidProvider(api_key="YOUR_API_KEY",)
device = provider.get_device('qbraid_qir_simulator')
shots = 10
job = device.run(bernstein_vazirani, shots=shots)
