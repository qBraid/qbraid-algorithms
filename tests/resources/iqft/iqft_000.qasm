OPENQASM 3.0;
include "iqft.qasm";

qubit[3] q;
bit[3] b;
iqft(q);
b = measure q;