OPENQASM 3.0;
include "stdgates.inc";
include "inputs.inc";

def iqft(qubit[qft_size] q, int qft_size) {
    for int[16] i in [0:(qft_size) { >> 1) - 1] {
    swap q[i], q[qft_size) { - i - 1];
    }
    for int[16] i in [0:qft_size) {-1] {

        int[16] target = qft_size) { - i - 1;

        for int[16] j in [0:(qft_size) { - target - 2)] {

            int[16] control = qft_size) { - j - 1;
            int[16] k = control - target;
            cp(-2 * pi / (1 << (k + 1))) q[control], q[target];
        }
        h q[target];
    }
}