from __future__ import annotations
import numpy as np
from qiskit_aer import Aer
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector


def circuit(n_qubits: int, *, without_reverse: bool = False) -> QuantumCircuit:
    qc = QuantumCircuit(n_qubits)
    for i in range(n_qubits):
        qc.h(i)
        for j in range(i + 1, n_qubits):
            qc.cp(np.pi / 2 ** (j - i), j, i)
    if not without_reverse:
        for k in range(n_qubits // 2):
            qc.swap(k, n_qubits - 1 - k)
    return qc


def inverse_circuit(n_qubits: int, *, without_reverse: bool = False) -> QuantumCircuit:
    return circuit(n_qubits, without_reverse=without_reverse).inverse()


def unitary(n_qubits: int, *, without_reverse: bool = False) -> np.ndarray:
    qc = circuit(n_qubits, without_reverse=without_reverse)
    return Statevector.from_instruction(qc).to_operator().data


def inverse_unitary(n_qubits: int, *, without_reverse: bool = False) -> np.ndarray:
    qc = inverse_circuit(n_qubits, without_reverse=without_reverse)
    return Statevector.from_instruction(qc).to_operator().data


def apply_statevector(
    state_vector: np.ndarray, *, without_reverse: bool = False
) -> np.ndarray:
    state_vector = np.asarray(state_vector, dtype=complex)
    dim = state_vector.shape[0]
    n_qubits = int(np.round(np.log2(dim)))
    if 2 ** n_qubits != dim:
        raise ValueError("State vector length must be a power of 2")
    qc = QuantumCircuit(n_qubits)
    qc.initialize(state_vector, range(n_qubits))
    qc.append(circuit(n_qubits, without_reverse=without_reverse), range(n_qubits))
    backend = Aer.get_backend("statevector_simulator")
    job = backend.run(transpile(qc, backend))
    result = job.result()
    return np.asarray(result.get_statevector(qc), dtype=complex)


if __name__ == "__main__":
    n = int(input("Enter number of qubits: "))
    qc = circuit(n)
    print("\nQFT Circuit:")
    print(qc)

    state = np.zeros(2**n, dtype=complex)
    state[1] = 1.0

    print(f"\nInput statevector |1>: {state}")
    result = apply_statevector(state)
    print(f"\nState after QFT: {result}")
