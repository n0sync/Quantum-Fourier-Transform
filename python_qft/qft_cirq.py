from __future__ import annotations
from typing import Sequence, Optional

import cirq
import numpy as np


def circuit(qubits: Sequence[cirq.Qid], *, without_reverse: bool = False) -> cirq.Circuit:
    n = len(qubits)
    c = cirq.Circuit()

    for i in range(n):
        c.append(cirq.H(qubits[i]))
        for j in range(i + 1, n):
            alpha = 1.0 / (2 ** (j - i))
            c.append(cirq.CZ(qubits[j], qubits[i]) ** alpha)

    if not without_reverse:
        for k in range(n // 2):
            c.append(cirq.SWAP(qubits[k], qubits[n - 1 - k]))

    return c


def inverse_circuit(qubits: Sequence[cirq.Qid], *, without_reverse: bool = False) -> cirq.Circuit:
    return cirq.inverse(circuit(qubits, without_reverse=without_reverse), default=None)


def unitary(n_qubits: int, *, without_reverse: bool = False) -> np.ndarray:
    qs = cirq.LineQubit.range(n_qubits)
    U = cirq.unitary(circuit(qs, without_reverse=without_reverse))
    return np.asarray(U, dtype=complex)


def inverse_unitary(n_qubits: int, *, without_reverse: bool = False) -> np.ndarray:
    qs = cirq.LineQubit.range(n_qubits)
    U = cirq.unitary(inverse_circuit(qs, without_reverse=without_reverse))
    return np.asarray(U, dtype=complex)


def apply_statevector(
    state_vector: np.ndarray,
    *,
    without_reverse: bool = False,
    qubits: Optional[Sequence[cirq.Qid]] = None,
) -> np.ndarray:
    state_vector = np.asarray(state_vector, dtype=complex)
    dim = state_vector.shape[0]
    n_qubits = int(np.round(np.log2(dim)))

    if 2 ** n_qubits != dim:
        raise ValueError("State vector length must be a power of 2.")

    if qubits is None:
        qubits = cirq.LineQubit.range(n_qubits)

    sim = cirq.Simulator()
    c = circuit(qubits, without_reverse=without_reverse)
    result = sim.simulate(c, initial_state=state_vector)
    return np.asarray(result.final_state_vector, dtype=complex)


def apply_inverse_statevector(
    state_vector: np.ndarray,
    *,
    without_reverse: bool = False,
    qubits: Optional[Sequence[cirq.Qid]] = None,
) -> np.ndarray:
    state_vector = np.asarray(state_vector, dtype=complex)
    dim = state_vector.shape[0]
    n_qubits = int(np.round(np.log2(dim)))

    if 2 ** n_qubits != dim:
        raise ValueError("State vector length must be a power of 2.")

    if qubits is None:
        qubits = cirq.LineQubit.range(n_qubits)

    sim = cirq.Simulator()
    c = inverse_circuit(qubits, without_reverse=without_reverse)
    result = sim.simulate(c, initial_state=state_vector)
    return np.asarray(result.final_state_vector, dtype=complex)


if __name__ == "__main__":
    n = int(input("Enter number of qubits: "))
    qs = cirq.LineQubit.range(n)

    print("QFT circuit:")
    print(circuit(qs))

    U = unitary(n)
    print("\nQFT unitary:")
    print(U)

    identity = U.conj().T @ U
    print("\nCheck unitarity (should be close to identity):")
    print(np.abs(identity))

    input_state = np.array([0, 1, 0, 0], dtype=complex)
    print("\nInput state |01⟩:", input_state)

    qft_state = apply_statevector(input_state)
    print("After QFT:", qft_state)

    recovered_state = apply_inverse_statevector(qft_state)
    print("After inverse QFT:", recovered_state)
    print("Recovery error:", np.linalg.norm(recovered_state - input_state))
