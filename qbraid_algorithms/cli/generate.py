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
Generate subroutines and oracles for quantum algorithms.
"""

import os

import typer
from typing_extensions import Annotated

# Import modules with error handling
try:
    from qbraid_algorithms import qft, iqft
    from qbraid_algorithms import bernstein_vazirani as bv
except ImportError as e:
    typer.echo(f"Missing required module: {e}", err=True)
    raise typer.Exit(1)

app = typer.Typer(
    name="generate",
    help="Generate quantum algorithm subroutines and oracles",
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.command(name="qft")
def generate_qft(
    qubits: Annotated[
        int,
        typer.Option(
            "--qubits",
            "-q",
            help="Number of qubits for the QFT circuit.",
            min=1,
            max=20,
        ),
    ],
    output: Annotated[
        str,
        typer.Option("--output", "-o", help="Output filename for the QFT subroutine."),
    ] = "qft.qasm",
    show_circuit: Annotated[
        bool, typer.Option("--show", help="Display the generated circuit QASM code.")
    ] = False,
):
    """
    Generate a QFT (Quantum Fourier Transform) subroutine.

    Creates a QASM file containing a QFT subroutine that can be included in other circuits.

    Examples:
        qbraid-algorithms generate qft --qubits 4
        qbraid-algorithms generate qft -q 3 -o my_qft.qasm --gate-name my_qft --show
    """
    try:
        qft.generate_subroutine(qubits)
        typer.echo(f"QFT subroutine for {qubits} qubits generated successfully.")
        typer.echo(f"Output: {os.path.abspath('qft.qasm')}")

        # Rename if custom output specified
        if output != "qft.qasm":
            os.rename("qft.qasm", output)
            typer.echo(f"Renamed to: {os.path.abspath(output)}")

        # Show circuit if requested
        if show_circuit:
            final_output = output if output != "qft.qasm" else "qft.qasm"
            with open(final_output, "r", encoding="utf-8") as f:
                qasm_content = f.read()
            typer.echo("Generated QASM:")
            typer.echo("-" * 50)
            typer.echo(qasm_content)
            typer.echo("-" * 50)

    except Exception as e:
        typer.echo(f"Error generating QFT subroutine: {e}", err=True)
        raise typer.Exit(1)


@app.command(name="iqft")
def generate_iqft(
    qubits: Annotated[
        int,
        typer.Option(
            "--qubits",
            "-q",
            help="Number of qubits for the IQFT circuit.",
            min=1,
            max=20,
        ),
    ],
    output: Annotated[
        str,
        typer.Option("--output", "-o", help="Output filename for the IQFT subroutine."),
    ] = "iqft.qasm",
    show_circuit: Annotated[
        bool, typer.Option("--show", help="Display the generated circuit QASM code.")
    ] = False,
):
    """
    Generate an IQFT (Inverse Quantum Fourier Transform) subroutine.

    Creates a QASM file containing an IQFT subroutine that can be included in other circuits.

    Examples:
        qbraid-algorithms generate iqft --qubits 4
        qbraid-algorithms generate iqft -q 3 -o my_iqft.qasm --gate-name my_iqft --show
    """
    try:
        iqft.generate_subroutine(qubits)
        typer.echo(f"IQFT subroutine for {qubits} qubits generated successfully.")
        typer.echo(f"Output: {os.path.abspath('iqft.qasm')}")

        # Rename if custom output specified
        if output != "iqft.qasm":
            os.rename("iqft.qasm", output)
            typer.echo(f"Renamed to: {os.path.abspath(output)}")

        # Show circuit if requested
        if show_circuit:
            final_output = output if output != "iqft.qasm" else "iqft.qasm"
            with open(final_output, "r", encoding="utf-8") as f:
                qasm_content = f.read()
            typer.echo("Generated QASM:")
            typer.echo("-" * 50)
            typer.echo(qasm_content)
            typer.echo("-" * 50)

    except Exception as e:
        typer.echo(f"Error generating IQFT subroutine: {e}", err=True)
        raise typer.Exit(1)


@app.command(name="bernvaz")
def generate_bernvaz(
    secret: Annotated[
        str,
        typer.Option(
            "--secret",
            "-s",
            help="Binary secret string for Bernstein-Vazirani algorithm.",
        ),
    ],
    oracle_only: Annotated[
        bool,
        typer.Option(
            "--oracle-only", help="Generate only the oracle, not the complete circuit."
        ),
    ] = False,
    output: Annotated[
        str, typer.Option("--output", "-o", help="Output filename.")
    ] = None,
    gate_name: Annotated[
        str, typer.Option("--gate-name", "-g", help="Name for the gate.")
    ] = None,
    show_circuit: Annotated[
        bool, typer.Option("--show", help="Display the generated circuit QASM code.")
    ] = False,
):
    """
    Generate Bernstein-Vazirani algorithm circuit or oracle.

    Creates a QASM file for the Bernstein-Vazirani algorithm with the specified secret string.
    Use --oracle-only to generate just the oracle subroutine.

    Examples:
        qbraid-algorithms generate bernvaz --secret "101"
        qbraid-algorithms generate bernvaz -s "1001" --oracle-only --show
        qbraid-algorithms generate bernvaz -s "110" -o my_bv.qasm
    """
    # Validate secret string
    if not secret or not all(c in "01" for c in secret):
        typer.echo(
            "Error: Secret must be a non-empty binary string (e.g., '101')", err=True
        )
        raise typer.Exit(1)

    # Set default filenames and gate names
    if oracle_only:
        default_output = f"bernvaz_oracle_{secret}.qasm"
        default_gate_name = f"bernvaz_oracle_{secret}"
        typer.echo(f"Generating Bernstein-Vazirani oracle for secret '{secret}'...")
    else:
        default_output = f"bernvaz_{secret}.qasm"
        default_gate_name = f"bernvaz_{secret}"
        typer.echo(f"Generating Bernstein-Vazirani circuit for secret '{secret}'...")

    output = output or default_output
    gate_name = gate_name or default_gate_name

    try:
        if oracle_only:
            # Generate oracle only
            bv.generate_oracle(secret)
            generated_file = "oracle.qasm"
            typer.echo("Bernstein-Vazirani oracle generated successfully.")
        else:
            # Generate complete circuit
            bv.generate_subroutine(secret)
            generated_file = "bernvaz.qasm"
            typer.echo("Bernstein-Vazirani circuit generated successfully.")

        # Rename if custom output specified
        if output != default_output:
            os.rename(generated_file, output)
            typer.echo(f"Renamed to: {os.path.abspath(output)}")
            final_file = output
        else:
            final_file = generated_file

        typer.echo(f"Output: {os.path.abspath(final_file)}")
        typer.echo(f"Secret string: {secret}")
        typer.echo(f"Qubits needed: {len(secret)} + 1 ancilla")

        # Show circuit if requested
        if show_circuit:
            with open(final_file, "r", encoding="utf-8") as f:
                qasm_content = f.read()
            typer.echo("Generated QASM:")
            typer.echo("-" * 50)
            typer.echo(qasm_content)
            typer.echo("-" * 50)

    except Exception as e:
        typer.echo(
            f"Error generating Bernstein-Vazirani {'oracle' if oracle_only else 'circuit'}: {e}",
            err=True,
        )
        raise typer.Exit(1)


@app.callback()
def generate_main():
    """
    Generate quantum algorithm subroutines and oracles.

    This command group allows you to generate QASM files for various quantum algorithms
    that can be used as subroutines in larger quantum programs.
    """
