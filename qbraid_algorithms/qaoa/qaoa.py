from qbraid_algorithms.qtran import QasmBuilder, std_gates, GateLibrary, GateBuilder
import networkx as nx
import pyqasm
from pyqasm.modules.base import QasmModule

class QAOA:

    builder : QasmBuilder
    mixer_hamiltonian : str
    cost_hamiltonian : str
    layer_circuit : str

    def __init__(self, num_qubits : int):
        builder = QasmBuilder(num_qubits)

    def qaoa_maxcut(self, graph : nx.Graph) -> tuple[str, str] : 
        std = self.builder.import_library(lib_class=std_gates)
            
        cost_name = f"qaoa_maxcut_cost_{self.builder.qubits}"

        qubit_array_param = f"qubit[{self.builder.qubits}] qubits"

        gamma = "float gamma"

        # cost hamiltonian \sum_{E(graph)} Z_i @ Z_j
        std.begin_subroutine(
            cost_name, [qubit_array_param , gamma]
        )

        for i,j in graph.edges:
            std.cnot(i,j)
            std.rz("2 * gamma", j)
            std.cnot(i,j)

        std.end_subroutine()


        # mixer hamiltonian \sum_{i} X_i
        mixer_name = f"qaoa_maxcut_mixer_{self.builder.qubits}"

        alpha = "float alpha"

        std.begin_subroutine(
            mixer_name, [qubit_array_param, alpha]
        )

        for i in range(self.builder.qubits):
            std.rx("-2 * alpha", i)
        
        std.end_subroutine()

        return mixer_name, cost_name
    
    def setup_maxcut(self, graph : nx.Graph):
        self.mixer_hamiltonian, self.cost_hamiltonian = self.qaoa_maxcut(graph=graph)
        self.layer_circuit = self.layer(self.cost_hamiltonian, self.mixer_hamiltonian)

    def layer(self, cost_ham : str, mixer_ham : str) -> str :
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

    def cost_function(self, layer : str, depth : int, params : list[tuple[float, float]]) -> str :
        std = self.builder.import_library(lib_class=std_gates)

        name = f"qaoa_cost_function_{layer}"

        qubit_array_param = f"qubit[{self.builder.qubits}] qubits"

        for i in range(self.builder.qubits):
            std.h(i)

        for i in range(depth):
            std.call_subroutine(layer, parameters=["qubits", params[i][0], params[i][1]])

        return name

    def generate_algorithm(self, cost_ham : str, depth : int, layer : str = "", epsilon : float = 0.01) -> QasmModule:
        std = self.builder.import_library(lib_class=std_gates)

        layer = self.layer_circuit if layer == "" else layer
        
        num_qubits = self.builder.qubits
        self.builder.claim_qubits(self.builder.qubits)
        self.builder.claim_qubits(1)

        repetitions = int(round((1.0/epsilon)**2))
        
        for i in range(depth):
            std.add_input_var(f"gamma_{i}", qtype="float")
            std.add_input_var(f"alpha_{i}", qtype="float")
        
        std.add_var(name="measure_0", qtype="int")
        std.add_output_var("expval", qtype="float")
        std.begin_loop(repetitions)
        
        for q in range(self.builder.qubits):
            std.reset(q)
        
        for q in range(self.builder.qubits):
            std.h(q)

        for i in range(depth):
            std.call_subroutine(layer, parameters=[f"qb[0:{num_qubits}]", f"gamma_{i}", f"alpha_{i}"])
            std.call_subroutine(layer, parameters=[f"qb[{num_qubits}:{num_qubits*2}]", f"gamma_{i}", f"alpha_{i}"])

        std.call_subroutine(cost_ham, [f"qb[0:{num_qubits}]", "1"])
        std.h(self.builder.qubits - 1)
        for q in range(num_qubits):
            std.cswap(control=f"qb[{self.builder.qubits - 1}]", targ1=f"qb[{q}]", targ2=f"qb[{q+num_qubits}]")
        
        std.measure(f"qb[{self.builder.qubits - 1}", "cb[0]")

        std.begin_if("cb[0] == 0")
        std.classical_op("measure_0 = measure_0 + 1")
        std.end_if()
        
        std.end_loop()

        std.classical_op(f"expval = measure_0/{repetitions}")
        std.classical_op("expval = 2*(expval - 0.5)")
        std.classical_op("expval = sqrt(expval)")
        std.classical_op("expval = log(expval)")

        return pyqasm.load(self.builder.build())
