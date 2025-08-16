OPENQASM 3.0;
include "iqft.qasm";

qubit[1] q;
bit[1] b;
iqft(q);
b = measure q;