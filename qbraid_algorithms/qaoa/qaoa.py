from qbraid_algorithms.qtran import QasmBuilder, std_gates, GateLibrary, GateBuilder
from matplotlib import pyplot as plt
import networkx as nx

def qaoa_maxcut(builder : QasmBuilder, graph : nx.Graph) -> tuple[str, str] : 
    std = builder.import_library(lib_class=std_gates)
        
    cost_name = f"qaoa_maxcut_cost_{builder.qubits}"

    qubit_array_param = f"qubit[{builder.qubits}] qubits"

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
    mixer_name = f"qaoa_maxcut_mixer_{builder.qubits}"

    alpha = "float alpha"

    std.begin_subroutine(
        mixer_name, [qubit_array_param, alpha]
    )

    for i in range(builder.qubits):
        std.rx("-2 * alpha", i)
    
    std.end_subroutine()

    return mixer_name, cost_name

def layer(builder : QasmBuilder, cost_ham : str, mixer_ham : str) -> str :
    std = builder.import_library(lib_class=std_gates)

    name = f"qaoa_layer_function_{builder.qubits}"

    qubit_array_param = f"qubit[{builder.qubits}] qubits"
    gamma = "float gamma"
    alpha = "float alpha"

    std.begin_subroutine(
        name, [qubit_array_param , gamma, alpha]
    )

    std.call_subroutine(cost_ham, ["qubits", "gamma"])
    std.call_subroutine(mixer_ham, ["qubits", "alpha"])

    std.end_subroutine()

    return name

def cost_function(builder : QasmBuilder, layer : str, depth : int, params : list[tuple[float, float]]) -> str :
    std = builder.import_library(lib_class=std_gates)

    name = f"qaoa_cost_function_{layer}"

    qubit_array_param = f"qubit[{builder.qubits}] qubits"

    std.begin_subroutine(
        name, [qubit_array_param, "float value"], "float"
    )

    for i in range(builder.qubits):
        std.h(i)

    for i in range(depth):
        std.call_subroutine(layer, parameters=["qubits", params[i][0], params[i][1]])
    
    std.end_subroutine()

    return name


def calculate_gradient_function(builder : QasmBuilder, hamiltonian : str, delta : float = 0.1) -> str :
    std = builder.import_library(lib_class=std_gates)

    name = f"qaoa_compute_gradient_{hamiltonian}"

    qubit_array_param = f"qubit[{builder.qubits}] qubits"

    std.begin_subroutine(
        name, [qubit_array_param, "float value"], "float"
    )
    std.add_var(name="frac", qtype="float")
    std.add_var(name="val1", qtype="int")
    std.add_var(name="val2", qtype="int")
    std.call_subroutine(hamiltonian, [qubit_array_param, f"value + {delta}"])
    std.measure(range(builder.qubits), range(builder.qubits))
    std.classical_op(f"val1 = cb[0:{builder.qubits}]")
    std.call_subroutine(hamiltonian, [qubit_array_param, f"value - {delta}"])
    std.measure(range(builder.qubits), [i + builder.qubits for i in range(builder.qubits)])
    std.classical_op(f"val2 = cb[{builder.qubits}:{builder.qubits*2}]")
    std.classical_op(operation=f"frac = (val1 - val2)/(2* {delta})")

    std.classical_op(operation="return frac")

    std.end_subroutine()

    return name