OPENQASM 3.0;
include "iqft_subroutine.qasm";

qubit[IQFT_SIZE] q;
bit[IQFT_SIZE] b;

iqft(q);
b = measure q;