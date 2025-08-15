OPENQASM 3.0;
include "bernvaz_subroutine.qasm";

qubit[BERNVAZ_SIZE] q;
qubit[1] ancilla;
bit[BERNVAZ_SIZE] b;

bernvaz(q, ancilla);
b = measure q;
