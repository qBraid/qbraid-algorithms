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
Tests for QAOA implementation.
"""
import os

import networkx as nx
import pyqasm

from qbraid_algorithms import qaoa

from .local_device import LocalDevice


def test_generate_program():
    """Test that generate_program correctly returns a str object."""
    qaoa_module = qaoa.QAOA(5)
    edges = [(0, 1), (0, 2), (0, 4), (1, 2), (2, 3), (3, 4)]
    graph = nx.Graph(edges)
    qaoa_module.setup_maxcut(graph=graph)
    program = qaoa_module.generate_algorithm(2)
    assert isinstance(program, str)
    assert qaoa_module.builder.qubits == 5  # 5 data qubits


def test_unroll():
    """Test that pyqasm unrolls correclty."""
    qaoa_module = qaoa.QAOA(5, use_input=False)
    edges = [(0, 1), (0, 2), (0, 4), (1, 2), (2, 3), (3, 4)]
    graph = nx.Graph(edges)
    qaoa_module.setup_maxcut(graph=graph)
    program = qaoa_module.generate_algorithm(2, param=[1, 2, 3, 4])
    module = pyqasm.loads(program)
    module.unroll()

def test_correct_hamiltonian_from_graph():
    """Test that the cost Hamiltonian for maxcut is generated correctly."""
    qaoa_module = qaoa.QAOA(5)
    edges = [(0, 1), (0, 2)]
    graph = nx.Graph(edges)
    qaoa_module.setup_maxcut(graph=graph)
    program = qaoa_module.generate_algorithm(2)
    assert ("\tcnot qubits[0],qubits[1];\n"+
            "\trz(-2 * gamma) qubits[1];\n"+
            "\tcnot qubits[0],qubits[1];\n"+
            "\tcnot qubits[0],qubits[2];\n"+
            "\trz(-2 * gamma) qubits[2];\n"+
            "\tcnot qubits[0],qubits[2];") in program

def test_use_input():
    """Test the use_input parameter."""
    qaoa_module = qaoa.QAOA(5, use_input=False)
    edges = [(0, 1), (0, 2)]
    graph = nx.Graph(edges)
    qaoa_module.setup_maxcut(graph=graph)
    program = qaoa_module.generate_algorithm(2, param=[1, 2, 3, 4])
    assert "gamma_0 = 1" in program
    assert "alpha_0 = 2" in program
    assert "gamma_1 = 3" in program
    assert "alpha_1 = 4" in program


def test_execution():
    """Test correct execution in local device."""
    device = LocalDevice()
    qaoa_module = qaoa.QAOA(5, use_input=False)
    edges = [(0, 1), (0, 2)]
    graph = nx.Graph(edges)
    qaoa_module.setup_maxcut(graph=graph)
    program = qaoa_module.generate_algorithm(2, param=[1, 2, 3, 4])
    module = pyqasm.loads(program)
    module.unroll()
    program_str = pyqasm.dumps(module)
    _ = device.run(program_str, shots=1000)

def test_x_mixer():
    """Test that the x mixer Hamiltonian is generated correctly."""
    qaoa_module = qaoa.QAOA(8)
    edges = [(0, 1), (0, 2)]
    graph = nx.Graph(edges)
    qaoa_module.setup_maxcut(graph=graph)
    program = qaoa_module.generate_algorithm(2)
    assert ("\trx(2 * alpha) qubits[0];\n"+
	        "\trx(2 * alpha) qubits[1];\n"+
	        "\trx(2 * alpha) qubits[2];") in program

def test_xy_mixer():
    """Test that the x mixer Hamiltonian is generated correctly."""
    qaoa_module = qaoa.QAOA(8)
    edges = [(0, 1), (0, 2)]
    graph = nx.Graph(edges)
    qaoa_module.setup_maxcut(graph=graph)
    qaoa_module.mixer_hamiltonian = qaoa_module.xy_mixer(graph=graph)
    program = qaoa_module.generate_algorithm(2)
    assert ("\tcnot qubits[0],qubits[1];\n"
	        "\trx(-alpha) qubits[1];\n"+
            "\try(-alpha) qubits[1];\n"+
            "\tcnot qubits[0],qubits[1];\n"+
            "\tcnot qubits[0],qubits[2];\n"+
            "\trx(-alpha) qubits[2];\n"+
            "\try(-alpha) qubits[2];\n"+
            "\tcnot qubits[0],qubits[2];") in program