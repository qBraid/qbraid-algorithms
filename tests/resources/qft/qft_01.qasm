OPENQASM 3.0;
include "qft.qasm";

qubit[2] q;
bit[2] b;
x q[0]; // Initialize the first qubit to |1>
qft(q);
b = measure q;