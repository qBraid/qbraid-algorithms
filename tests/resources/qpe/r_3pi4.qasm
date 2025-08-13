OPENQASM 3.0;
include "stdgates.inc";

gate custom_3pi4 q {
    p(3 * pi/4) q;
}