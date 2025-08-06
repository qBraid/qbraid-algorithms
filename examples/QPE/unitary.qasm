OPENQASM 3.0;
include "stdgates.inc";

gate test_gate a {
  h a;
  x a;
}
