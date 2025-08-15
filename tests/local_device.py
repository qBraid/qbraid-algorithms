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

"""Temporary Qiskit Aer wrapper local device class for testing."""

from __future__ import annotations

from typing import TYPE_CHECKING

from qbraid.programs import ExperimentType, ProgramSpec
from qbraid.runtime.device import QuantumDevice
from qbraid.runtime.enums import DeviceStatus
from qbraid.runtime.profile import TargetProfile
from qbraid.runtime.result import Result
from qbraid.runtime.result_data import GateModelResultData
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

if TYPE_CHECKING:
    import qiskit.result


class LocalDevice(QuantumDevice):
    """Local device class."""

    def __init__(self):
        profile = TargetProfile(
            device_id="aer_simulator",
            simulator=True,
            experiment_type=ExperimentType.GATE_MODEL,
            program_spec=ProgramSpec(
                QuantumCircuit, alias="qiskit", experiment_type=ExperimentType.GATE_MODEL
            ),
            provider_name="Qiskit",
        )
        super().__init__(profile=profile)
        self.aer_simulator = AerSimulator()

    def status(self) -> DeviceStatus:
        return DeviceStatus.ONLINE

    def transform(self, run_input: QuantumCircuit) -> QuantumCircuit:
        """Transform a circuit for the local device."""
        return transpile(run_input, self.aer_simulator)

    def submit(
        self,
        run_input: QuantumCircuit | list[QuantumCircuit],
        *args,
        shots: int = 1024,
        **kwargs
    ) -> Result:
        """Run a program on the local device."""
        job = self.aer_simulator.run(run_input, shots=shots, **kwargs)
        result: qiskit.result.Result = job.result()
        counts = result.get_counts(run_input)
        return Result(
            device_id=self.id,
            job_id=job.job_id(),
            success=True,
            data=GateModelResultData(
                measurement_counts=counts,
            ),
            **kwargs,
        )
