import re
from pathlib import Path


def _replace_vars(qasm_str: str, replacements: dict[str, str]) -> str:
    """
    Replaces variables in a QASM string with user-defined parameters.

    Args:
        qasm_str (str): The QASM string containing variable placeholders.
        replacements (dict[str, str]): A dictionary mapping variable names to
        their string values.
    
    Returns:
        str: The QASM string with variables replaced by their values.
    """
    for var, value in replacements.items():
        qasm_str = re.sub(rf"\b{var}\b", value, qasm_str)
    return qasm_str


def _prep_qasm_file(path: str, replacements: dict[str, str]) -> None:
    """
    Prepares a QASM file by replacing variable placeholders with 
    user-defined parameters. Modifies the file in place.

    Args:
        path (str): Path to the QASM file to be processed.
        replacements (dict[str, str]): A dictionary mapping variable names to
        their string values.

    Returns:
        None
    """
    qasm_path = Path(path)
    qasm_str = qasm_path.read_text()
    qasm_str = _replace_vars(qasm_str, replacements)
    qasm_path.write_text(qasm_str)