import os
import tempfile
import shutil
import pyqasm 

from utils import build_gate

PyQASMModule = pyqasm.modules.qasm3.Qasm3Module


def load_program(num_qubits: int) -> PyQASMModule:
    # Copy source qasm3 file to temp directory
    temp_dir = tempfile.mkdtemp()
    qft_src = "qft.qasm" 
    qft_dst = os.path.join(temp_dir, "qft.qasm")
    shutil.copy(qft_src, qft_dst)
    # Create include file in temp directory to pass variables
    with open(os.path.join(temp_dir, "qft.inc"), 'w') as file:
        file.write(f'const int[16] n = {num_qubits};')

    # load the algorithm
    module = pyqasm.load(qft_dst)

    # delete the created files
    shutil.rmtree(temp_dir)

    return module


def generate_gate(num_qubits: int, gate_name: str = None, filename:str = "qft.inc"):
    """Generate a gate-version of QFT circuit, and return the name of the include file
    and gate for use in other programs
    """
    program = load_program(num_qubits)
    program.unroll()
    gate_def, gate_name = build_gate(program, gate_name)
    with open(filename, "w") as f:
        f.write(gate_def)
    
    print(f"Gate '{gate_name}' has been added to {os.path.join(os.getcwd(), filename)}")