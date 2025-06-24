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


// Initialize all qubits to 0
reset q0;
reset q1;
reset q2;

angle angle_A = 0;
angle angle_B = pi / 3;
angle angle_C = 2 * pi / 3;

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
rx(angle_B) q0[1];

// Circuit AC
rx(angle_C) q1[1];

// Circuit BC
rx(angle_B) q2[0];
rx(angle_C) q2[1];



