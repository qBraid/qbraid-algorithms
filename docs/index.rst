.. raw:: html

   <html>
   <head>
   <meta name="viewport" content="width=device-width, initial-scale=1">
   <style>
   * {
   box-sizing: border-box;
   }

   body {
   font-family: Arial, Helvetica, sans-serif;
   }

   /* Float four columns side by side */
   .column {
   display: inline-block;
   vertical-align: middle;
   float: none;
   width: 25%;
   padding: 0 10px;
   }

   /* Remove extra left and right margins, due to padding */
   .row {
   text-align: center;
   margin:0 auto;
   }

   /* Clear floats after the columns */
   .row:after {
   content: "";
   display: table;
   clear: both;
   }

   /* Responsive columns */
   @media screen and (max-width: 600px) {
      .column {
         width: 100%;
         margin-bottom: 20px;
      }
   }

   </style>
   </head>
   <body>
   <h1 style="text-align: center">
      <img src="_static/logo.png" alt="qbraid logo" style="width:60px;height:60px;">
      <span> qBraid</span>
      <span style="color:#808080"> | algorithms</span>
   </h1>
   <p style="text-align:center;font-style:italic;color:#808080">
      Build Quantum Algorithms with qBraid.
   </p>
   </body>
   </html>

|

:Release: |release|

Overview
--------

`qBraid Algorithms <https://docs.qbraid.com/qbraid-algorithms/user-guide/overview>`_ is a Python package designed for quantum algorithm development, implementation, and execution. Built on the `OpenQASM3 <https://openqasm.com/>`_ standard, this library provides researchers, developers, and quantum computing enthusiasts with a robust toolkit for exploring and deploying quantum algorithms across various domains.

**Key Features:**

* **Comprehensive Algorithm Library**: Implementation of fundamental quantum algorithms including Grover's search, Quantum Fourier Transform (QFT), Quantum Phase Estimation (QPE), and advanced techniques like amplitude amplification and Hamiltonian evolution.

* **OpenQASM 3 Integration**: Native support for OpenQASM 3, enabling seamless integration with modern quantum hardware and simulators while maintaining compatibility with the evolving quantum computing ecosystem.

* **Modular Architecture**: Clean, modular design that allows for easy extension, customization, and integration into existing quantum computing workflows.

* **Research-Ready Implementation**: Optimized for both educational purposes and cutting-edge research, with implementations suitable for near-term quantum devices (NISQ era) and fault-tolerant quantum computers.

* **Hardware Agnostic**: Designed to work across different quantum computing platforms and simulators, providing flexibility in deployment and testing.

Installation
-------------

qbraid-algorithms requires Python 3.11 or greater, and can be installed with pip as follows:

.. code-block:: bash

   pip install qbraid-algorithms


Install from Source
--------------------

You can also install from source by cloning this repository and running a pip install command in the root directory of the repository:

.. code-block:: bash

   git clone https://github.com/qBraid/qbraid-algorithms.git
   cd qbraid-algorithms
   pip3 install .


Resources
----------

- `User Guide <https://docs.qbraid.com/qbraid-algorithms/user-guide/overview>`_
- `Example Notebooks <https://github.com/qBraid/qbraid-algorithms/tree/main/examples>`_
- `API Reference <https://sdk.qbraid.com/qBraid/api/qbraid_algorithms.html>`_
- `Source Code <https://github.com/qBraid/qbraid-algorithms>`_

.. toctree::
   :maxdepth: 1
   :caption: SDK API Reference
   :hidden:

   qbraid <https://sdk.qbraid.com/qBraid/api/qbraid.html>
   qbraid.programs <https://sdk.qbraid.com/qBraid/api/qbraid.programs.html>
   qbraid.interface <https://sdk.qbraid.com/qBraid/api/qbraid.interface.html>
   qbraid.transpiler <https://sdk.qbraid.com/qBraid/api/qbraid.transpiler.html>
   qbraid.passes <https://sdk.qbraid.com/qBraid/api/qbraid.passes.html>
   qbraid.runtime <https://sdk.qbraid.com/qBraid/api/qbraid.runtime.html>
   qbraid.visualization <https://sdk.qbraid.com/qBraid/api/qbraid.visualization.html>

.. toctree::
   :caption: QIR API Reference
   :hidden:

   qbraid_qir <https://sdk.qbraid.com/qbraid-qir/api/qbraid_qir.html>
   qbraid_qir.cirq <https://sdk.qbraid.com/qbraid-qir/api/qbraid_qir.cirq.html>
   qbraid_qir.qasm3 <https://sdk.qbraid.com/qbraid-qir/api/qbraid_qir.qasm3.html>

.. toctree::
   :caption: CORE API Reference
   :hidden:

   qbraid_core <https://sdk.qbraid.com/qbraid-core/api/qbraid_core.html>
   qbraid_core.services <https://sdk.qbraid.com/qbraid-core/api/qbraid_core.services.html>

.. toctree::
   :caption: PYQASM API Reference
   :hidden:

   pyqasm <https://sdk.qbraid.com/pyqasm/api/pyqasm.html>


.. toctree::
   :maxdepth: 1
   :caption: ALGOS API Reference
   :hidden:

   api/qbraid_algorithms