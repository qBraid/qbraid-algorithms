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
Quantum Approximate Optimization Algorithm (QAOA) Implementation

This module provides an implementation of the Quantum Approximate Optimization Algorithm ansatz
for different standard mixer and cost Hamiltonians, namely maximum-cut, maximum clique and minimum vertex cover.
"""
import networkx as nx

from qbraid_algorithms.qtran import QasmBuilder, std_gates

class QAOA:
    """
    Quantum Approximate Optimization Algorithm (QAOA) class used to define cost and mixer Hamiltonians
    and generate QASM programs accordingly.
    """
    def __init__(self, num_qubits : int, qasm_version : int = 3, use_input : bool = True):
        self.builder = QasmBuilder(num_qubits, version=qasm_version)
        self.use_input = use_input
        self.mixer_hamiltonian = ""
        self.cost_hamiltonian = ""
        self.layer_circuit = ""
        self._x_mixer_count = 0
        self._max_clique_cost_count = 0
        self._xy_mixer_count = 0
        self._min_vertex_cover_cost_count = 0
        self._maxcut_cost_count = 0

    def xy_mixer(self, graph : nx.Graph) -> str:
        r"""
        Generate XY mixer Hamiltonian subroutine.
        
        xy_mixer_hamiltonian = $$\frac{1}{2}\sum_{(i,j)\in E(G)} X_iX_j + Y_iY_j$$

        This mixer was introduced in 
        From the Quantum Approximate Optimization Algorithm to a Quantum Alternating Operator Ansatz 
        by Stuart Hadfield, Zhihui Wang, Bryan O’Gorman, 
        Eleanor G. Rieffel, Davide Venturelli, and Rupak Biswas Algorithms 12.2 (2019).
        Args:
            graph : nx.Graph
                Graph that describes the problem
        Returns:
            mixer Hamiltonian subroutine name
        """
        if len(graph.nodes) > self.builder.qubits:
            raise ValueError(
                f"The graph provided has more nodes"
                f"({len(graph.nodes)}) than the qubits initialized ({self.builder.qubits})"
            )

        std = self.builder.import_library(lib_class=std_gates)

        mixer_name = f"qaoa_xy_mixer_{self._xy_mixer_count}_{self.builder.qubits}"
        self._xy_mixer_count += 1

        qubit_array_param = f"qubit[{self.builder.qubits}] qubits"

        alpha = "float alpha"

        std.begin_subroutine(
            mixer_name, [qubit_array_param, alpha]
        )
        old_call_space = std.call_space
        std.call_space = "qubits[{}]"

        for i,j in graph.edges:
            std.cnot(i,j)
            std.rx("-alpha", j)
            std.ry("-alpha", j)
            std.cnot(i,j)
        std.call_space = old_call_space
        std.end_subroutine()

        return mixer_name

    def x_mixer(self, graph : nx.Graph) -> str:
        r"""
        Generate X mixer Hamiltonian subroutine.
        
        x_mixer_hamiltonian = $$\sum_{i} X_i$$
        
        This mixer is used in A Quantum Approximate Optimization Algorithm 
        by Edward Farhi, Jeffrey Goldstone, Sam Gutmann [arXiv:1411.4028].
        Args:
            graph : nx.Graph
                Graph that describes the problem
        Returns:
            mixer Hamiltonian subroutine name
        """
        if len(graph.nodes) > self.builder.qubits:
            raise ValueError(
                f"The graph provided has more nodes"
                f"({len(graph.nodes)}) than the qubits initialized ({self.builder.qubits})"
            )
        std = self.builder.import_library(lib_class=std_gates)

        mixer_name = f"qaoa_x_mixer_{self._x_mixer_count}_{self.builder.qubits}"
        self._x_mixer_count += 1

        qubit_array_param = f"qubit[{self.builder.qubits}] qubits"

        alpha = "float alpha"

        std.begin_subroutine(
            mixer_name, [qubit_array_param, alpha]
        )
        old_call_space = std.call_space
        std.call_space = "qubits[{}]"
        for i in graph.nodes:
            std.rx("2 * alpha", i)
        std.call_space = old_call_space
        std.end_subroutine()

        return mixer_name

    def min_vertex_cover_cost(self, graph : nx.Graph) -> str:
        r"""
        Generate min vertex cover cost Hamiltonian subroutine.
        
        cost_hamiltonian $$3\sum_{(i,j)\in E(G)} (Z_i \otimes Z_j + Z_i + Z_j)-\sum_{i \in V(G)} Z_i$$
        https://openqaoa.entropicalabs.com/problems/minimum-vertex-cover/
        As described in Ising formulations of many NP problems by Andrew Lucas [arXiv:1302.5843]
        Args:
            graph : nx.Graph
                Graph that describes the problem
        Returns:
            Cost Hamiltonian subroutine name
        """
        if len(graph.nodes) > self.builder.qubits:
            raise ValueError(
                f"The graph provided has more nodes"
                f"({len(graph.nodes)}) than the qubits initialized ({self.builder.qubits})"
            )
        std = self.builder.import_library(lib_class=std_gates)

        cost_name = f"qaoa_min_vertex_cover_cost_{self._min_vertex_cover_cost_count}_{self.builder.qubits}"
        self._min_vertex_cover_cost_count += 1

        qubit_array_param = f"qubit[{self.builder.qubits}] qubits"

        gamma = "float gamma"

        # cost hamiltonian $$3\sum_{(i,j)\in E(G)} (Z_i \otimes Z_j + Z_i + Z_j)-\sum_{i \in V(G)} Z_i$$
        std.begin_subroutine(
            cost_name, [qubit_array_param , gamma]
        )
        old_call_space = std.call_space
        std.call_space = "qubits[{}]"
        for i,j in graph.edges:
            std.cnot(i,j)
            std.rz("3 * 2 * gamma", j)
            std.cnot(i,j)
            std.rz("3 * 2 * gamma", i)
            std.rz("3 * 2 * gamma", j)

        for i in graph.nodes:
            std.rz("-2 * gamma", i)
        std.call_space = old_call_space
        std.end_subroutine()

        return cost_name

    def max_clique_cost(self, graph : nx.Graph) -> str:
        r"""
        Generate max clique cost Hamiltonian subroutine.
        
        cost_hamiltonian $$3\sum_{(i,j)\in E(\bar{G})} (Z_i \otimes Z_j - Z_i - Z_j)+\sum_{i \in V(G)} Z_i$$
        As described in Ising formulations of many NP problems by Andrew Lucas [arXiv:1302.5843]
        Args:
            graph : nx.Graph
                Graph that describes the problem
        Returns:
            Cost Hamiltonian subroutine name
        """
        if len(graph.nodes) > self.builder.qubits:
            raise ValueError(
                f"The graph provided has more nodes"
                f"({len(graph.nodes)}) than the qubits initialized ({self.builder.qubits})"
            )
        std = self.builder.import_library(lib_class=std_gates)

        cost_name = f"qaoa_max_clique_cost_{self._max_clique_cost_count}_{self.builder.qubits}"
        self._max_clique_cost_count += 1

        qubit_array_param = f"qubit[{self.builder.qubits}] qubits"

        gamma = "float gamma"

        # cost hamiltonian $$3\sum_{(i,j)\in E(\bar{G})} (Z_i \otimes Z_j - Z_i - Z_j)+\sum_{i \in V(G)} Z_i$$
        std.begin_subroutine(
            cost_name, [qubit_array_param , gamma]
        )
        old_call_space = std.call_space
        std.call_space = "qubits[{}]"
        graph_complement = nx.complement(graph)

        for i,j in graph_complement.edges:
            std.cnot(i,j)
            std.rz("3 * 2 * gamma", j)
            std.cnot(i,j)
            std.rz("-3 * 2 * gamma", i)
            std.rz("-3 * 2 * gamma", j)

        for i in graph.nodes:
            std.rz("2 * gamma", i)
        std.call_space = old_call_space
        std.end_subroutine()

        return cost_name

    def qaoa_maxcut(self, graph : nx.Graph) -> tuple[str, str] :
        r"""
        Generate cost hamiltonian and mixer hamiltonian subroutines.

        cost_hamiltonian = $$\sum_{E(graph)} Z_i \otimes Z_j$$
        This Hamiltonian is decribed in 
        Quantum Approximate Optimization Algorithm for MaxCut: 
        A Fermionic View by Zhihui Wang, Stuart Hadfield, 
        Zhang Jiang, Eleanor G. Rieffel [arXiv:1706.02998].
        
        mixer_hamiltonian = $$\sum_{i} X_i$$
        Args:
            graph : nx.Graph
                Graph that describes the problem
        Returns:
            (mixer, cost) : tuple[str, str] mixer and cost hamiltonian subroutine names respectively
        """
        if len(graph.nodes) > self.builder.qubits:
            raise ValueError(
                f"The graph provided has more nodes"
                f"({len(graph.nodes)}) than the qubits initialized ({self.builder.qubits})"
            )
        std = self.builder.import_library(lib_class=std_gates)

        cost_name = f"qaoa_maxcut_cost_{self._maxcut_cost_count}_{self.builder.qubits}"
        self._maxcut_cost_count += 1

        qubit_array_param = f"qubit[{self.builder.qubits}] qubits"

        gamma = "float gamma"

        # cost hamiltonian $$\sum_{E(graph)} Z_i \otimes Z_j$$
        std.begin_subroutine(
            cost_name, [qubit_array_param , gamma]
        )
        old_call_space = std.call_space
        std.call_space = "qubits[{}]"
        for i,j in graph.edges:
            std.cnot(i,j)
            std.rz("-2 * gamma", j)
            std.cnot(i,j)
        std.call_space = old_call_space
        std.end_subroutine()

        # mixer hamiltonian $$\sum_{i} X_i$$
        mixer_name = self.x_mixer(graph)

        return mixer_name, cost_name

    def setup_maxcut(self, graph : nx.Graph):
        r"""
        Perform the setup for a Max Cut problem with the given graph.

        Args:
            graph : nx.Graph
                Graph that describes the problem
        """
        self.mixer_hamiltonian, self.cost_hamiltonian = self.qaoa_maxcut(graph=graph)
        self.layer_circuit = self.layer(self.cost_hamiltonian, self.mixer_hamiltonian)

    def layer(self, cost_ham : str, mixer_ham : str) -> str :
        r"""
        Create layer circuit.
        Args:
            cost_ham : str
                Name of cost Hamiltonian subroutine
            mixer_ham : str
                Name of mixer Hamiltonian subroutine
        Returns:
            Name of layer subroutine
        """
        std = self.builder.import_library(lib_class=std_gates)

        name = f"qaoa_layer_function_{self.builder.qubits}"

        qubit_array_param = f"qubit[{self.builder.qubits}] qubits"
        gamma = "float gamma"
        alpha = "float alpha"

        std.begin_subroutine(
            name, [qubit_array_param , gamma, alpha]
        )

        std.call_subroutine(cost_ham, ["qubits", "gamma"])
        std.call_subroutine(mixer_ham, ["qubits", "alpha"])

        std.end_subroutine()

        return name

    def generate_algorithm(self, depth : int, layer : str = "", param : list[float] | None = None) -> str:
        r"""
        Load the Quantum Approximate Optimization Algorithm (QAOA) ansatz as a pyqasm module.

        Args:
            depth : int
                Depth of the circuit (i.e. number of layer repetitions)
            layer : str
                Name of the layer circuit subroutine
            param : list[float]
                Parameters for circuit definitions, the number of parameters to provide is 2*depth.
                The expected format is [gamma_0 alpha_0 gamma_1 alpha_1 ... gamma_(depth-1) alpha_(depth-1)], 
                where gamma and alpha are the coefficients for the cost and mixer Hamiltonians respetively

        Returns:
            (str) qasm code containing the QAOA ansatz circuit
        """
        if param is None and self.use_input is False:
            raise ValueError(
                "Param cannot be None if use_input is False"
            )
        std = self.builder.import_library(lib_class=std_gates)

        layer = self.layer_circuit if layer == "" else layer

        num_qubits = self.builder.qubits

        for i in range(depth):
            if self.use_input:
                std.add_input_var(f"gamma_{i}", qtype="float")
                std.add_input_var(f"alpha_{i}", qtype="float")
            else:
                std.classical_op(f"float gamma_{i} = {param[i*2]}")
                std.classical_op(f"float alpha_{i} = {param[i*2+1]}")

        for q in range(self.builder.qubits):
            std.reset(q)

        for q in range(self.builder.qubits):
            std.h(q)

        for i in range(depth):
            std.call_subroutine(layer, parameters=[f"qb[0:{num_qubits}]", f"gamma_{i}", f"alpha_{i}"])

        std.measure(list(range(num_qubits)), list(range(num_qubits)))

        return self.builder.build()
