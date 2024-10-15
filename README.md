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
  <a href="https://www.gnu.org/licenses/gpl-3.0.html">
    <img src="https://img.shields.io/github/license/qBraid/qbraid.svg" alt="License"/>
  </a>
  <a href="https://discord.gg/TPBU2sa8Et">
    <img src="https://img.shields.io/badge/Discord-%235865F2.svg?logo=discord&logoColor=white" alt="Discord"/>
  </a>
</p>

Python package for building, simulating, and benchmarking hybrid quantum-classical algorithms.

[<img src="https://qbraid-static.s3.amazonaws.com/logos/Launch_on_qBraid_white.png" width="150">](https://account.qbraid.com?gitHubUrl=https://github.com/qBraid/qbraid-algorithms.git)

## Installation

qbraid-algorithms requires Python 3.10 or greater, and can be installed with pip as follows:

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

## Community

**We are actively looking for new contributors!**

- Interested in contributing code, or making a PR? See
  [CONTRIBUTING.md](CONTRIBUTING.md)
- For feature requests and bug reports: [Submit an issue](https://github.com/qBraid/qbraid-algorithms/issues)
- For discussions and/or specific questions about qBraid services, [join our discord community](https://discord.gg/TPBU2sa8Et)
- For questions that are more suited for a forum, post to [Stack Exchange](https://quantumcomputing.stackexchange.com/) with the [`qbraid`](https://quantumcomputing.stackexchange.com/questions/tagged/qbraid) tag.
- By participating, you are expected to uphold our [code of conduct](CODE_OF_CONDUCT).

## Acknowledgements

This project was conceived in cooperation with the Quantum Open Source Foundation ([QOSF](https://qosf.org/)).

<a href="https://qosf.org/"><img src="https://qbraid-static.s3.amazonaws.com/logos/qosf.png" width="100px" style="vertical-align: middle;" /></a>

## License

[GNU General Public License v3.0](LICENSE)
