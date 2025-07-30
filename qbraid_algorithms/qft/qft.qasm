OPENQASM 3.0;
include "inputs.inc";
include "qft_subroutine.qasm";

qubit[qft_size] q;
bit[qft_size] b;

qft(q, qft_size);
b = measure q;