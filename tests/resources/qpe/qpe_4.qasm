OPENQASM 3.0;
include "qpe.qasm";

qubit[4] m;
bit[4] b;
qubit[1] psi;

// Tests on T gate (eigenvector |1>)
x psi; // Initialize the state |1>
qpe(m, psi); 
b = measure m;