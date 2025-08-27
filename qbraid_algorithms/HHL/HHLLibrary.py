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


from ..qpe import PhaseEstimationLibrary

# from GateLibrary import GateLibrary, std_gates
from ..QTran import *


def HHLLibrary(PhaseEstimation):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def HHL(self,a,b,clock):
        sys = self.builder
        A = sys.import_library(a)
        P = sys.import_library(PhaseEstimationLibrary)
        gate_name = P.phase_estimation(b,clock,a)
        # todo: make the lambda scaling/ U invert
        P.inverse_op(gate_name)