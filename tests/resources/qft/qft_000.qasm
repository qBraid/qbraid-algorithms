OPENQASM 3.0;
include "qft.qasm";

qubit[3] q;
bit[3] b;
qft(q);
b = measure q;