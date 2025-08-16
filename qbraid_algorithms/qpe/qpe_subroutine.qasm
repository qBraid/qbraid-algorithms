OPENQASM 3.0;
include "stdgates.inc";
include "iqft.qasm";

CUSTOM_GATE_DEFS 

def qpe(qubit[QPE_SIZE] q, qubit[1] psi) {
    int n = QPE_SIZE;
    for int i in [0:n-1] {
        h q[i];
    }
    for int j in [0:n-1] {
        int[16] k = 1 << j;
        for int m in [0:k-1] {
            CU q[j], psi[0];
        }
    }
    iqft(q);

}