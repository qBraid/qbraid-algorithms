from qbraid_algorithms.qtran import QasmBuilder, std_gates, GateLibrary, GateBuilder
import networkx as nx
import pyqasm
from pyqasm.modules.base import QasmModule

class QAOA:

    builder : QasmBuilder
    mixer_hamiltonian : str
    cost_hamiltonian : str
    layer_circuit : str
    use_subroutines : bool
    use_input : bool

    def __init__(self, num_qubits : int, qasm_version : int = 3, use_input : bool = True):
        self.builder = QasmBuilder(num_qubits, version=qasm_version)
        self.use_input = use_input

    
    def xy_mixer(self, graph : nx.Graph) -> str:
        """
        Generate XY mixer Hamiltonian subroutine.
        
        xy_mixer_hamiltonian = $$\frac{1}{2}\sum_{(i,j)\in E(G)} X_iX_j + Y_iY_j$$
        Args:
            graph : nx.Graph
                Graph that describes the problem
        Returns:
            mixer Hamiltonian subroutine name
        """
        std = self.builder.import_library(lib_class=std_gates)
            
        mixer_name = f"qaoa_xy_mixer_{self.builder.qubits}"

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
        """
        Generate X mixer Hamiltonian subroutine.
        
        x_mixer_hamiltonian = $$\sum_{i} X_i$$
        Args:
            graph : nx.Graph
                Graph that describes the problem
        Returns:
            mixer Hamiltonian subroutine name
        """
        std = self.builder.import_library(lib_class=std_gates)
            
        mixer_name = f"qaoa_x_mixer_{self.builder.qubits}"

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
        """
        Generate min vertex cover cost Hamiltonian subroutine.
        
        cost_hamiltonian $$3\sum_{(i,j)\in E(G)} (Z_i \otimes Z_j + Z_i + Z_j)-\sum_{i \in V(G)} Z_i$$
        Args:
            graph : nx.Graph
                Graph that describes the problem
        Returns:
            Cost Hamiltonian subroutine name
        """
        std = self.builder.import_library(lib_class=std_gates)
            
        cost_name = f"qaoa_min_vertex_cover_cost_{self.builder.qubits}"

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
        """
        Generate max clique cost Hamiltonian subroutine.
        
        cost_hamiltonian $$3\sum_{(i,j)\in E(\bar{G})} (Z_i \otimes Z_j - Z_i - Z_j)+\sum_{i \in V(G)} Z_i$$
        Args:
            graph : nx.Graph
                Graph that describes the problem
        Returns:
            Cost Hamiltonian subroutine name
        """
        std = self.builder.import_library(lib_class=std_gates)
            
        cost_name = f"qaoa_min_vertex_cover_cost_{self.builder.qubits}"

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
        """
        Generate cost hamiltonian and mixer hamiltonian subroutines.

        cost_hamiltonian = $$\sum_{E(graph)} Z_i \otimes Z_j$$
        
        mixer_hamiltonian = $$\sum_{i} X_i$$
        Args:
            graph : nx.Graph
                Graph that describes the problem
        Returns:
            (mixer, cost) : tuple[str, str] mixer and cost hamiltonian subroutine names respectively
        """
        std = self.builder.import_library(lib_class=std_gates)
            
        cost_name = f"qaoa_maxcut_cost_{self.builder.qubits}"

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
        """
        Perform the setup for a Max Cut problem with the given graph.

        Args:
            graph : nx.Graph
                Graph that describes the problem
        """
        self.mixer_hamiltonian, self.cost_hamiltonian = self.qaoa_maxcut(graph=graph)
        self.layer_circuit = self.layer(self.cost_hamiltonian, self.mixer_hamiltonian)

    def layer(self, cost_ham : str, mixer_ham : str) -> str :
        """
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

    def generate_algorithm(self, depth : int, layer : str = "", param : list[float] = []) -> str:
        """
        Load the Quantum Approximate Optimization Algorithm (QAOA) ansatz as a pyqasm module.

        Args:
            cost_ham : str
                Name of the cost Hamiltonian subroutine
            depth : int
                Depth of the circuit (i.e. number of layer repetitions)
            layer : str
                Name of the layer circuit subroutine
            epsilon : float
                Error for expectation value calculation

        Returns:
            (PyQasm Module) pyqasm module containing the QAOA ansatz circuit
        """
        std = self.builder.import_library(lib_class=std_gates)

        layer = self.layer_circuit if layer == "" else layer

        num_qubits = self.builder.qubits
        #self.builder.claim_qubits(self.builder.qubits)
        #self.builder.claim_qubits(1)
        
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

        #std.call_subroutine(cost_ham, [f"qb[0:{num_qubits}]", "1"])
        #std.h(self.builder.qubits - 1)
        std.measure(list(range(num_qubits)), list(range(num_qubits)))
        """for q in range(num_qubits):
            std.cswap(control=f"qb[{self.builder.qubits - 1}]", targ1=f"qb[{q}]", targ2=f"qb[{q+num_qubits}]")
        std.h(self.builder.qubits - 1)
        std.measure([self.builder.qubits - 1], [0])

        std.begin_if("cb[0] == 0")
        std.classical_op("measure_0 = measure_0 + 1")
        std.end_if()"""

        """std.classical_op(f"expval = measure_0/{repetitions}")
        std.classical_op("expval = 2*(expval - 0.5)")
        std.classical_op("expval = sqrt(expval)")
        std.classical_op("expval = log(expval)")"""

        return self.builder.build()
