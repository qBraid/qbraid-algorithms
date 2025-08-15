OPENQASM 3.0;
include "iqft.qasm";

qubit[2] q;
bit[2] b;
h q[0];
h q[1];
iqft(q);
b = measure q;