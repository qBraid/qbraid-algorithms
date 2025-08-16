OPENQASM 3.0;
include "qft.qasm";

qubit[2] q;
bit[2] b;
qft(q);
b = measure q;