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
      Build hybrid quantum-classical algorithms with qBraid.
   </p>
   </body>
   </html>

|

:Release: |release|

Overview
---------

Python package for building, simulating, and benchmarking hybrid quantum-classical algorithms.


Installation
-------------

qbraid-algorithms requires Python 3.11 or greater, and can be installed with pip as follows:

.. code-block:: bash

   pip install qbraid-algorithms


Install from Source
^^^^^^^^^^^^^^^^^^^^

You can also install from source by cloning this repository and running a pip install command in the root directory of the repository:

.. code-block:: bash

   git clone https://github.com/qBraid/qbraid-algorithms.git
   cd qbraid-algorithms
   pip3 install .


Resources
----------

- `User Guide <https://docs.qbraid.com/sdk/user-guide>`_
- `Example Notebooks <https://github.com/qBraid/qbraid-lab-demo>`_
- `API Reference <https://qbraid.github.io/qBraid/api/qbraid_algorithms.html>`_
- `Source Code <https://github.com/qBraid/qbraid-algorithms>`_

.. toctree::
   :maxdepth: 1
   :caption: SDK API Reference
   :hidden:

   qbraid <https://qbraid.github.io/qBraid/api/qbraid.html>
   qbraid.programs <https://qbraid.github.io/qBraid/api/qbraid.programs.html>
   qbraid.interface <https://qbraid.github.io/qBraid/api/qbraid.interface.html>
   qbraid.transpiler <https://qbraid.github.io/qBraid/api/qbraid.transpiler.html>
   qbraid.passes <https://qbraid.github.io/qBraid/api/qbraid.passes.html>
   qbraid.runtime <https://qbraid.github.io/qBraid/api/qbraid.runtime.html>
   qbraid.visualization <https://qbraid.github.io/qBraid/api/qbraid.visualization.html>

.. toctree::
   :caption: QIR API Reference
   :hidden:

   qbraid_qir <https://qbraid.github.io/qbraid-qir/api/qbraid_qir.html>
   qbraid_qir.cirq <https://qbraid.github.io/qbraid-qir/api/qbraid_qir.cirq.html>
   qbraid_qir.qasm3 <https://qbraid.github.io/qbraid-qir/api/qbraid_qir.qasm3.html>

.. toctree::
   :caption: CORE API Reference
   :hidden:

   qbraid_core <https://qbraid.github.io/qbraid-core/api/qbraid_core.html>
   qbraid_core.services <https://qbraid.github.io/qbraid-core/api/qbraid_core.services.html>

.. toctree::
   :caption: PYQASM API Reference
   :hidden:

   pyqasm <https://qbraid.github.io/pyqasm/api/pyqasm.html>


.. toctree::
   :maxdepth: 1
   :caption: ALGOS API Reference
   :hidden:

   api/qbraid_algorithms