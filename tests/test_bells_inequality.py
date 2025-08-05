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
Tests for Bell's inequality module.
"""

from pyqasm.modules.base import QasmModule
from qbraid_algorithms import bells_inequality as bells

def test_load_program():
    """Test that load_program correctly returns a pyqasm module object."""
    bells_module = bells.load_program()
    assert isinstance(bells_module, QasmModule)
    assert bells_module.num_qubits == 6 # test involves 6 qubits
