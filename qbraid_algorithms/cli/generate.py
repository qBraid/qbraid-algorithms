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
    from qbraid_algorithms import qft, iqft, qpe
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
    path: Annotated[
        str,
        typer.Option(
            "--path",
            "-p",
            help="Directory path where the QFT subroutine will be created.",
        ),
    ] = None,
    show_circuit: Annotated[
        bool, typer.Option("--show", help="Display the generated circuit QASM code.")
    ] = False,
):
    """
    Generate a QFT (Quantum Fourier Transform) subroutine.

    Creates a QASM file containing a QFT subroutine that can be included in other circuits.

    Examples:
        qbraid-algorithms generate qft --qubits 4
        qbraid-algorithms generate qft -q 3 -o my_qft.qasm --path /tmp --show
    """
    try:
        # Determine the target directory and filename
        target_dir = path if path else os.getcwd()
        target_file = os.path.join(target_dir, output)

        # Generate the subroutine using the path parameter
        qft.generate_subroutine(qubits, quiet=True, path=target_dir)

        # Rename to custom output if needed
        generated_file = os.path.join(target_dir, "qft.qasm")
        if output != "qft.qasm":
            os.rename(generated_file, target_file)
            final_file = target_file
        else:
            final_file = generated_file

        typer.echo(f"QFT subroutine for {qubits} qubits generated successfully.")
        typer.echo(f"Output: {os.path.abspath(final_file)}")

        # Show circuit if requested
        if show_circuit:
            with open(final_file, "r", encoding="utf-8") as f:
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
    path: Annotated[
        str,
        typer.Option(
            "--path",
            "-p",
            help="Directory path where the IQFT subroutine will be created.",
        ),
    ] = None,
    show_circuit: Annotated[
        bool, typer.Option("--show", help="Display the generated circuit QASM code.")
    ] = False,
):
    """
    Generate an IQFT (Inverse Quantum Fourier Transform) subroutine.

    Creates a QASM file containing an IQFT subroutine that can be included in other circuits.

    Examples:
        qbraid-algorithms generate iqft --qubits 4
        qbraid-algorithms generate iqft -q 3 -o my_iqft.qasm --path /tmp --show
    """
    try:
        # Determine the target directory and filename
        target_dir = path if path else os.getcwd()
        target_file = os.path.join(target_dir, output)

        # Generate the subroutine using the path parameter
        iqft.generate_subroutine(qubits, quiet=True, path=target_dir)

        # Rename to custom output if needed
        generated_file = os.path.join(target_dir, "iqft.qasm")
        if output != "iqft.qasm":
            os.rename(generated_file, target_file)
            final_file = target_file
        else:
            final_file = generated_file

        typer.echo(f"IQFT subroutine for {qubits} qubits generated successfully.")
        typer.echo(f"Output: {os.path.abspath(final_file)}")

        # Show circuit if requested
        if show_circuit:
            with open(final_file, "r", encoding="utf-8") as f:
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
    *,
    oracle_only: Annotated[
        bool,
        typer.Option(
            "--oracle-only", help="Generate only the oracle, not the complete circuit."
        ),
    ] = False,
    output: Annotated[
        str, typer.Option("--output", "-o", help="Output filename.")
    ] = None,
    path: Annotated[
        str,
        typer.Option(
            "--path",
            "-p",
            help="Directory path where the Bernstein-Vazirani files will be created.",
        ),
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
        qbraid-algorithms generate bernvaz -s "110" -o my_bv.qasm --path /tmp
    """
    # Validate secret string
    if not secret or not all(c in "01" for c in secret):
        typer.echo(
            "Error: Secret must be a non-empty binary string (e.g., '101')", err=True
        )
        raise typer.Exit(1)

    # Set default filenames and gate names
    if oracle_only:
        default_output = "oracle.qasm"
        default_gate_name = f"bernvaz_oracle_{secret}"
        typer.echo(f"Generating Bernstein-Vazirani oracle for secret '{secret}'...")
    else:
        default_output = "bernvaz.qasm"
        default_gate_name = f"bernvaz_{secret}"
        typer.echo(f"Generating Bernstein-Vazirani circuit for secret '{secret}'...")

    output = output or default_output
    gate_name = gate_name or default_gate_name

    try:
        # Determine the target directory and filename
        target_dir = path if path else os.getcwd()
        target_file = os.path.join(target_dir, output)

        if oracle_only:
            # Generate oracle only
            bv.generate_oracle(secret, quiet=True, path=target_dir)
            generated_file = os.path.join(target_dir, "oracle.qasm")
            typer.echo("Bernstein-Vazirani oracle generated successfully.")
        else:
            # Generate complete circuit
            bv.generate_subroutine(secret, quiet=True, path=target_dir)
            generated_file = os.path.join(target_dir, "bernvaz.qasm")
            typer.echo("Bernstein-Vazirani circuit generated successfully.")

        # Rename if custom output specified
        if output != default_output:
            os.rename(generated_file, target_file)
            final_file = target_file
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


@app.command(name="qpe")
def generate_qpe(
    unitary_file: Annotated[
        str,
        typer.Option(
            "--unitary-file",
            "-u",
            help="Path to QASM file defining the unitary gate U for phase estimation.",
        ),
    ],
    qubits: Annotated[
        int,
        typer.Option(
            "--qubits",
            "-q",
            help="Number of qubits for the phase estimation register.",
            min=1,
            max=20,
        ),
    ] = 4,
    output: Annotated[
        str,
        typer.Option("--output", "-o", help="Output filename for the QPE subroutine."),
    ] = "qpe.qasm",
    path: Annotated[
        str,
        typer.Option(
            "--path",
            "-p",
            help="Directory path where the QPE subroutine will be created.",
        ),
    ] = None,
    show_circuit: Annotated[
        bool, typer.Option("--show", help="Display the generated circuit QASM code.")
    ] = False,
):
    """
    Generate a QPE (Quantum Phase Estimation) subroutine.

    Creates a QASM file containing a QPE subroutine that estimates the phase of
    a given unitary operator. Requires a QASM file defining the unitary gate.

    Examples:
        qbraid-algorithms generate qpe --unitary-file my_gate.qasm --qubits 4
        qbraid-algorithms generate qpe -u gate.qasm -q 3 -o my_qpe.qasm --path /tmp --show
    """
    # Validate unitary file exists
    if not os.path.exists(unitary_file):
        typer.echo(f"Error: Unitary file '{unitary_file}' not found.", err=True)
        raise typer.Exit(1)

    try:
        # Determine the target directory and filename
        target_dir = path if path else os.getcwd()
        target_file = os.path.join(target_dir, output)

        # Generate the subroutine using the path parameter
        qpe.generate_subroutine(unitary_file, qubits, quiet=True, path=target_dir)

        # Rename to custom output if needed
        generated_file = os.path.join(target_dir, "qpe.qasm")
        if output != "qpe.qasm":
            os.rename(generated_file, target_file)
            final_file = target_file
        else:
            final_file = generated_file

        typer.echo(f"QPE subroutine for {qubits} qubits generated successfully.")
        typer.echo(f"Unitary file: {os.path.abspath(unitary_file)}")
        typer.echo(f"Output: {os.path.abspath(final_file)}")

        # Show circuit if requested
        if show_circuit:
            with open(final_file, "r", encoding="utf-8") as f:
                qasm_content = f.read()
            typer.echo("Generated QASM:")
            typer.echo("-" * 50)
            typer.echo(qasm_content)
            typer.echo("-" * 50)

    except Exception as e:
        typer.echo(f"Error generating QPE subroutine: {e}", err=True)
        raise typer.Exit(1)


@app.callback()
def generate_main():
    """
    Generate quantum algorithm subroutines and oracles.

    This command group allows you to generate QASM files for various quantum algorithms
    that can be used as subroutines in larger quantum programs.
    """
