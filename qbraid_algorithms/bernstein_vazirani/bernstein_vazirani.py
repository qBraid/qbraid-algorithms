import autoqasm as aq
from autoqasm.instructions import cnot, h, measure, x
#from qbraid.transpiler.conversions.qasm3 import autoqasm_to_qasm3
import pyqasm

Qasm3Module = pyqasm.modules.qasm3.Qasm3Module


# Secret string
s = "11010" # TODO: let user specify secret string


@aq.subroutine
def oracle():
    """
    Subroutine to implement oracle of Bernstein-Vazirani algorithm.
    Currently implements oracle for fixed hidden string '11010'.
    """
    cnot(0, 5)
    cnot(1, 5)
    cnot(3, 5)

@aq.subroutine
def measure_qubits():
    """
    Subroutine to measure the qubits.
    """
    for i in range(5):
        measure(i)

@aq.subroutine
def prep_ancilla():
    """
    Subroutine to prepare the ancilla qubit.
    """
    x(6)
    h(6)

@aq.main(num_qubits=6)
def bernstein_vazirani():
    """
    Bernstein-Vazirani Algorithm Implementation for hidden string `s`.
    """    
    # Initialize input qubits to |+> state
    for i in range(4):
        h(i)
    # Prepare ancilla qubit
    prep_ancilla()
    oracle()
    # Re-apply Hadamard gates to input qubits
    for i in range(4):
        h(i)
    # Measure input qubits
    measure_qubits()

def load_program() -> Qasm3Module:
    """
    Load the Bernstein-Vazirani circuit as a pyqasm module.
    
    Returns:
        pyqasm module containing the Bernstein-Vazirani circuit
    """
    program = bernstein_vazirani.build()
    return program.to_ir()
    #qasm_str = autoqasm_to_qasm3(program)
   # return pyqasm.loads(qasm_str)