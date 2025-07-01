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
Bell's Inequality Experiment Implementation

Simple functions for loading and running Bell's inequality circuits.
"""

from pathlib import Path

import pyqasm

from pyqasm.modules.base import QasmModule

def load_program() -> QasmModule:
    """
    Load the Bell's inequality circuit as a pyqasm module.
    
    Returns:
        pyqasm module containing the Bell's inequality circuit
    """
    qasm_path = Path(__file__).parent / "bells_inequality.qasm"
    return pyqasm.load(str(qasm_path))
