OPENQASM 3.0;
include "inputs.inc";
include "iqft_subroutine.qasm";

qubit[qft_size] q;
bit[qft_size] b;

iqft(q, qft_size);
b = measure q;