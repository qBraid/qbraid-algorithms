OPENQASM 3.0;
include "stdgates.inc";
include "qft.inc";

qubit[n] q;
bit[n] b;
for int[16] i in [0:n] {
  h q[i];
  for int[16] j in [i + 1:n] {
    int[16] k = j - i;
    cp(2 * pi / (1 << k + 1)) q[j], q[i];
  }
}
for int[16] i in [0:n >> 1] {
  swap q[i], q[n - i - 1];
}
b = measure q;