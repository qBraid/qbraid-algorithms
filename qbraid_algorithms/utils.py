# Copyright 2025 qBraid
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Module containing utility functions for algorithm implementation.

"""
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
    qasm_str = qasm_path.read_text(encoding="utf-8")
    qasm_str = _replace_vars(qasm_str, replacements)
    qasm_path.write_text(qasm_str, encoding="utf-8")


def get_max_count(counts: dict[str, int]) -> tuple[str, int]:
    """
    Get the bitstring with the maximum count from a counts dictionary.

    Args:
        counts (dict[str, int]): A dictionary mapping bitstrings to their counts.

    Returns:
        tuple[str, int]: The bitstring with the maximum count and its count.
    """
    max_bitstring = max(counts, key=lambda k: counts[k])
    max_count = counts[max_bitstring]
    return max_bitstring, max_count
