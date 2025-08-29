# Copyright 2025 qBraid
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



# from GateLibrary import GateLibrary, std_gates
# from qbraid_algorithms.QTran import 

def HHLLibrary(PhaseEstimationLibrary):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def HHL(self,a,b,clock):
        sys = self.builder
        # A = sys.import_library(a)
        # operation currently works within main method due to need of inverse op and use of ancillas
        #TODO: edit this into a full subroutine once complex hamiltonians for phase est are implemented
        # this is due to evolution being just a negative time value while static hamiltonians need a full inverse_op call
        P = sys.import_library(PhaseEstimationLibrary)
        gate_name = P.phase_estimation(b,clock,a)
        # todo: make the lambda scaling/ U invert
        P.inverse_op(gate_name)