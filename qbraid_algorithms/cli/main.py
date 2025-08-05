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
Entrypoint for the qbraid-algorithms CLI.
"""

import sys

try:
    import typer
    from typing_extensions import Annotated

    from qbraid_algorithms.cli import generate
except ImportError as err:
    print(
        f"Missing required dependency: '{err.name}'.\n\n"
        "Install the dependencies for the qbraid-algorithms CLI with:\n\n"
        "\t$ pip install 'qbraid-algorithms[cli]'",
        file=sys.stderr,
    )
    sys.exit(1)

app = typer.Typer(
    name="qbraid-algorithms",
    help="CLI for qBraid quantum algorithms package",
    context_settings={"help_option_names": ["-h", "--help"]},
)


def version_callback(value: bool):
    """Show the version and exit."""
    if value:
        # pylint: disable-next=import-outside-toplevel
        from qbraid_algorithms._version import __version__

        typer.echo(f"qbraid-algorithms/{__version__}")
        raise typer.Exit(0)


# Add the generate command
app.add_typer(generate.app, name="generate")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            callback=version_callback,
            is_eager=True,
            help="Show the version and exit.",
        ),
    ] = False,
):
    """
    qBraid Algorithms CLI

    Generate quantum algorithm circuits including QFT, IQFT, and Bernstein-Vazirani.

    Examples:
        qbraid-algorithms generate qft --qubits 4
        qbraid-algorithms generate bernvaz --secret "101" --oracle-only
        qbraid-algorithms generate iqft --qubits 3 --output my_iqft.qasm --show
    """
    if ctx.invoked_subcommand and version:
        raise typer.BadParameter(
            "The '--version' option cannot be used with a subcommand."
        )
    if not ctx.invoked_subcommand and not version:
        typer.echo(ctx.get_help())
        raise typer.Exit(0)


if __name__ == "__main__":
    app()
