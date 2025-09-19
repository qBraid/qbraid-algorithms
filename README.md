# qbraid-algorithms

<p align="left">
  <a href="https://github.com/qBraid/qbraid-algorithms/actions/workflows/main.yml">
    <img src="https://github.com/qBraid/qbraid-algorithms/actions/workflows/main.yml/badge.svg?branch=main" alt="CI"/>
  </a>
  <a href="https://codecov.io/gh/qBraid/qbraid-algorithms"> 
    <img src="https://codecov.io/gh/qBraid/qbraid-algorithms/graph/badge.svg?token=7jYcnneDys"/>
  </a>
  <a href="https://pypi.org/project/qbraid-algorithms/">
    <img src="https://img.shields.io/pypi/v/qbraid-algorithms.svg?color=blue" alt="PyPI version"/>
  </a>
  <a href="https://pypi.org/project/qbraid-algorithms/">
    <img src="https://img.shields.io/pypi/pyversions/qbraid-algorithms.svg?color=blue" alt="PyPI version"/>
  </a>
  <a href='http://www.apache.org/licenses/LICENSE-2.0'>
    <img src='https://img.shields.io/github/license/qBraid/qbraid-qir.svg' alt='License'/>
  </a>
  <a href="https://discord.gg/TPBU2sa8Et">
    <img src="https://img.shields.io/badge/Discord-%235865F2.svg?logo=discord&logoColor=white" alt="Discord"/>
  </a>
</p>

Python package for building, simulating, and benchmarking hybrid quantum-classical algorithms.

[<img src="https://qbraid-static.s3.amazonaws.com/logos/Launch_on_qBraid_white.png" width="150">](https://account.qbraid.com?gitHubUrl=https://github.com/qBraid/qbraid-algorithms.git)

## Installation

qbraid-algorithms requires Python 3.11 or greater, and can be installed with pip as follows:

```bash
pip install qbraid-algorithms
```

>[!WARNING]
> **This project is "pre-alpha", and is not yet stable or fully realized. Use with caution, as the API and functionality are subject to significant changes.**

### Install from source

You can also install from source by cloning this repository and running a pip install command
in the root directory of the repository:

```bash
git clone https://github.com/qBraid/qbraid-algorithms.git
cd qbraid-algorithms
pip3 install .
```

## Check version

You can view the version of qbraid-algorithms you have installed within a Python shell as follows:

```python
import qbraid_algorithms

qbraid_algorithms.__version__
```

## Key Features: Load algorithms as PyQASM modules and QASM files

qBraid Algorithms provides a collection of quantum algorithms that can be loaded
as [PyQASM](https://docs.qbraid.com/pyqasm/user-guide/overview) modules, or
you can generate .qasm files to use them as subroutines in your own circuits.

### Loading Algorithms as PyQASM Modules

To load an algorithm as a PyQASM module, use the `load_program` function from the `qbraid_algorithms` package, passing algorithm-specific parameters. For example, to load the Quantum Fourier Transform (QFT) algorithm:

```python
from qbraid_algorithms import qft

qft_module = qft.load_program(3) # Load QFT for 3 qubits
```

Now, you can perform operations with the PyQASM module, such as unrolling, and
converting back to a QASM string:

```python
qft_module.unroll()
qasm_str = pyqasm.dumps(qft_module)
```

### Loading Algorithms as `.qasm` Files

In order to utilize algorithms as subroutines in your own circuits, use the
`generate_subroutine` function for your desired algorithm. By passing algorithm-specific parameters, and optionally a desired output path, you can
generate a .qasm file containing a subroutine for the paramterized circuit. For
example, to generate a QFT subroutine for 4 qubits:

```python
from qbraid_algorithms import qft, iqft
path = "path/to/output" # Specify your desired output path
qft.generate_subroutine(4) # Generate 4-qubit QFT in the current directory
iqft.generate_subroutine(4, path=path) # Generate 4-qubit IQFT in specified path

```

To utilize the generated subroutine in your own circuit, include the generated
.qasm file, and call the subroutine on an qubit register of the size specified
when generating the subroutine. For example, after running

```python
qft.generate_subroutine(4)
```

you can append `include "qft.qasm";` to your OpenQASM file, and call the
subroutine. For example:

```qasm
OPENQASM 3.0;
include "qft.qasm";

qubit[4] q;
bit[4] c;

qft(q);
measure q -> c;
```

## CLI Usage

qBraid Algorithms includes a command-line interface (CLI) for generating quantum algorithm subroutines.

### Installation

To use the CLI, install with CLI dependencies:

```bash
pip install "qbraid-algorithms[cli]"
```

Or install from source:

```bash
pip install -e ".[cli]"
```

### Generate Subroutines

Generate quantum algorithm subroutines that can be included in other circuits:

```bash
# Generate QFT subroutine for 4 qubits
qbraid-algorithms generate qft --qubits 4

# Generate IQFT subroutine for 3 qubits with custom name and show the circuit
qbraid-algorithms generate iqft -q 3 -o my_iqft.qasm --gate-name my_iqft --show

# Generate Bernstein-Vazirani circuit for secret "101" and display it
qbraid-algorithms generate bernvaz --secret "101" --show

# Generate only the oracle for Bernstein-Vazirani
qbraid-algorithms generate bernvaz -s "1001" --oracle-only --show

# Generate QPE subroutine for 4 qubits with a custom unitary gate
qbraid-algorithms generate qpe --unitary-file my_gate.qasm --qubits 4

# Generate QPE with custom output and show the circuit
qbraid-algorithms generate qpe -u gate.qasm -q 3 -o my_qpe.qasm --show
```

### Help

Get help for any command:

```bash
qbraid-algorithms --help
qbraid-algorithms generate --help
qbraid-algorithms generate qft --help
qbraid-algorithms generate iqft --help
qbraid-algorithms generate bernvaz --help
qbraid-algorithms generate qpe --help
qbraid-algorithms generate bernvaz --help
```

### Examples

#### Complete Workflow

1. Generate a QFT subroutine:

   ```bash
   qbraid-algorithms generate qft --qubits 3
   ```

2. Generate a Bernstein-Vazirani oracle and view it:

   ```bash
   qbraid-algorithms generate bernvaz --secret "101" --oracle-only --show
   ```

3. Generate an IQFT circuit with custom output:

   ```bash
   qbraid-algorithms generate iqft --qubits 4 --output my_iqft_4.qasm --show
   ```

4. Generate a QPE subroutine for phase estimation:
   ```bash
   qbraid-algorithms generate qpe --unitary-file t_gate.qasm --qubits 3 --show
   ```

## Community

**We are actively looking for new contributors!**

- Interested in contributing code, or making a PR? See
  [CONTRIBUTING.md](CONTRIBUTING.md)
- For feature requests and bug reports: [Submit an issue](https://github.com/qBraid/qbraid-algorithms/issues)
- For discussions and/or specific questions about qBraid services, [join our discord community](https://discord.gg/TPBU2sa8Et)
- For questions that are more suited for a forum, post to [Stack Exchange](https://quantumcomputing.stackexchange.com/) with the [`qbraid`](https://quantumcomputing.stackexchange.com/questions/tagged/qbraid) tag.
- By participating, you are expected to uphold our [code of conduct](CODE_OF_CONDUCT).

## License

[Apache-2.0 License](LICENSE)
