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

"""Tests for the Gaussian OpenPulse waveform generator."""

from __future__ import annotations

import textwrap

import pyqasm
import pytest

from qbraid_algorithms.openpulse import GaussianPulse, PulseParams, generate_program


def test_generate_program_emits_expected_qasm() -> None:
    """Generated OpenPulse QASM should match the expected structure and order."""
    pulse = GaussianPulse(amplitude=1.0 + 2.0j, duration="16ns", sigma="4ns")
    params = PulseParams(frame_frequency=5.0e9, frame_phase=0.0, defcal_name="play_gaussian", qubit=0)

    module = generate_program(pulse, params=params)
    actual = pyqasm.dumps(module).strip()

    expected = textwrap.dedent(
        """\
        OPENQASM 3.0;
        defcalgrammar "openpulse";
        cal {
            port d0;
            frame driveframe = newframe(d0, 5000000000.0, 0.0);
            waveform wf = gaussian(1.0 + 2.0im, 16ns, 4ns);
        }
        defcal play_gaussian() $0 {
            play(driveframe, wf);
        }
        """
    ).strip()

    assert actual == expected


def test_generate_program_kwargs_override_names_emits_expected_qasm() -> None:
    """kwargs overrides should be reflected in the emitted QASM (structure + order)."""
    pulse = GaussianPulse(amplitude=0.5 + 0.0j, duration="8ns", sigma="2ns")
    params = PulseParams(frame_frequency=5.0e9, frame_phase=0.0, defcal_name="play_gaussian", qubit=0)

    module = generate_program(
        pulse,
        params=params,
        frame_name="driveframe2",
        waveform_name="wf2",
        port_name="d1",
    )
    actual = pyqasm.dumps(module).strip()

    expected = textwrap.dedent(
        """\
        OPENQASM 3.0;
        defcalgrammar "openpulse";
        cal {
            port d1;
            frame driveframe2 = newframe(d1, 5000000000.0, 0.0);
            waveform wf2 = gaussian(0.5 + 0.0im, 8ns, 2ns);
        }
        defcal play_gaussian() $0 {
            play(driveframe2, wf2);
        }
        """
    ).strip()

    assert actual == expected


def test_unroll_succeeds_when_pulse_dependencies_present() -> None:
    """
    Unrolling requires the OpenPulse parser dependency.

    In CI this should be available via the `pulse` extra (pyqasm[pulse]).
    """
    pulse = GaussianPulse(amplitude=1.0 + 2.0j, duration="16ns", sigma="4ns")
    params = PulseParams(frame_frequency=5.0e9, frame_phase=0.0, defcal_name="play_gaussian", qubit=0)

    module = generate_program(pulse, params=params)

    try:
        module.unroll()
    except ModuleNotFoundError as exc:
        pytest.skip(f"OpenPulse parser dependency not installed: {exc}")

    qasm = pyqasm.dumps(module)
    assert "qubit[1] __PYQASM_QUBITS__;" in qasm
