OPENQASM 3.0;
include "qpe_subroutine.qasm";

qubit[QPE_SIZE] q;
qubit[1] psi;
bit[QPE_SIZE] b;

PREP_EIGENSTATE
qpe(q, psi);
b = measure q;
