import os
import tempfile
import shutil
from pathlib import Path
import pyqasm 

PyQASMModule = pyqasm.modules.qasm3.Qasm3Module

def load_program(num_qubits: int) -> PyQASMModule:
    # Load the QFT subroutine and measurement circuits
    temp_dir = tempfile.mkdtemp()
    qft_src = Path(__file__).parent / "qft.qasm"
    qft_sub_src = Path(__file__).parent / "qft_subroutine.qasm"
    qft_dst = os.path.join(temp_dir, "qft.qasm")
    qft_sub_dst = os.path.join(temp_dir, "qft_subroutine.qasm")
    shutil.copy(qft_src, qft_dst)
    shutil.copy(qft_sub_src, qft_sub_dst)
    # Create temporary include file for algorithm-specific variables
    _generate_inputs(num_qubits)

    # Load the algorithm
    module = pyqasm.load(qft_dst)

    # Delete the created files
    shutil.rmtree(temp_dir)

    return module


def generate_subroutine(num_qubits) -> None:
    """
    Creates a QFT subroutine module with user-defined number of qubits 
    within user's current working directory.
    """
    qft_sub_src = Path(__file__).parent / "qft_subroutine.qasm"
    shutil.copy(qft_sub_src, os.path.join(os.getcwd(), f"qft.qasm"))
    # Create include file for variable definition
    _generate_inputs(num_qubits)

    print(f"Subroutine 'qft' has been added to {os.path.join(os.getcwd(), 'qft.qasm')}")


def _generate_inputs(num_qubits: int) -> None:
    """
    Creates an input file for the QFT subroutine with user-defined number of qubits.
    """
    with open(os.path.join(os.getcwd(), f"inputs.inc"), 'w') as file:
        file.write(f'const int[16] qft_size = {num_qubits};')
