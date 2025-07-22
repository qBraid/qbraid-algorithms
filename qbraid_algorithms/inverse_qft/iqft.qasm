OPENQASM 3.0;
include "stdgates.inc";
include "iqft.inc"; 

qubit[n] q;
bit[n] b;

for int[16] i in [0:n >> 1] {
    swap q[i], q[n - i - 1];
}

for int[16] i in [0:n] {
    int[16] target = n - 1 - i;
    
    for int[16] j in [0:(n - target - 1)] {
        int[16] ctrl = n - j - 1;
        int[16] k = ctrl - target - 1;
        cp(-2 * pi / (1 << (k + 2))) q[ctrl], q[target];
    }

    h q[target];
}

b = measure q;
