OPENQASM 3.0;
include "qft_subroutine.qasm";

qubit[QFT_SIZE] q;
bit[QFT_SIZE] b;

qft(q);
b = measure q;