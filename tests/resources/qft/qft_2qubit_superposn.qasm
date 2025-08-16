OPENQASM 3.0;
include "qft.qasm";

qubit[2] q;
bit[2] b;
h q[0];
h q[1];
qft(q);
b = measure q;