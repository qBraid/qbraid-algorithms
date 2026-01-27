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

import pyqasm
import pytest

from qbraid_algorithms.openpulse import GaussianPulse, PulseParams, generate_program


def test_generate_program_dumps_contains_expected_sections() -> None:
    """Verify generated OpenPulse program contains expected QASM sections."""
    pulse = GaussianPulse(amplitude=1.0 + 2.0j, duration="16ns", sigma="4ns")
    params = PulseParams(frame_frequency=5.0e9, frame_phase=0.0, defcal_name="play_gaussian", qubit=0)

    module = generate_program(pulse, params=params)
    qasm = pyqasm.dumps(module)

    assert 'defcalgrammar "openpulse";' in qasm
    assert "cal {" in qasm
    assert "port d0;" in qasm
    assert "frame driveframe = newframe(d0, 5000000000.0, 0.0);" in qasm
    assert "waveform wf = gaussian(1.0 + 2.0im, 16ns, 4ns);" in qasm
    assert "defcal play_gaussian" in qasm
    assert "play(driveframe, wf);" in qasm


def test_generate_program_kwargs_override_names() -> None:
    """Verify kwargs correctly override parameters."""
    pulse = GaussianPulse(amplitude=0.5 + 0.0j, duration="8ns", sigma="2ns")
    params = PulseParams(frame_frequency=5.0e9, frame_phase=0.0, defcal_name="play_gaussian", qubit=0)

    module = generate_program(
        pulse,
        params=params,
        frame_name="driveframe2",
        waveform_name="wf2",
        port_name="d1",
    )
    qasm = pyqasm.dumps(module)

    assert "port d1;" in qasm
    assert "frame driveframe2 = newframe(d1, 5000000000.0, 0.0);" in qasm
    assert "waveform wf2 = gaussian(0.5 + 0.0im, 8ns, 2ns);" in qasm
    assert "play(driveframe2, wf2);" in qasm


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
