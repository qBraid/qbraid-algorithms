OPENQASM 3.0;
include "stdgates.inc";
include "inputs.inc";


def qft(qubit[qft_size] q, int n) {
  for int[16] i in [0:n - 1] {
    h q[i];
    for int[16] j in [i + 1:n - 1] {
      int[16] k = j - i;
      cp(2 * pi / (1 << (k + 1))) q[j], q[i];
    }
  }

  for int[16] i in [0:(n >> 1) - 1] {
    swap q[i], q[n - i - 1];
  }
}