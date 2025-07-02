/*
A reference implementation of the Quantum Fourier Transform (QFT) circuit 
for 5 qubits in QASM3 format.
*/

OPENQASM 3.0;
include "stdgates.inc";

/*
- First define a register of 5 qubits
- Next iterate through each of the 5 qubits
   - apply H gate 
   - then we need to apply n - i - 1 controlled phase gates
      - we must compute the phase angle for each controlled gate by:
            - 2 * pi / 2^(n - i - 1) - double check this
   - after iterating through all qubits, we then do n // 2 swaps to 
     reverse the order of the qubits
   - do we measure at the end?
*/

// Define a 5-qubit quantum register
qubit[5] q;
// Initialize all qubits to 0
reset q0;

// Iterate through qubits and apply H & cp gates
for int i in [0:4]
    h q[i];
    for int j in [5 - i - 1]
    // Compute angle for cp gate - this allows bit to be encoded in phase 
        int[32] angle = 2 * pi / 2^(5 - i - 1);
        cp(angle, q[i], q[j + i + 1]);

// Reverse order of the qubits by applying swaps - only need 5 // 2 = 2 here
swap q[0], q[4];
swap q[1], q[3];

// Measure the qubits
bit[5] c;
c = measure q;

