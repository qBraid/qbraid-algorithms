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

class GateLibrary:
    def __init__(self, gate_import, gate_ref, gate_defs, program_append,builder,annotated=False):
        self.gate_import = gate_import
        self.gate_ref = gate_ref
        self.gate_defs = gate_defs
        self.program = program_append
        self.builder = builder
        self.annotated = annotated
        self.gate_mod = ""
        self.name = "GATE_LIB"

    def call_gate(self,gate,target,controls=None,phases=None,prefix =""):
        if gate not in self.gate_ref:
            print(f"stdgates: gate {gate} is not part of visible scope, make sure that this isn't a floating reference / malformed statement, or is at least previously defined within untracked environment definitions")
        call = prefix+str(gate) + ' '
        if phases is not None:
            call += '('
            if isinstance(phases,list):
                call += phase[0]
                for phase in phases[1:]:
                    call += f",{phase}"
            else:
                call += str(phases)
            call += ')'
        
        if controls is not None:
            if isinstance(controls,list):
                for control in controls:
                    call += f" qb[{control}],"
            else:
                call += f" qb[{controls}],"
            
        call += f" qb[{target}];"
        self.program(self.gate_mod + call)

        
    def measure(self,qubits:list,clbits:list):
        cindex = "cb[{" + str(clbits)[1:-1] + "}]"
        qindex = "qb[{" + str(qubits)[1:-1] + "}]"
        call = f"{cindex} = measure {qindex};"
        self.program(call)

    def comment(self,line:str):
        call = ""
        if "\n" in line:
            call += "/*\n" + line +"\n*/"
        else:
            call += "//" + line
        self.program(call)
    
    def begin_if(self,conditional: str):
        call = f"if ({conditional})" +"{"
        self.builder.scope += 1
        self.program(call)

    def begin_loop(self, iter, id: str="i"):
        if isinstance(iter,int):
            base = "int"
            dom = f"[0:{int(iter)}]"
        elif isinstance(iter,tuple):
            if len(iter) ==2:
                if isinstance(iter[0],str):
                    base = iter[0]
                    dom = iter[1]
                else:
                    base = "int"
                    dom = f"[{int(iter[0])}:{int(iter[1])}]"
            else:
                if isinstance(iter[1],int):
                    base = "int"
                    dom = f"[{int(iter[0])}:{int(iter[2])}:{int(iter[1])}]"
                else:
                    base = "float"
                    r = int(iter[2])
                    dom = "{" + str([iter[0]+float(i)/(r-1) for i in range(r)])[1:-1] + "}"
        elif isinstance(iter, str):
            call  = "for " + iter + "{"
            self.program(call)
            self.builder.scope += 1
            return 
        else:
            print(f"loop has improper parameterization with: {iter}")
            return
        call = f"for {base} {id} in {dom} " + "{"
        self.program(call)
        self.builder.scope += 1

    def begin_gate(self, name, qargs, params=None):
        if name in self.gate_ref:
            print(f"warning: gate {name} replacing existing namespace")
        call = f"gate {name}{"("+str(params)[1:-1]+")" if params is not None else ""} {str(qargs)[1:-1]}" +"{"
        self.program(call)
        self.builder.scope += 1
    
    def begin_subroutine(self,name, parameters:list[str], return_type=None):
        if name in self.gate_ref:
            print(f"warning:  gate {name} replacing existing namespace")
        call = f"def {name}({str(parameters)[1:-1]}) -> {return_type if return_type is not None else ""}" + "{"
        self.program(call)
        self.builder.scope += 1


    def close_scope(self):
        self.builder.scope -= 1
        self.program("}")

    def end_if(self):
        self.close_scope()
    def end_loop(self):
        self.close_scope()
    def end_gate(self):
        self.close_scope()
    def end_subroutine(self):
        self.close_scope()
    def controlled_op(self,gate_call,params,n=1):
        if isinstance(gate_call,str):
            self.call_gate(gate_call,*params,prefix=f"ctrl{'' if n==0 else f'({n})'} @")
        else:
            self.gate_mod = f"ctrl{'' if n<2 else f'({n})'} @ "
            gate_call(*params)
            self.gate_mod = ""
    def add_gate(self,name: str,gate_def: str):
        self.gate_defs[name] = gate_def
        self.gate_ref.append(name)


class std_gates(GateLibrary):
    gates = ["phase","x","y","z","h","s","sdg","sx",'cx','cy','cz','cphase','crx','cry','crz','swap','ccx','cswap']
    name = 'std_gates.inc'
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.name not in self.gate_import:
            self.gate_import.append(self.name)
        for gate in std_gates.gates:
            if gate not in self.gate_ref:
                self.gate_ref.append(gate)


    def phase(self,theta,targ: int):
        self.call_gate("phase",targ,phases=theta)
    def x(self,targ: int):
        self.call_gate('x',targ)
    def y(self,targ: int):
        self.call_gate('y',targ)
    def z(self,targ: int):
        self.call_gate('z',targ)
    def h(self,targ: int):
        self.call_gate('h',targ)
    def s(self,targ: int):
        self.call_gate('s',targ)
    def sdg(self,targ: int):
        self.call_gate('sdg',targ)
    def sx(self,targ: int):
        self.call_gate('sx',targ)