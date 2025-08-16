OPENQASM 3.0;
include "iqft.qasm";

qubit[2] q;
bit[2] b;
iqft(q);
b = measure q;