from qbraid import QbraidProvider
from collections import Counter

"""
Bernstein-Vazirani Algorithm Implementation for String '1001'
"""
# Configure QBraid provider
provider = QbraidProvider(api_key="6c009jivcyw",)
device = provider.get_device('qbraid_qir_simulator')
shots = 10

with open("bernstein_vazirani.qasm", "r") as f:
    qasm = f.read()

job = device.run(qasm, shots=shots)
result = job.result()
data = result.data

# Get counts - note that rightmost qubit is the ancilla qubit
counts = data.get_counts()

print("Counts (rightmost qubit is ancilla):", counts)