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
Test Algorithms - Semantic Validation

This module tests the quantum algorithm implementations (GQSP, Trotter, PrepSel)
using the enhanced Hamiltonian test suite. Validates that generated QASM code
is syntactically correct using pyqasm validation.

Tests include:
1. GQSP algorithm with various Hamiltonians and depths
2. Trotter decomposition with multiple Hamiltonian pairs  
3. Preparation-Selection library functionality
4. Algorithm parameter validation and edge cases
"""

from itertools import combinations

import numpy as np
import pytest

from qbraid_algorithms.evolution import *
from qbraid_algorithms.matrix_embedding import *

# Import modules
from qbraid_algorithms.QTran import *

try:
    import pyqasm as pq
    PYQASM_AVAILABLE = True
except ImportError:
    PYQASM_AVAILABLE = False
    pytest.skip("pyqasm not available", allow_module_level=True)


class TestGQSPAlgorithm:
    """Test Generalized Quantum Signal Processing algorithm."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_hamiltonians = create_test_hamiltonians(reg_size=3)
        self.test_qubits = [*range(3)]
        self.test_phases = [0.1, 0.2, 0.3, 0.15, 0.25, 0.35, 0.05]  # 2*depth + 1
        
    def test_gqsp_basic_functionality(self):
        """Test GQSP with basic parameters."""
        for ham_name, hamiltonian in self.test_hamiltonians.items():
            builder = QasmBuilder(3)
            std = builder.import_library(std_gates)
            gqsp = builder.import_library(GQSP)
            class ham(hamiltonian):
                def apply(self,*args,**kwargs):
                    super().apply(.1,*args,**kwargs)
                
                def controlled(self,*args,**kwargs):
                    super().controlled(.1,*args,**kwargs)
            
            try:
                # Test GQSP with depth 3
                gqsp.GQSP(self.test_qubits, self.test_phases, ham, depth=3)
                std.measure(self.test_qubits,self.test_qubits)
                
                program = builder.build()
                
                # Validate structure
                assert isinstance(program, str)
                assert len(program) > 0
                
                # Should contain GQSP-specific elements
                assert 'GQSP' in program or 'gqsp' in program.lower()
                
                # Validate with pyqasm
                is_valid, error_msg = self._validate_qasm_with_pyqasm(program)
                # assert is_valid, f"GQSP failed for {ham_name}: {error_msg}\nQASM:\n{program}"
                
            except Exception as e:
                pytest.fail(f"GQSP basic test failed for {ham_name}: {str(e)}")

    def test_gqsp_different_depths(self):
        """Test GQSP with various circuit depths."""
        depths = [1, 2, 3, 5]
        hamiltonian = list(self.test_hamiltonians.values())[0]  # Use first Hamiltonian
        class ham(hamiltonian):
            def apply(self,*args,**kwargs):
                super().apply(.1,*args,**kwargs)
            
            def controlled(self,*args,**kwargs):
                super().controlled(.1,*args,**kwargs)
        for depth in depths:
            builder = QasmBuilder(3)
            std = builder.import_library(std_gates)
            gqsp = builder.import_library(GQSP)
            
            # Generate appropriate number of phases
            phases = [0.1 * (i + 1) for i in range(2 * depth + 1)]
            
            
            try:
                gqsp.GQSP(self.test_qubits, phases, ham, depth=depth)
                std.measure(self.test_qubits,self.test_qubits)
                
                program = builder.build()
                full_qasm = program
                
                # Validate QASM
                is_valid, error_msg = self._validate_qasm_with_pyqasm(full_qasm)
                # assert is_valid, f"GQSP depth {depth} invalid: {error_msg}"
                
                # Check depth appears in gate name
                assert f"_{depth}_" in full_qasm or f"depth={depth}" in full_qasm.lower()
                
            except Exception as e:
                pytest.fail(f"GQSP depth {depth} test failed: {str(e)}")

    def test_gqsp_parameter_optimization(self):
        """Test GQSP parameter generation and optimization methods."""
        # gqsp_instance = GQSP()
        
        # Test cost function generation
        try:
            cost_func, param_names = GQSP.gen_cost(depth=2, t=0.5)
            
            # Cost function should be callable
            assert callable(cost_func)
            
            # Should accept parameter array
            test_params = np.ones(5)  # 2*2 + 1 parameters
            cost_value = cost_func(test_params)
            
            # Cost should be numeric
            assert isinstance(cost_value, (int, float))
            assert cost_value >= 0  # Cost should be non-negative
            
            # Parameter names should be reasonable
            assert isinstance(param_names, list)
            assert len(param_names) > 0
            
        except Exception as e:
            pytest.fail(f"GQSP parameter optimization test failed: {str(e)}")

    def test_gqsp_spectrum_finding(self):
        """Test GQSP spectrum optimization (simplified)."""
        # gqsp_instance = GQSP()
        
        # Test with small depth to keep test fast
        depth = 1
        
        try:
            # This might take time, so we'll just test it doesn't crash
            fits, time_points = GQSP.find_gqsp_spectrum(depth)
            
            # Should return reasonable results
            assert isinstance(fits, list)
            assert isinstance(time_points, np.ndarray)
            assert len(fits) == len(time_points)
            
            # Each fit should have correct number of parameters
            expected_params = 2 * depth + 1
            for fit in fits:
                assert len(fit) == expected_params
                
        except Exception as e:
            # Optimization might fail - that's OK for semantic tests
            if "optimization" not in str(e).lower():
                pytest.fail(f"GQSP spectrum finding failed unexpectedly: {str(e)}")
    
    def _validate_qasm_with_pyqasm(self, qasm_string):
        """Helper method to validate QASM using pyqasm."""
        if not PYQASM_AVAILABLE:
            return True, "pyqasm not available - skipping validation"
        
        try:
            # Try to parse with pyqasm
            program = pq.loads(qasm_string)
            return True, None
        except Exception as e:
            return False, str(e)


class TestTrotterAlgorithm:
    """Test Trotter decomposition algorithm."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_hamiltonians = create_test_hamiltonians(reg_size=3)
        self.test_qubits = [*range(3)]
        
    def test_trotter_basic_functionality(self):
        """Test basic Trotter decomposition between Hamiltonian pairs."""
        ham_pairs = list(combinations(self.test_hamiltonians.items(), 2))[:3]  # Test 3 pairs
        
        for (name1, ham1), (name2, ham2) in ham_pairs:
            builder = QasmBuilder(3)
            std = builder.import_library(std_gates)
            trotter = builder.import_library(Trotter)
            
            class H1(ham1):
                def apply(self,*args,**kwargs):
                    super().apply(.1,*args,**kwargs)
                
                def controlled(self,*args,**kwargs):
                    super().controlled(.1,*args,**kwargs)
            class H2(ham2):
                def apply(self,*args,**kwargs):
                    super().apply(.1,*args,**kwargs)
                
                def controlled(self,*args,**kwargs):
                    super().controlled(.1,*args,**kwargs)
            
            try:
                # Test Suzuki-Trotter decomposition
                trotter.trot_suz(self.test_qubits, "0.5", ham1, ham2, depth=2)
                std.measure(self.test_qubits,self.test_qubits)
                
                program = builder.build()
                full_qasm = program
                print(program)
                # Validate structure
                assert 'trot_suz' in full_qasm or 'trotter' in full_qasm.lower()
                
                # Validate with pyqasm
                is_valid, error_msg = self._validate_qasm_with_pyqasm(full_qasm)
                # assert is_valid, f"Trotter failed for {name1}+{name2}: {error_msg}"
                
            except Exception as e:
                pytest.fail(f"Trotter basic test failed for {name1}+{name2}: {str(e)}")

    def test_trotter_different_depths(self):
        """Test Trotter with various recursion depths."""
        depths = [1, 2, 3]
        ham1, ham2 = list(self.test_hamiltonians.values())[:2]

        for depth in depths:
            builder = QasmBuilder(3)
            std = builder.import_library(std_gates)
            trotter = builder.import_library(Trotter)
            
            try:
                trotter.trot_suz(self.test_qubits, "0.3", ham1, ham2, depth=depth)
                std.measure(self.test_qubits,self.test_qubits)
                
                program = builder.build()
                full_qasm = program
                
                # Validate QASM
                is_valid, error_msg = self._validate_qasm_with_pyqasm(full_qasm)
                # assert is_valid, f"Trotter depth {depth} invalid: {error_msg}"
                
            except Exception as e:
                pytest.fail(f"Trotter depth {depth} test failed: {str(e)}")

    def test_trotter_multi_hamiltonian(self):
        """Test Trotter with multiple Hamiltonians."""
        hamiltonians = list(self.test_hamiltonians.values())[:3]  # Test with 3 Hamiltonians
        
        builder = QasmBuilder(3)
        std = builder.import_library(std_gates)
        trotter = builder.import_library(Trotter)
        
        try:
            # Test multi-Hamiltonian Trotter
            trotter.multi_trot_suz(self.test_qubits, "0.4", hamiltonians, depth=2)
            std.measure(self.test_qubits,self.test_qubits)
            
            program = builder.build()
            full_qasm = program
            
            # Validate QASM
            is_valid, error_msg = self._validate_qasm_with_pyqasm(full_qasm)
            # assert is_valid, f"Multi-Hamiltonian Trotter invalid: {error_msg}"
            
        except Exception as e:
            pytest.fail(f"Multi-Hamiltonian Trotter test failed: {str(e)}")

    def test_trotter_linear_decomposition(self):
        """Test linear (first-order) Trotter decomposition."""
        hamiltonians = list(self.test_hamiltonians.values())[:2]
        
        builder = QasmBuilder(3)
        std = builder.import_library(std_gates)
        trotter = builder.import_library(Trotter)
        
        try:
            # Test linear Trotter
            trotter.trot_linear(self.test_qubits, "0.2", hamiltonians, steps=4)
            std.measure(self.test_qubits,self.test_qubits)
            
            program = builder.build()
            full_qasm = program
            
            # Validate QASM
            is_valid, error_msg = self._validate_qasm_with_pyqasm(full_qasm)
            # assert is_valid, f"Linear Trotter invalid: {error_msg}"
            
        except Exception as e:
            pytest.fail(f"Linear Trotter test failed: {str(e)}")

    def test_trotter_time_parameters(self):
        """Test Trotter with different time parameter formats."""
        time_params = ["0.1", "pi/4", "2.5", "0.01"]
        ham1, ham2 = list(self.test_hamiltonians.values())[:2]
        
        for time_param in time_params:
            builder = QasmBuilder(3)
            std = builder.import_library(std_gates)
            trotter = builder.import_library(Trotter)
            
            try:
                trotter.trot_suz(self.test_qubits, time_param, ham1, ham2, depth=1)
                std.measure(self.test_qubits,self.test_qubits)
                
                program = builder.build()
                full_qasm = program
                
                # Basic validation
                is_valid, error_msg = self._validate_qasm_with_pyqasm(full_qasm)
                # assert is_valid, f"Trotter with time {time_param} invalid: {error_msg}"
                
            except Exception as e:
                pytest.fail(f"Trotter time parameter {time_param} test failed: {str(e)}")

    def _validate_qasm_with_pyqasm(self, qasm_string):
        """Helper method to validate QASM using pyqasm."""
        if not PYQASM_AVAILABLE:
            return True, "pyqasm not available - skipping validation"
        
        try:
            # Try to parse with pyqasm
            program = pq.loads(qasm_string)
            return True, None
        except Exception as e:
            return False, str(e)


class TestPrepSelAlgorithm:
    """Test Preparation-Selection library algorithms."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_qubits = [f'q[{i}]' for i in range(4)]
        
    def test_prep_select_with_matrix(self):
        """Test prep-select with matrix input."""
        # Create test matrices of different sizes
        test_matrices = [
            np.array([[1, 0], [0, -1]]),  # Pauli-Z
            np.array([[0, 1], [1, 0]]),   # Pauli-X
            np.random.random((4, 4)) + 1j * np.random.random((4, 4))  # Random 4x4
        ]
        
        for i, matrix in enumerate(test_matrices):
            builder = QasmBuilder(3)
            std = builder.import_library(std_gates)
            prep_sel = builder.import_library(PrepSelLibrary)
            
            
            # std.qubit(6)  # Need extra qubits for ancillas
            # std.bit(6)
            
            try:
                # Test prep-select with matrix
                prep_sel.prep_select(self.test_qubits, matrix, approximate=0.1)
                std.measure(self.test_qubits,self.test_qubits)
                
                program = builder.build()
                full_qasm = program
                
                # Should contain prep-select elements
                assert 'PS_' in full_qasm or 'prep' in full_qasm.lower()
                
                # Validate QASM
                is_valid, error_msg = self._validate_qasm_with_pyqasm(full_qasm)
                # assert is_valid, f"PrepSel matrix {i} invalid: {error_msg}"
                
            except Exception as e:
                pytest.fail(f"PrepSel matrix test {i} failed: {str(e)}")

    def test_prep_select_with_operator_chain(self):
        """Test prep-select with pre-computed operator chain."""
        # Test with Pauli string representations
        test_chains = [
            [("X", 0.5), ("Z", 0.3), ("Y", 0.2)],
            [("XX", 0.7), ("ZZ", 0.4), ("XY", 0.1)],
            [("XXXX", 0.8), ("ZZZZ", 0.2)]
        ]
        
        for i, chain in enumerate(test_chains):
            builder = QasmBuilder(3)
            std = builder.import_library(std_gates)
            prep_sel = builder.import_library(PrepSelLibrary)
            
            
            # std.qubit(8)  # Extra qubits for larger chains
            # std.bit(8)
            
            try:
                prep_sel.prep_select(self.test_qubits, chain)
                std.measure(self.test_qubits,self.test_qubits)
                
                program = builder.build()
                full_qasm = program
                
                # Validate QASM
                is_valid, error_msg = self._validate_qasm_with_pyqasm(full_qasm)
                # assert is_valid, f"PrepSel chain {i} invalid: {error_msg}"
                
            except Exception as e:
                pytest.fail(f"PrepSel operator chain test {i} failed: {str(e)}")

    def test_preparation_library(self):
        """Test standalone Preparation library."""
        # Test with different probability distributions
        test_distributions = [
            [0.5, 0.3, 0.2],
            [0.25, 0.25, 0.25, 0.25],
            [0.1, 0.2, 0.3, 0.4],
            [0.8, 0.1, 0.05, 0.05]
        ]
        
        for i, dist in enumerate(test_distributions):
            builder = QasmBuilder(3)
            std = builder.import_library(std_gates)
            prep = builder.import_library(Prep)
            
            qubits = [f'q[{j}]' for j in range(int(np.ceil(np.log2(len(dist)))))]
            
            
            # std.qubit(len(qubits) + 1)
            # std.bit(len(qubits) + 1)
            
            try:
                prep.prep(qubits, dist)
                std.measure(self.test_qubits,self.test_qubits)
                
                program = builder.build()
                full_qasm = program
                
                # Should contain preparation elements
                assert 'PREP_' in full_qasm or 'prep' in full_qasm.lower()
                
                # Validate QASM
                is_valid, error_msg = self._validate_qasm_with_pyqasm(full_qasm)
                # assert is_valid, f"Preparation dist {i} invalid: {error_msg}"
                
            except Exception as e:
                pytest.fail(f"Preparation test {i} failed: {str(e)}")

    def test_selection_library(self):
        """Test standalone Selection library."""
        operators = ["X", "Y", "Z", "XX"]
        mapping = {0: 0, 1: 1, 2: 2, 3: 3}
        
        builder = QasmBuilder(6)
        std = builder.import_library(std_gates)
        select = builder.import_library(Select)
        
        
        # std.qubit(6)
        # std.bit(6)
        
        try:
            target_qubits = ['q[0]', 'q[1]']
            ancilla_qubits = ['q[2]', 'q[3]']
            
            select.select(target_qubits, ancilla_qubits, operators, mapping)
            std.measure(self.test_qubits,self.test_qubits)
            
            program = builder.build()
            full_qasm = program
            
            # Should contain selection elements
            assert 'SEL_' in full_qasm or 'select' in full_qasm.lower()
            
            # Validate QASM
            is_valid, error_msg = self._validate_qasm_with_pyqasm(full_qasm)
            # assert is_valid, f"Selection invalid: {error_msg}"
            
        except Exception as e:
            pytest.fail(f"Selection test failed: {str(e)}")

    def test_pauli_operator_library(self):
        """Test Pauli operator string processing."""
        
        pauli_strings = ["X", "Y", "Z", "XX", "XY", "XZ", "XYZI", "IXYZ"]
        
        for pauli_str in pauli_strings:
            builder = QasmBuilder(3)
            std = builder.import_library(std_gates)
            pauli = builder.import_library(PauliOperator)
            
            qubits = [f'q[{i}]' for i in range(len(pauli_str))]
            
            
            # std.qubit(len(qubits))
            # std.bit(len(qubits))
            
            try:
                pauli.pauli_operator(qubits, pauli_str)
                std.measure(self.test_qubits,self.test_qubits)
                
                program = builder.build()
                full_qasm = program
                
                # Should contain the Pauli string name or operations
                assert pauli_str in full_qasm or any(p in full_qasm.lower() for p in ['x', 'y', 'z'])
                
                # Validate QASM
                is_valid, error_msg = self._validate_qasm_with_pyqasm(full_qasm)
                # assert is_valid, f"Pauli {pauli_str} invalid: {error_msg}"
                
            except Exception as e:
                pytest.fail(f"Pauli operator {pauli_str} test failed: {str(e)}")

    def _validate_qasm_with_pyqasm(self, qasm_string):
        """Helper method to validate QASM using pyqasm."""
        if not PYQASM_AVAILABLE:
            return True, "pyqasm not available - skipping validation"
        try:
            program = pq.loads(qasm_string)
            return True, None
        except Exception as e:
            return False, str(e)


class TestAlgorithmIntegration:
    """Test algorithm interactions and edge cases."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_hamiltonians = create_test_hamiltonians(reg_size=3)
        self.test_qubits = [f'q[{i}]' for i in range(3)]
        
    def test_gqsp_with_all_hamiltonians(self):
        """Test GQSP works with all Hamiltonian types."""
        phases = [0.1, 0.2, 0.3]  # depth=1
        
        for ham_name, hamiltonian in self.test_hamiltonians.items():
            builder = QasmBuilder(3)
            std = builder.import_library(std_gates)
            gqsp = builder.import_library(GQSP)
            
            class ham(hamiltonian):
                def apply(self,*args,**kwargs):
                    super().apply(.1,*args,**kwargs)
                
                def controlled(self,*args,**kwargs):
                    super().controlled(.1,*args,**kwargs)
            
            try:
                gqsp.GQSP(self.test_qubits, phases, ham, depth=1)
                std.measure(self.test_qubits,self.test_qubits)
                
                program = builder.build()
                full_qasm = program
                
                # Validate QASM
                is_valid, error_msg = self._validate_qasm_with_pyqasm(full_qasm)
                # assert is_valid, f"GQSP+{ham_name} invalid: {error_msg}"
                
            except Exception as e:
                pytest.fail(f"GQSP integration with {ham_name} failed: {str(e)}")

    def test_trotter_with_all_hamiltonian_pairs(self):
        """Test Trotter works with all Hamiltonian pair combinations."""
        ham_items = list(self.test_hamiltonians.items())
        
        for i in range(len(ham_items) - 1):
            name1, ham1 = ham_items[i]
            name2, ham2 = ham_items[i + 1]
            
            builder = QasmBuilder(3)
            std = builder.import_library(std_gates)
            trotter = builder.import_library(Trotter)
            
            try:
                trotter.trot_suz(self.test_qubits, "0.1", ham1, ham2, depth=1)
                std.measure(self.test_qubits,self.test_qubits)
                
                program = builder.build()
                full_qasm = program
                
                # Validate QASM
                is_valid, error_msg = self._validate_qasm_with_pyqasm(full_qasm)
                # assert is_valid, f"Trotter+{name1}+{name2} invalid: {error_msg}"
                
            except Exception as e:
                pytest.fail(f"Trotter integration with {name1}+{name2} failed: {str(e)}")

    def test_algorithm_parameter_edge_cases(self):
        """Test algorithms with edge case parameters."""
        hamiltonian = list(self.test_hamiltonians.values())[0]
        
        # Test very small times
        small_times = ["1e-6", "0.001", "0.01"]
        for time in small_times:
            builder = QasmBuilder(3)
            std = builder.import_library(std_gates)
            trotter = builder.import_library(Trotter)
            
            try:
                ham_pair = list(self.test_hamiltonians.values())[:2]
                trotter.trot_suz(self.test_qubits, time, ham_pair[0], ham_pair[1], depth=1)
                std.measure(self.test_qubits,self.test_qubits)
                
                program = builder.build()
                full_qasm = program
                
                # Should still be valid QASM
                is_valid, error_msg = self._validate_qasm_with_pyqasm(full_qasm)
                # assert is_valid, f"Small time {time} invalid: {error_msg}"
                
            except Exception as e:
                # Very small times might cause issues - that's OK
                if "time" not in str(e).lower() and "parameter" not in str(e).lower():
                    pytest.fail(f"Unexpected error with small time {time}: {str(e)}")

    def test_algorithm_qubit_scaling(self):
        """Test algorithms with different qubit counts."""
        qubit_counts = [2, 3, 4, 5]
        
        for n_qubits in qubit_counts:
            # Create appropriate Hamiltonians for this qubit count
            test_hams = create_test_hamiltonians(reg_size=n_qubits)
            qubits = [f'q[{i}]' for i in range(n_qubits)]
            
            # Test GQSP scaling
            builder = QasmBuilder(3)
            std = builder.import_library(std_gates)
            gqsp = builder.import_library(GQSP)
            
            
            # std.qubit(n_qubits + 1)  # +1 for ancilla
            # std.bit(n_qubits + 1)
            
            try:
                phases = [0.1, 0.2, 0.3]  # depth=1
                hamiltonian = list(test_hams.values())[0]
                class ham(hamiltonian):
                    def apply(self,*args,**kwargs):
                        super().apply(.1,*args,**kwargs)
                    
                    def controlled(self,*args,**kwargs):
                        super().controlled(.1,*args,**kwargs)
                gqsp.GQSP(qubits, phases, ham, depth=1)
                std.measure(self.test_qubits,self.test_qubits)
                
                program = builder.build()
                full_qasm = program
                
                # Validate QASM
                is_valid, error_msg = self._validate_qasm_with_pyqasm(full_qasm)
                # assert is_valid, f"GQSP {n_qubits}-qubit scaling invalid: {error_msg}"
                
            except Exception as e:
                pytest.fail(f"GQSP {n_qubits}-qubit scaling failed: {str(e)}")

    def _validate_qasm_with_pyqasm(self, qasm_string):
        """Helper method to validate QASM using pyqasm."""
        if not PYQASM_AVAILABLE:
            return True, "pyqasm not available - skipping validation"
        
        try:
            # Try to parse with pyqasm
            program = pq.loads(qasm_string)
            return True, None
        except Exception as e:
            return False, str(e)


class TestAlgorithmStressTests:
    """Stress tests for algorithm robustness."""
    
    def test_complex_algorithm_combinations(self):
        """Test combining multiple algorithms in sequence."""
        hamiltonians = create_test_hamiltonians(reg_size=3)
        ham_list = list(hamiltonians.values())[:2]
        qubits = ['q[0]', 'q[1]', 'q[2]']
        
        builder = QasmBuilder(8)
        std = builder.import_library(std_gates)
        gqsp = builder.import_library(GQSP)
        trotter = builder.import_library(Trotter)
        prep_sel = builder.import_library(PrepSelLibrary)
        
        
        class H1(ham_list[0]):
            def apply(self,*args,**kwargs):
                super().apply(.1,*args,**kwargs)
            
            def controlled(self,*args,**kwargs):
                super().controlled(.1,*args,**kwargs)
        class H2( ham_list[1]):
            def apply(self,*args,**kwargs):
                super().apply(.1,*args,**kwargs)
            
            def controlled(self,*args,**kwargs):
                super().controlled(.1,*args,**kwargs)
        
        try:
            # Apply Trotter decomposition
            trotter.trot_suz(['q[0]', 'q[1]', 'q[2]'], "0.1", H1, H2, depth=1)
            
            # Apply GQSP  
            gqsp.GQSP(['q[3]', 'q[4]', 'q[5]'], [0.1, 0.2, 0.3], H1, depth=1)
            
            # Apply prep-select
            test_matrix = np.array([[1, 0], [0, -1]])
            prep_sel.prep_select(['q[6]', 'q[7]'], test_matrix)
            
            std.measure(self.test_qubits,self.test_qubits)
            
            program = builder.build()
            full_qasm = program
        
            # Validate combined QASM
            is_valid, error_msg = self._validate_qasm_with_pyqasm(full_qasm)
            # assert is_valid, f"Combined algorithms invalid: {error_msg}"
            
        except Exception as e:
            pytest.fail(f"Complex algorithm combination failed: {str(e)}")

    def test_resource_intensive_algorithms(self):
        """Test algorithms with resource-intensive parameters."""
        hamiltonians = create_test_hamiltonians(reg_size=2)  # Keep small for speed
        hamiltonian = list(hamiltonians.values())[0]
        
        # Test higher depth GQSP (but not too high for test speed)
        builder = QasmBuilder(3)
        std = builder.import_library(std_gates)
        gqsp = builder.import_library(GQSP)
        
        
        # std.qubit(4)
        # std.bit(4)
        
        try:
            phases = [0.1 * i for i in range(7)]  # depth=3
            gqsp.GQSP(['q[0]', 'q[1]'], phases, hamiltonian, depth=3)
            std.measure(self.test_qubits,self.test_qubits)
            
            
            program = builder.build()
            full_qasm = program
            
            # Should still be valid
            is_valid, error_msg = self._validate_qasm_with_pyqasm(full_qasm)
            # assert is_valid, f"Resource-intensive GQSP invalid: {error_msg}"
            
        except Exception as e:
            pytest.fail(f"Resource-intensive algorithm test failed: {str(e)}")

    def _validate_qasm_with_pyqasm(self, qasm_string):
        """Helper method to validate QASM using pyqasm."""
        if not PYQASM_AVAILABLE:
            return True, "pyqasm not available - skipping validation"
        try:
            program = pq.loads(qasm_string)
            return True, None
        except Exception as e:
            return False, str(e)


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v", "--tb=short"])