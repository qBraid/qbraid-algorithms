// Bell's Inequality Circuit based on Amazon Braket Experimental Library
OPENQASM 3.0;
include "stdgates.inc";

/*
Create bell inequality circuits
*/
// Create 3 2-qubit registries (we need 3 total circuits)
qubit[2] q0; 
qubit[2] q1;
qubit[2] q2;


// Create 3 2-bit classical registries for measurment 
bit[2] c0;
bit[2] c1;
bit[2] c2;

// Initialize all qubits to 0
reset q0;
reset q1;
reset q2;

/*
Prepare bell singlet states between each of the qubit pairs
*/
x q0[0];
x q0[1];
h q0[0];
cx q0[0], q0[1];

x q1[0];
x q1[1];
h q1[0];
cx q1[0], q1[1];

x q2[0];
x q2[1];
h q2[0];
cx q2[0], q2[1];

/*
Apply the rotations (angle A = 0 = no rotation)
*/

// Circuit AB
rx(pi / 3) q0[1];

// Circuit AC
rx(2 * pi / 3) q1[1];

// Circuit BC
rx(pi / 3) q2[0];
rx(2 * pi / 3) q2[1];

// Perform measurements for each of the three circuits
measure q0[0] -> c0[0];
measure q0[1] -> c0[1];

measure q1[0] -> c1[0];
measure q1[1] -> c1[1];

measure q2[0] -> c2[0];
measure q2[1] -> c2[1];






