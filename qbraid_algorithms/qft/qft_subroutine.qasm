OPENQASM 3.0;
include "stdgates.inc";
include "inputs.inc";


def qft(qubit[qft_size] q, int qft_size) {
  for int[16] i in [0:qft_size - 1] {
    h q[i];
    for int[16] j in [i + 1:qft_size - 1] {
      int[16] k = j - i;
      cp(2 * pi / (1 << (k + 1))) q[j], q[i];
    }
  }

  for int[16] i in [0:(qft_size >> 1) - 1] {
    swap q[i], q[qft_size - i - 1];
  }
}