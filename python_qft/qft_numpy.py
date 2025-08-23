import numpy as np

def matrix(n_qubits):
    """
    The Quantum Fourier Transform matrix for n_qubits.
    
    The QFT matrix element (j,k) is:
    (1/sqrt(2^n)) * exp(2πi * j * k / 2^n)
    
    Args:
        n_qubits: Number of qubits
        
    Returns:
        Complex matrix of shape (2^n_qubits, 2^n_qubits)
    """
    N = 2 ** n_qubits  # Matrix dimension
    
    # Create indices for all combinations
    j, k = np.meshgrid(range(N), range(N), indexing='ij')
    
    # Calculate the QFT matrix elements
    # Formula: (1/sqrt(N)) * exp(2πi * j * k / N)
    omega = np.exp(2j * np.pi / N)  # Primitive Nth root of unity
    qft = (1 / np.sqrt(N)) * (omega ** (j * k))
    
    return qft

def apply(state_vector):
    """
    Apply QFT to a quantum state vector.
    
    Args:
        state_vector: Complex array of length 2^n representing quantum state
        
    Returns:
        QFT-transformed state vector
    """
    n_qubits = int(np.log2(len(state_vector)))
    if len(state_vector) != 2**n_qubits:
        raise ValueError("State vector length must be a power of 2")
    
    qft_mat = matrix(n_qubits)
    return qft_mat @ state_vector

def inverse_qft_matrix(n_qubits):
    """
    Generate the inverse QFT matrix (conjugate transpose of QFT).
    """
    return matrix(n_qubits).conj().T

def apply_inverse_qft(state_vector):
    """Inverse QFT to a quantum state vector."""
    n_qubits = int(np.log2(len(state_vector)))
    if len(state_vector) != 2**n_qubits:
        raise ValueError("State vector length must be a power of 2")
    
    iqft_mat = inverse_qft_matrix(n_qubits)
    return iqft_mat @ state_vector


if __name__ == "__main__":

    n = int(input("Enter the number of Qubits: "))
    print(f"QFT matrix for {n} qubits:")
    qft_n= matrix(n)
    print(qft_n)
    print()
    
    identity = qft_n.conj().T @ qft_n
    print("Verification that QFT is unitary (should be close to identity):")
    print(np.abs(identity))
    print()
    
    input_state = np.array([0, 1, 0, 0], dtype=complex)
    print("Input state |01⟩:", input_state)
    

    qft_state = apply(input_state)
    print("After QFT:", qft_state)
    
    # Apply inverse QFT 
    recovered_state = apply_inverse_qft(qft_state)
    print("After inverse QFT:", recovered_state)
    print("Recovery error:", np.linalg.norm(recovered_state - input_state))
    
    # Mathematical Implementation
    print("\nMathematical formula:")
    print("QFT|j⟩ = (1/√N) ∑ₖ exp(2πijk/N)|k⟩")
    print("where N = 2^n_qubits")
    print("Matrix element (j,k) = (1/√N) * exp(2πijk/N)")