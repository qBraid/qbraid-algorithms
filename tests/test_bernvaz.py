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
Tests for Bernstein-Vazirani algorithm implementation.
"""

from pyqasm.modules.base import QasmModule
from qbraid_algorithms import bernstein_vazirani as bv

def test_load_program():
    """Test that load_program correctly returns a pyqasm module object."""
    bv_module = bv.load_program("101")
    assert isinstance(bv_module, QasmModule)
    assert bv_module.num_qubits == 4 # 3 data qubits + 1 ancilla qubit
