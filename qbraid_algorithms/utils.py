import re
import pyqasm

PyQASMModule = pyqasm.modules.qasm3.Qasm3Module

def rename_vars(qasm_str: str) -> str:
    """Rename variables from array values to names (q[0] -> q0)"""
    return re.sub(r"q\[(\d+)\]", r"q\1", qasm_str)

def remove_openqasm(qasm_str: str) -> str:
    """Remove OpenQASM3 and include statements"""
    return re.sub(r'^\s*OPENQASM\s+[^\n]*;?\s*', '', qasm_str)
    
def remove_declarations(qasm_str: str) -> str:
    """Remove bit and qubit declarations"""
    return re.sub(r'^\s*(qubit|bit)\s*\[\s*\d+\s*\]\s*\w+\s*;?\s*$', '', qasm_str, flags=re.MULTILINE)

def build_gate(module: PyQASMModule, gate_name: str = None) -> str:
    """
    Remove measurements, OPENQASM and include statments, and (qu)bit declerations.
    Rename variables, add gate definition line, and format properly for custom gate defintion.
    """
    # Apply transformations that keep it as valid PyQASM module
    module.remove_measurements()
    module.remove_includes()
    module.unroll()
    # Convert to pyqasm string
    qasm_str = pyqasm.dumps(module)
    qasm_str = remove_declarations(qasm_str)
    qasm_str = rename_vars(qasm_str.strip())
    qasm_str = remove_openqasm(qasm_str)

    # Add indent tab
    qasm_str = "\n".join("\t" + line for line in qasm_str.strip().splitlines())
    # Get parameters list
    params = sorted(set(re.findall(r"q\d+", qasm_str)))
    # Add gate definition line
    num_qubits = len(params)
    if gate_name is None:
        gate_name = f"qft_{num_qubits}"
    gate_def = f"gate {gate_name} {', '.join(params)} {{\n{qasm_str}\n}}"
    
    return gate_def, gate_name