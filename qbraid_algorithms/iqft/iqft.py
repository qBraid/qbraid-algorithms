import os
import tempfile
import shutil
from pathlib import Path
import pyqasm 

from ..utils import build_subroutine

PyQASMModule = pyqasm.modules.qasm3.Qasm3Module


def load_program(num_qubits: int) -> PyQASMModule:
    # Copy source qasm3 file to temp directory
    temp_dir = tempfile.mkdtemp()
    iqft_src = Path(__file__).parent / "iqft.qasm"
    iqft_dst = os.path.join(temp_dir, "iqft.qasm")
    shutil.copy(iqft_src, iqft_dst)
    # Create include file in temp directory to pass variables
    with open(os.path.join(temp_dir, "iqft.inc"), 'w') as file:
        file.write(f'const int[16] n = {num_qubits};')

    # load the algorithm
    module = pyqasm.load(iqft_dst)

    # delete the created files
    shutil.rmtree(temp_dir)

    return module


def generate_subroutine(num_qubits: int, subroutine_name: str = "iqft", filename:str = "iqft.inc"):
    """Generate a subroutine-version of IQFT circuit, and return the name of the include file
    and subroutine for use in other programs
    """
    program = load_program(num_qubits)
    subroutine_def, subroutine_name = build_subroutine(program, num_qubits, f'{subroutine_name}_{num_qubits}')
    with open(filename, "w") as f:
        f.write(subroutine_def)
    
    print(f"Subroutine '{subroutine_name}' has been added to {os.path.join(os.getcwd(), filename)}")