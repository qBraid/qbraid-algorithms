OPENQASM 3.0;
include "qft.qasm";
include "iqft.qasm";

qubit[2] q;
bit[2] b;
qft(q);
iqft(q);
b = measure q;