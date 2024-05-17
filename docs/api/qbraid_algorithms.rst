qbraid_algorithms
===================

.. automodule:: qbraid_algorithms
   :members:
   :undoc-members:
   :show-inheritance:


Reservoir Computing
--------------------

Reservoir computing algorithms are a subset of recurrent neural networks (RNNs) that utilize
a fixed, randomly connected network known as the 'reservoir' to process temporal data. Unlike
traditional RNNs, reservoir computing models uniquely train only the output weights of the network.
This characteristic makes them particularly efficient as dynamic feature extractors for time series data.

.. autosummary::
   :toctree: ../stubs/

   esn
   qrc
   datasets