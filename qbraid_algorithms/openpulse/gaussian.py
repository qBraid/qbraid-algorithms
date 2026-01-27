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

"""
Gaussian OpenPulse Waveform Generator

This module provides a Gaussian pulse waveform generator using OpenQASM 3 OpenPulse
calibration syntax.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import pyqasm


def _complex_to_qasm(z: complex) -> str:
    """Convert a Python complex number to an OpenQASM complex literal."""
    a = float(z.real)
    b = float(z.imag)
    sign = "+" if b >= 0 else "-"
    return f"{a} {sign} {abs(b)}im"

@dataclass(frozen=True)
class PulseParams:
    """Common parameters for building an OpenPulse calibration program.

        frame_frequency (float): Initial frequency of the drive frame in Hz.
        frame_phase (float): Initial phase of the drive frame in radians.
        port_name (str): Name of the OpenPulse port.
        frame_name (str): Name of the OpenPulse frame.
        waveform_name (str): Identifier for the Gaussian waveform.
        defcal_name (str): Name of the generated calibration routine.
        qubit (int): Target qubit index for the calibration routine.
    """

    frame_frequency: float = 5.0e9
    frame_phase: float = 0.0
    port_name: str = "d0"
    frame_name: str = "driveframe"
    waveform_name: str = "wf"
    defcal_name: str = "play_pulse"
    qubit: int = 0

@dataclass(frozen=True)
class GaussianPulse:
    """A minimal Gaussian waveform spec for OpenPulse.

        amplitude (complex): Complex amplitude of the Gaussian pulse.
        duration (str): Total pulse duration (e.g. "16ns").
        sigma (str): Standard deviation of the Gaussian envelope.

    Notes:
      - duration/sigma are strings like "16ns", "100e-6s", etc.
      - amplitude is complex (OpenQASM complex literal).
    """

    amplitude: complex
    duration: str
    sigma: str

    def to_waveform_qasm(self, var_name: str = "wf") -> str:
        """Generate the OpenQASM waveform definition for this Gaussian pulse."""
        amp = _complex_to_qasm(self.amplitude)
        return f"waveform {var_name} = gaussian({amp}, {self.duration}, {self.sigma});"


def generate_program(
    pulse: GaussianPulse,
    params: PulseParams | None = None,
    **kwargs: Any,
) -> "pyqasm.QasmModule":
    """
    Load a Gaussian OpenPulse waveform program as a pyqasm module.

    Args:
        pulse (GaussianPulse): Pulse specification (amplitude, duration, sigma).
        params (PulseParams | None): Common OpenPulse/program parameters.
        **kwargs: Overrides for fields in PulseParams (e.g. frame_name="...", qubit=1).

    Returns:
        (PyQasm Module) pyqasm module containing the Gaussian OpenPulse program
    """
    params = params or PulseParams()
    p = {**asdict(params), **kwargs}

    wf_line = pulse.to_waveform_qasm(var_name=p["waveform_name"])

    qasm = f"""OPENQASM 3.0;
defcalgrammar "openpulse";

cal {{
    port {p["port_name"]};
    frame {p["frame_name"]} = newframe({p["port_name"]}, {p["frame_frequency"]}, {p["frame_phase"]});
    {wf_line}
}}

defcal {p["defcal_name"]} ${p["qubit"]} {{
    play({p["frame_name"]}, {p["waveform_name"]});
}}
"""

    module = pyqasm.loads(qasm)
    return module
