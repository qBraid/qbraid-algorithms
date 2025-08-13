OPENQASM 3.0;
include "qft.qasm";

qubit[1] q;
bit[1] b;
x q[0];
qft(q);
b = measure q;