import os
import tempfile
import shutil
from pathlib import Path
import pyqasm
from qbraid_algorithms.utils import _prep_qasm_file

PyQASMModule = pyqasm.modules.qasm3.Qasm3Module

def load_program(num_qubits: int) -> PyQASMModule:
    """
    Load the Quantum Fourier Transform circuit as a pyqasm module.
    Args:
        num_qubits (int): The number of qubits for the QFT.
        
    Returns:
        (PyQasm Module) pyqasm module containing the QFT circuit
    """
    # Load the QFT QASM files into a staging directory
    temp_dir = tempfile.mkdtemp()
    qft_src = Path(__file__).parent / "qft.qasm"
    qft_sub_src = Path(__file__).parent / "qft_subroutine.qasm"
    qft_dst = os.path.join(temp_dir, "qft.qasm")
    qft_sub_dst = os.path.join(temp_dir, "qft_subroutine.qasm")
    shutil.copy(qft_src, qft_dst)
    shutil.copy(qft_sub_src, qft_sub_dst)

    # Replace variable placeholders with user-defined parameters
    replacements = { "QFT_SIZE": str(num_qubits) }
    _prep_qasm_file(qft_sub_dst, replacements)
    _prep_qasm_file(qft_dst, replacements)

    # Load the algorithm
    module = pyqasm.load(qft_dst)

    # Delete the created files
    shutil.rmtree(temp_dir)

    return module


def generate_subroutine(num_qubits) -> None:
    """
    Creates a QFT subroutine module with user-defined number of qubits 
    within user's current working directory.

    Args:
        num_qubits (int): The number of qubits for the QFT.
    
    Returns:
        None
    """
    # Copy the QFT subroutine QASM file to the current working directory
    qft_src = Path(__file__).parent / "qft_subroutine.qasm"
    qft_dst = os.path.join(os.getcwd(), f"qft.qasm")
    shutil.copy(qft_src, qft_dst)

    # Replace variable placeholders with user-defined parameters
    replacements = { "QFT_SIZE": str(num_qubits) }
    _prep_qasm_file(qft_dst, replacements)

    print(f"Subroutine 'qft' has been added to {qft_dst}")
