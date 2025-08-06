OPENQASM 3.0;
include "stdgates.inc";


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
    // pyqasm does not currently support nested includes, so iqft defined explicitly
    // IQFT
    for int[16] i in [0:(n >> 1) - 1] {
        swap q[i], q[n - i - 1];
    }
    for int[16] i in [0:n-1] {
        int[16] target = n - i - 1;
        for int[16] j in [0:(n - target - 2)] {
            int[16] control = n - j - 1;
            int[16] k = control - target;
            cp(-2 * pi / (1 << (k + 1))) q[control], q[target];
        }
        h q[target];
    }
}