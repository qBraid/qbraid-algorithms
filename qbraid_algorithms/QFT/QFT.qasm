// QASM3 native application of QFT
OPENQASM 3.0;
include "stdgates.inc";

def QFT(readonly array[qubit,#dim= 1] reg){
    for int i in [0:sizeof(reg)-1]{
        h reg[i]
        for int j in [i+1:sizeof(reg)]{
            cp(pi>>(j-i)) i , j
        }
    }
    h reg[-1]
}