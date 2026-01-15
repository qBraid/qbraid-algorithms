from qbraid_algorithms.qtran import GateLibrary, std_gates


def bit_driver(builder, qubits, b):
    std = builder.import_library(lib_class=std_gates)
    
    name = f"qaoa_cost_{len(qubits)}"  # BUG FIX: Include depth in name

    qubit_list = "{" + ",".join([str(q) for q in qubits]) + "}"

    qubit_array_param = f"qubit[{len(qubits)}] qubits"

    std.begin_subroutine(
        name, [qubit_array_param]
    )

    for i in qubits:
        std.z(i)

    std.end_subroutine()
        
