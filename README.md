# Quantum Fourier Transform (QFT) 

This project demonstrates the **Quantum Fourier Transform (QFT)** using four different approaches, providing a comprehensive comparison of quantum computing paradigms from high-level frameworks to low-level implementations:

- **Cirq** - Google's quantum framework for circuit-based quantum computing
- **Qiskit** - IBM's quantum framework with real hardware access  
- **NumPy** - Classical matrix simulation showing the mathematical foundation
- **C** - Low-level implementation for performance and educational insights

The QFT is a fundamental quantum algorithm used in Shor's algorithm, quantum phase estimation, and various quantum signal processing applications.

---

## Quick Start

**Clone :**
```bash
git clone https://github.com/n0sync/Quantum-Fourier-Transform
```

**Python implementations:**
```bash
pip install -r requirements.txt
python cirq_qft/qft_cirq.py      # Google Cirq implementation
python qiskit_qft/qft_qiskit.py  # IBM Qiskit implementation  
python numpy_qft/qft_numpy.py   # NumPy matrix implementation
```

**C implementation:**
```bash
cd c_qft
gcc qft.c -o qft -lm
./qft
```

**Example output:**
```
Enter number of qubits: 3
Initial state: |000⟩
After QFT: 0.354|000⟩ + 0.354|001⟩ + ... + 0.354|111⟩
```

---

## Implementation Details

**Cirq** - Uses quantum gates (H, CZ) to build QFT circuits with Google's clean API. Best for learning quantum circuit design and rapid prototyping.

**Qiskit** - Industry-standard framework with extensive tooling, visualization, and access to IBM's real quantum computers. Ideal for production quantum applications.

**NumPy** - Constructs the QFT transformation matrix explicitly using classical linear algebra. Perfect for understanding the mathematical theory behind QFT.

**C** - Manual implementation using complex number arithmetic and direct state vector manipulation. Demonstrates low-level quantum state operations and optimal performance.

---

## Mathematical Foundation

The QFT transforms a quantum state |x⟩ using the formula:

`QFT|x⟩ = (1/√2ⁿ) Σ(y=0 to 2ⁿ-1) e^(2πixy/2ⁿ)|y⟩`

Where `n` is the number of qubits, and the transformation maps computational basis states to their quantum Fourier coefficients. This creates superposition states that encode frequency information, enabling quantum algorithms to process periodic functions exponentially faster than classical methods.

Each implementation demonstrates this transformation using different computational approaches - from high-level quantum circuit abstractions to direct matrix operations and low-level state vector manipulations.
