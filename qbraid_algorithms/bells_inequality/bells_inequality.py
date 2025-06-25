from qbraid import transpile, QbraidProvider
from collections import Counter

# Configure QBraid provider
provider = QbraidProvider(api_key="YOUR_API_KEY_HERE",)
device = provider.get_device('qbraid_qir_simulator')
shots = 10

with open("bells_inequality.qasm", "r") as f:
    qasm = f.read()

job = device.run(qasm, shots=shots)
result = job.result()
data = result.data
# Note: Results for each of the 3 circuits are returned as single string
counts = data.get_counts()
probs = data.get_probabilities()


def process_results(results):
    """
    Parses the counts or probabilities of each circuit 
    """
    ab = Counter()
    ac = Counter()
    bc = Counter()

    for bitstring, freq in results.items():
        ab_val = bitstring[0:2]
        ac_val = bitstring[2:4]
        bc_val = bitstring[4:6]

        ab[ab_val] += freq
        ac[ac_val] += freq
        bc[bc_val] += freq
    
    return dict(ab), dict(ac), dict(bc)
    
ab_counts, ac_counts, bc_counts = process_results(counts)
ac_probs, bc_probs, ab_probs = process_results(probs)

print("Circuit 1 (AB) Counts:", ab_counts)
print("Circuit 2 (AC) Counts:", ac_counts)
print("Circuit 3 (BC) Counts:", bc_counts)