// Bernstein Vazirani algorithm - example for string "1001"
OPENQASM 3.0;
include "stdgates.inc";

// Input string qubits
qubit[4] x; 

// Ancilla qubit
qubit[1] a;

// Classical bits for measurement
bit[4] b;

// Initialize qubits to 0
reset x;
reset a;

// Apply Hadamard gate to all input qubits
h x[0];
h x[1];
h x[2];
h x[3];

// Apply X then H to ancilla qubit
x a[0];
h a[0];

// Build the oracle for the string "1001"
cx x[0], a[0];
cx x[3], a[0];

// Apply Hadamard gate to all  qubits again
h x[0];
h x[1];
h x[2];
h x[3];
h a[0];

// Perform measurements on input qubits to retrieve the secret string
measure x[0] -> b[0];
measure x[1] -> b[1];
measure x[2] -> b[2];
measure x[3] -> b[3];

