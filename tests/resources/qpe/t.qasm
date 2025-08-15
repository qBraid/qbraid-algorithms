OPENQASM 3.0;
include "stdgates.inc";

gate custom_t q {
    p(pi/4) q;
}