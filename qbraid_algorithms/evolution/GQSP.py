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


from ..QTran import *
import numpy as np
import itertools
from scipy.optimize import minimize
import string

class GQSP(GateLibrary):
    '''
    use this paper for future work, to be more in line with the actual gqsp implementation:
    arXiv:2105.02859 <https://arxiv.org/abs/2105.02859>
    this current work is essentially an incomplete derivative, but it works for any low degree polynomial   
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)