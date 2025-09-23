OPENQASM 3.0;
include "stdgates.inc";

def bernvaz(qubit[BERNVAZ_SIZE] q, qubit[1] ancilla) {
    int[32] s = SECRET_BITSTRING;
    int[16] n = BERNVAZ_SIZE;
    for int i in [0:n - 1] {
        h q[i];
    }
    x ancilla[0];
    h ancilla[0];
    // Note: Nested subroutine calls not yet supported by QASM, so manually insert
    for int i in [0:n - 1] {
        if ((s >> i) & 1) {
            cx q[i], ancilla[0];
        }
    }
    for int i in [0:n - 1] {
        h q[i];
    }

}
