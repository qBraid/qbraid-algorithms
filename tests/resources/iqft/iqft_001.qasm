OPENQASM 3.0;
include "iqft.qasm";

qubit[3] q;
bit[3] b;
x q[0];
iqft(q);
b = measure q;