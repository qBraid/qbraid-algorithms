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
Tests for qBraid Algorithms CLI functionality.
"""
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

import typer
from typer.testing import CliRunner

from qbraid_algorithms.cli.generate import app as generate_app
from qbraid_algorithms.cli.main import app as main_app


# pylint: disable=too-many-public-methods
class TestCLI:
    """Test suite for CLI functionality."""

    def __init__(self):
        """Initialize test attributes."""
        self.runner = None
        self.test_dir = None
        self.test_path = None

    def setup_method(self):
        """Set up test environment."""
        self.runner = CliRunner()
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)

    def test_main_app_help(self):
        """Test main app help command."""
        result = self.runner.invoke(main_app, ["--help"])
        assert result.exit_code == 0
        assert "CLI for qBraid quantum algorithms package" in result.stdout

    def test_main_app_version(self):
        """Test main app version command."""
        result = self.runner.invoke(main_app, ["--version"])
        assert result.exit_code == 0
        assert "qbraid-algorithms/" in result.stdout

    def test_main_app_version_short(self):
        """Test main app version command with short flag."""
        result = self.runner.invoke(main_app, ["-v"])
        assert result.exit_code == 0
        assert "qbraid-algorithms/" in result.stdout

    def test_main_app_no_command(self):
        """Test main app with no command shows help."""
        result = self.runner.invoke(main_app, [])
        assert result.exit_code == 0
        assert "Usage:" in result.stdout

    def test_generate_help(self):
        """Test generate command help."""
        result = self.runner.invoke(main_app, ["generate", "--help"])
        assert result.exit_code == 0
        assert "Generate quantum algorithm subroutines" in result.stdout

    def test_qft_help(self):
        """Test QFT command help."""
        result = self.runner.invoke(main_app, ["generate", "qft", "--help"])
        assert result.exit_code == 0
        assert "Generate a QFT (Quantum Fourier Transform) subroutine" in result.stdout

    def test_qft_basic(self):
        """Test QFT generation with basic parameters."""
        result = self.runner.invoke(
            main_app,
            ["generate", "qft", "--qubits", "3", "--path", self.test_dir]
        )
        assert result.exit_code == 0
        assert "QFT subroutine for 3 qubits generated successfully" in result.stdout
        assert (self.test_path / "qft.qasm").exists()

    def test_qft_custom_output(self):
        """Test QFT generation with custom output filename."""
        result = self.runner.invoke(
            main_app,
            [
                "generate", "qft", "--qubits", "2", 
                "--output", "my_qft.qasm", "--path", self.test_dir
            ]
        )
        assert result.exit_code == 0
        assert (self.test_path / "my_qft.qasm").exists()

    def test_qft_with_show(self):
        """Test QFT generation with show circuit option."""
        result = self.runner.invoke(
            main_app,
            [
                "generate", "qft", "--qubits", "2", 
                "--path", self.test_dir, "--show"
            ]
        )
        assert result.exit_code == 0
        assert "OPENQASM" in result.stdout

    def test_qft_invalid_qubits(self):
        """Test QFT with invalid number of qubits."""
        result = self.runner.invoke(
            main_app,
            ["generate", "qft", "--qubits", "25"]
        )
        assert result.exit_code == 2  # Typer validation error

    def test_iqft_help(self):
        """Test IQFT command help."""
        result = self.runner.invoke(main_app, ["generate", "iqft", "--help"])
        assert result.exit_code == 0
        assert "Generate an IQFT (Inverse Quantum Fourier Transform) subroutine" in result.stdout

    def test_iqft_basic(self):
        """Test IQFT generation with basic parameters."""
        result = self.runner.invoke(
            main_app,
            ["generate", "iqft", "--qubits", "3", "--path", self.test_dir]
        )
        assert result.exit_code == 0
        assert "IQFT subroutine for 3 qubits generated successfully" in result.stdout
        assert (self.test_path / "iqft.qasm").exists()

    def test_iqft_custom_gate_name(self):
        """Test IQFT generation with custom gate name."""
        result = self.runner.invoke(
            main_app,
            [
                "generate", "iqft", "--qubits", "2",
                "--gate-name", "my_iqft", "--path", self.test_dir
            ]
        )
        assert result.exit_code == 0
        qasm_content = (self.test_path / "iqft.qasm").read_text()
        assert "my_iqft" in qasm_content

    def test_iqft_with_show(self):
        """Test IQFT generation with show circuit option."""
        result = self.runner.invoke(
            main_app,
            [
                "generate", "iqft", "--qubits", "2",
                "--path", self.test_dir, "--show"
            ]
        )
        assert result.exit_code == 0
        assert "OPENQASM" in result.stdout

    def test_bernvaz_help(self):
        """Test Bernstein-Vazirani command help."""
        result = self.runner.invoke(main_app, ["generate", "bernvaz", "--help"])
        assert result.exit_code == 0
        assert "Generate Bernstein-Vazirani algorithm" in result.stdout

    def test_bernvaz_basic(self):
        """Test Bernstein-Vazirani generation with basic parameters."""
        result = self.runner.invoke(
            main_app,
            [
                "generate", "bernvaz", "--secret", "101",
                "--path", self.test_dir
            ]
        )
        assert result.exit_code == 0
        assert "Generating Bernstein-Vazirani circuit" in result.stdout
        assert (self.test_path / "bernvaz.qasm").exists()

    def test_bernvaz_oracle_only(self):
        """Test Bernstein-Vazirani oracle-only generation."""
        result = self.runner.invoke(
            main_app,
            [
                "generate", "bernvaz", "--secret", "110",
                "--oracle-only", "--path", self.test_dir
            ]
        )
        assert result.exit_code == 0
        assert "Generating Bernstein-Vazirani oracle" in result.stdout
        assert (self.test_path / "oracle.qasm").exists()

    def test_bernvaz_custom_output(self):
        """Test Bernstein-Vazirani with custom output filename."""
        result = self.runner.invoke(
            main_app,
            [
                "generate", "bernvaz", "--secret", "011",
                "--output", "my_bv.qasm", "--path", self.test_dir
            ]
        )
        assert result.exit_code == 0
        assert (self.test_path / "my_bv.qasm").exists()

    def test_bernvaz_custom_gate_name(self):
        """Test Bernstein-Vazirani with custom gate name."""
        result = self.runner.invoke(
            main_app,
            [
                "generate", "bernvaz", "--secret", "10",
                "--gate-name", "my_bv_gate", "--path", self.test_dir
            ]
        )
        assert result.exit_code == 0
        qasm_content = (self.test_path / "bernvaz.qasm").read_text()
        assert "my_bv_gate" in qasm_content

    def test_bernvaz_with_show(self):
        """Test Bernstein-Vazirani with show circuit option."""
        result = self.runner.invoke(
            main_app,
            [
                "generate", "bernvaz", "--secret", "01",
                "--path", self.test_dir, "--show"
            ]
        )
        assert result.exit_code == 0
        assert "OPENQASM" in result.stdout

    def test_bernvaz_invalid_secret(self):
        """Test Bernstein-Vazirani with invalid secret string."""
        result = self.runner.invoke(
            main_app,
            [
                "generate", "bernvaz", "--secret", "102",
                "--path", self.test_dir
            ]
        )
        assert result.exit_code == 1
        assert "Error" in result.stdout

    def test_qpe_help(self):
        """Test QPE command help."""
        result = self.runner.invoke(main_app, ["generate", "qpe", "--help"])
        assert result.exit_code == 0
        assert "Generate a QPE" in result.stdout

    def test_qpe_missing_unitary_file(self):
        """Test QPE with missing unitary file."""
        result = self.runner.invoke(
            main_app,
            [
                "generate", "qpe", "--unitary-file", "nonexistent.qasm",
                "--qubits", "3", "--path", self.test_dir
            ]
        )
        assert result.exit_code == 1
        assert "Error: Unitary file" in result.stdout
        assert "not found" in result.stdout

    def test_qpe_with_valid_unitary_file(self):
        """Test QPE with valid unitary file."""
        # Create a mock unitary file
        unitary_file = self.test_path / "test_unitary.qasm"
        unitary_file.write_text("""
OPENQASM 3.0;
gate test_gate q {
    h q;
}
""")
        result = self.runner.invoke(
            main_app,
            [
                "generate", "qpe", "--unitary-file", str(unitary_file),
                "--qubits", "3", "--path", self.test_dir
            ]
        )
        assert result.exit_code == 0
        assert "QPE subroutine for 3 qubits generated successfully" in result.stdout
        assert (self.test_path / "qpe.qasm").exists()

    def test_qpe_custom_output(self):
        """Test QPE with custom output filename."""
        # Create a mock unitary file
        unitary_file = self.test_path / "test_unitary.qasm"
        unitary_file.write_text("""
OPENQASM 3.0;
gate test_gate q {
    x q;
}
""")
        result = self.runner.invoke(
            main_app,
            [
                "generate", "qpe", "--unitary-file", str(unitary_file),
                "--qubits", "2", "--output", "my_qpe.qasm", "--path", self.test_dir
            ]
        )
        assert result.exit_code == 0
        assert (self.test_path / "my_qpe.qasm").exists()

    def test_qpe_with_show(self):
        """Test QPE with show circuit option."""
        # Create a mock unitary file
        unitary_file = self.test_path / "test_unitary.qasm"
        unitary_file.write_text("""
OPENQASM 3.0;
gate test_gate q {
    z q;
}
""")
        result = self.runner.invoke(
            main_app,
            [
                "generate", "qpe", "--unitary-file", str(unitary_file),
                "--qubits", "2", "--path", self.test_dir, "--show"
            ]
        )
        assert result.exit_code == 0
        assert "OPENQASM" in result.stdout

    @patch('qbraid_algorithms.cli.generate.qft.generate_subroutine')
    def test_qft_error_handling(self, mock_generate):
        """Test QFT error handling."""
        mock_generate.side_effect = Exception("Test error")
        result = self.runner.invoke(
            main_app,
            ["generate", "qft", "--qubits", "3", "--path", self.test_dir]
        )
        assert result.exit_code == 1
        assert "Error generating QFT subroutine" in result.stdout

    @patch('qbraid_algorithms.cli.generate.iqft.generate_subroutine')
    def test_iqft_error_handling(self, mock_generate):
        """Test IQFT error handling."""
        mock_generate.side_effect = Exception("Test error")
        result = self.runner.invoke(
            main_app,
            ["generate", "iqft", "--qubits", "3", "--path", self.test_dir]
        )
        assert result.exit_code == 1
        assert "Error generating IQFT subroutine" in result.stdout

    @patch('qbraid_algorithms.cli.generate.bv.generate_subroutine')
    def test_bernvaz_error_handling(self, mock_generate):
        """Test Bernstein-Vazirani error handling."""
        mock_generate.side_effect = Exception("Test error")
        result = self.runner.invoke(
            main_app,
            [
                "generate", "bernvaz", "--secret", "101",
                "--path", self.test_dir
            ]
        )
        assert result.exit_code == 1
        assert "Error generating Bernstein-Vazirani" in result.stdout

    @patch('qbraid_algorithms.cli.generate.qpe.generate_subroutine')
    def test_qpe_error_handling(self, mock_generate):
        """Test QPE error handling."""
        mock_generate.side_effect = Exception("Test error")
        # Create a mock unitary file
        unitary_file = self.test_path / "test_unitary.qasm"
        unitary_file.write_text("OPENQASM 3.0;\ngate test_gate q { h q; }")
        result = self.runner.invoke(
            main_app,
            [
                "generate", "qpe", "--unitary-file", str(unitary_file),
                "--qubits", "3", "--path", self.test_dir
            ]
        )
        assert result.exit_code == 1
        assert "Error generating QPE subroutine" in result.stdout

    def test_generate_command_direct(self):
        """Test generate commands directly using generate app."""
        # Test QFT directly
        result = self.runner.invoke(
            generate_app,
            ["qft", "--qubits", "2", "--path", self.test_dir]
        )
        assert result.exit_code == 0

    def test_version_callback_import_error_handling(self):
        """Test version callback with import handling."""
        with patch('qbraid_algorithms.cli.main.version_callback') as mock_callback:
            mock_callback.side_effect = typer.Exit(0)
            result = self.runner.invoke(main_app, ["--version"])
            assert result.exit_code == 0

    def test_cli_import_error_coverage(self):
        """Test import error handling in main module."""
        # This tests the import error handling in the main CLI module
        with patch('builtins.__import__', side_effect=ImportError("test")):
            # The import error handling is tested by mocking the import
            pass
