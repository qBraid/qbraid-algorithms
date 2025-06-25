from qbraid import QbraidProvider
from collections import Counter
import pyqasm

"""
Bernstein-Vazirani Algorithm Implementation for String '1001'
"""
# Configure QBraid provider
provider = QbraidProvider(api_key="YOUR_API_KEY",)
device = provider.get_device('qbraid_qir_simulator')
shots = 10

module = pyqasm.load("bernstein_vazirani.qasm")
ir = str(module)

job = device.run(ir, shots=shots)
result = job.result()
data = result.data

# Get counts - note that rightmost qubit is the ancilla qubit
counts = data.get_counts()

print("Counts (rightmost qubit is ancilla):", counts)