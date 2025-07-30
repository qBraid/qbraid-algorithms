import os
import tempfile
import shutil
from pathlib import Path
import pyqasm 

from ..utils import build_subroutine

PyQASMModule = pyqasm.modules.qasm3.Qasm3Module

def load_program(num_qubits: int) -> PyQASMModule:
    # Load the QFT subroutine and measurement circuits
    temp_dir = tempfile.mkdtemp()
    iqft_src = Path(__file__).parent / "iqft.qasm"
    iqft_sub_src = Path(__file__).parent / "iqft_subroutine.qasm"
    iqft_dst = os.path.join(temp_dir, "iqft.qasm")
    iqft_sub_dst = os.path.join(temp_dir, "iqft_subroutine.qasm")
    shutil.copy(iqft_src, iqft_dst)
    shutil.copy(iqft_sub_src, iqft_sub_dst)
    # Create temporary include file for algorithm-specific variables
    with open(os.path.join(temp_dir, "inputs.inc"), 'w') as file:
        file.write(f'const int[16] qft_size = {num_qubits};')


    # Load the algorithm
    module = pyqasm.load(iqft_dst)

    # Delete the created files
    shutil.rmtree(temp_dir)

    return module


def generate_subroutine(num_qubits) -> None:
    """
    Creates a QFT subroutine module with user-defined number of qubits 
    within user's current working directory.
    """
    iqft_sub_src = Path(__file__).parent / "iqft_subroutine.qasm"
    shutil.copy(iqft_sub_src, os.path.join(os.getcwd(), f"iqft.qasm"))
    # Create include file for variable definition
    with open(os.path.join(os.getcwd(), f"inputs.inc"), 'w') as file:
        file.write(f'const int[16] qft_size = {num_qubits};')

    print(f"Subroutine 'iqft' has been added to {os.path.join(os.getcwd(), 'iqft.qasm')}")