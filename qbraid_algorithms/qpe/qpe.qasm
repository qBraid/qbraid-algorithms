OPENQASM 3.0;
include "stdgates.inc";
include "qpe_subroutine.qasm";

qubit[QPE_SIZE] q;
qubit[1] psi;
bit[QPE_SIZE] b;

qpe(q, psi);
b = measure q;

