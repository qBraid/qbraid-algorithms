# -*- coding: utf-8 -*-
"""bloqade-python-scipy.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1T2sCY8tx4EeYOCBUpZ3ZlDSKYnPI3V2F
"""

# !pip install -qqq scipy bloqade --progress-bar off

from scipy.optimize import newton_krylov
import numpy as np
import pytest
from bloqade import (
    waveform,
    rydberg_h,
    piecewise_linear,
    piecewise_constant,
    constant,
    linear,
    var,
    cast,
    start,
    get_capabilities,
)
from bloqade.atom_arrangement import Chain
from bloqade.ir import (
    AnalogCircuit,
    Sequence,
    rydberg,
    Pulse,
    rabi,
    detuning,
    Field,
    Uniform,
)
from bloqade.ir.routine.base import Routine
# from bloqade.ir.routine import BloqadeEmulation
from bloqade.ir.routine.params import Params, ScalarArg

import numpy as np
from decimal import Decimal

def test_rydberg_h():
    run_time = var("run_time")

    @waveform(run_time + 0.2)
    def delta(t, amp, omega):
        return np.sin(omega * t) * amp

    delta = delta.sample(0.05, "linear")
    ampl = piecewise_linear([0.1, run_time, 0.1], [0, 10, 10, 0])
    phase = piecewise_constant([2, 2], [0, np.pi])
    register = Chain(11, lattice_spacing=6.1)

    static_params = {"amp": 1.0}
    batch_params = [{"omega": omega} for omega in [1, 2, 4, 8]]
    args = ["run_time"]

    routine = rydberg_h(
        atoms_positions=register,
        detuning=delta,
        amplitude=ampl,
        phase=phase,
        batch_params=batch_params,
        static_params=static_params,
        args=args,
    )

    detuning_field = Field({Uniform: delta})
    ampl_field = Field({Uniform: ampl})
    phase_field = Field({Uniform: phase})

    pulse = Pulse(
        {detuning: detuning_field, rabi.amplitude: ampl_field, rabi.phase: phase_field}
    )
    sequence = Sequence({rydberg: pulse})

    source = (
        register.rydberg.detuning.uniform.apply(delta)
        .amplitude.uniform.apply(ampl)
        .phase.uniform.apply(phase)
        .assign(**static_params)
        .batch_assign(batch_params)
        .args(args)
    )

    circuit = AnalogCircuit(register, sequence)
    args_list = tuple([ScalarArg(arg) for arg in args])
    params = Params(register.n_sites, static_params, batch_params, args_list)
    expected_routine = Routine(source, circuit, params)

    # ignore because no equality implemented
    # assert routine.source == expected_routine.source
    assert routine.circuit == expected_routine.circuit
    assert routine.params == expected_routine.params

def test_rydberg_h_3():
    from bloqade.atom_arrangement import Square

    atom_pos = Square(4, lattice_spacing=5.0)

    # dynamics
    durations = [0.15, 3.7, 0.15]
    delta_MHz = [-13.0, -13.0, 11.0, 11.0]
    omega_MHz = [0.0, 2.5, 2.5, 0.0]

    Delta = piecewise_linear(durations, [x * 2 * np.pi for x in delta_MHz])
    Omega = piecewise_linear(durations, [x * 2 * np.pi for x in omega_MHz])

    # create Hamiltonian
    program = rydberg_h(atoms_positions=atom_pos, detuning=Delta, amplitude=Omega, phase=None)
    print(program.bloqade.python())

    result = program.bloqade.python()._compile(10)

    assert len(result.tasks) == 1

test_rydberg_h_3()

