import os
import tempfile
import shutil
from pathlib import Path
import pyqasm
from qbraid_algorithms.utils import _prep_qasm_file

PyQASMModule = pyqasm.modules.qasm3.Qasm3Module

def load_program(num_qubits: int) -> PyQASMModule:
    """
    Load the Inverse Quantum Fourier Transform circuit as a pyqasm module.

    Args:
        num_qubits (int): The number of qubits for the IQFT.
    
    Returns:
        (PyQasm Module) pyqasm module containing the IQFT circuit
    """
    # Load the IQFT QASM files into a staging directory
    temp_dir = tempfile.mkdtemp()
    iqft_src = Path(__file__).parent / "iqft.qasm"
    iqft_sub_src = Path(__file__).parent / "iqft_subroutine.qasm"
    iqft_dst = os.path.join(temp_dir, "iqft.qasm")
    iqft_sub_dst = os.path.join(temp_dir, "iqft_subroutine.qasm")
    shutil.copy(iqft_src, iqft_dst)
    shutil.copy(iqft_sub_src, iqft_sub_dst)

    # Replace variable placeholders with user-defined parameters
    replacements = { "IQFT_SIZE": str(num_qubits) }
    _prep_qasm_file(iqft_sub_dst, replacements)
    _prep_qasm_file(iqft_dst, replacements)

    # Load the algorithm as a pyqasm module
    module = pyqasm.load(iqft_dst)

    # Delete the created files
    shutil.rmtree(temp_dir)

    return module


def generate_subroutine(num_qubits: int) -> None:
    """
    Creates a QFT subroutine module with user-defined number of qubits 
    within user's current working directory.

    Args:
        num_qubits (int): The number of qubits for the IQFT.

    Returns:
        None
    """
    # Copy the IQFT subroutine QASM file to the current working directory
    iqft_src = Path(__file__).parent / "iqft_subroutine.qasm"
    iqft_dst = os.path.join(os.getcwd(), f"iqft.qasm")
    shutil.copy(iqft_src, iqft_dst)

    # Replace variable placeholders with user-defined parameters
    replacements = { "IQFT_SIZE": str(num_qubits) }
    _prep_qasm_file(iqft_dst, replacements)

    print(f"Subroutine 'iqft' has been added to {iqft_dst}")

