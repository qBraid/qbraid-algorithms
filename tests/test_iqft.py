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
Tests for Inverse Quantum Fourier Transform (IQFT) algorithm implementation.
"""

from pyqasm.modules.base import QasmModule
from qbraid_algorithms import iqft

def test_load_program():
    """Test that load_program correctly returns a pyqasm module object."""
    iqft_module = iqft.load_program(3)
    assert isinstance(iqft_module, QasmModule)
    assert iqft_module.num_qubits == 3
