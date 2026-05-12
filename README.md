# Optimized Meet-in-the-Middle Subset Sum Solver
An academic-grade Python implementation of the Subset Sum Problem (SSP), transitioning from brute-force $O(2^n)$ to an optimized Meet-in-the-Middle (MITM) architecture. This solver is designed for high-precision computational research, ensuring $O(2^{n/2} \cdot \log 2^{n/2})$ complexity while maintaining absolute numerical integrity.

---

##  Theoretical Framework & Methodology
The solver addresses the NP-complete nature of the Subset Sum Problem by focusing on algorithmic efficiency and state-space management.

1. Algorithmic Complexity
- **Time Complexity:** The engine achieves $O(2^{n/2} \cdot \log 2^{n/2})$ through a dual-phase execution:
- **Generation:** Sub-sum spaces for two partitions are generated in $O(2^{n/2})$.
- **Intersection:** Lookups are optimized using Hash Maps for $O(1)$ average-case access and the bisect module for $O(\log N)$ binary search across sorted state spaces.
- **Space Complexity:** $O(2^{n/2})$ to store the primary state space.

2. Numerical Integrity
- **Arbitrary-Precision Arithmetic:** Unlike standard floating-point implementations susceptible to IEEE 754 bit-drift, this solver utilizes Python’s native arbitrary-precision integers. This ensures 100% accuracy for cryptographic-scale integers ($> 2^{256}$).
- **Rational Scaling:** For fractional datasets, the framework is designed to utilize fractions.Fraction or integer scaling to maintain absolute precision without the overhead of decimal context where it's not mathematically required.

---

## Core Features
**Hybrid Search Engine**
The solver bridges the gap between raw speed and memory management:
- **In-Memory MITM:** Optimized for $N \approx 30-45$ using Python’s highly optimized dictionary lookups.
- **Persistence Layer (Optional):** A diagnostic SQLite interface is available for Out-of-Core processing, allowing state-space tracking and atomic recovery (Checkpointing) for long-running research tasks on memory-constrained hardware.

**Approximation (FPTAS)**
For instances where $N > 60$, the engine implements a Fully Polynomial-Time Approximation Scheme:
- **Trimming Logic:** Reduces the state space by merging sums within a relative proximity factor $\delta = \epsilon / 2n$.
- **Quantifiable Error:** Guarantees a solution $V$ such that $(1-\epsilon) \cdot \text{Target} \leq V \leq \text{Target}$.

---

## Installation & Developer Setup
This project follows professional Python standards with strict separation of concerns.
```bash
git clone https://github.com/alekzandren/subset-sum-solver.git
cd subset-sum-solver
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

**Development Dependencies:**
For linting, type checking, and testing, install the development suite:
```bash
pip install -r requirements-dev.txt
```

---

## Validation & Benchmarking
The solver includes a rigorous test suite focusing on boundary conditions and computational limits:
- **Massive Magnitude Tests:** Validation of sets with values exceeding $10^{30}$.
- **Zero-Sum & Negative Constraints:** Handling edge cases in discrete optimization.
- **Complexity Benchmarks:** Automated scripts to verify the $O(2^{n/2})$ growth curve.
```bash
# Run the test suite
pytest tests/

# Run static type checking
mypy subset_sum_solver.py
```

---

## Project Structure
- subset_sum_solver.py: Core logic featuring type-hinted MITM and FPTAS implementations.
- test_core.py: Performance analysis scripts for complexity verification.
- requirements.txt: Zero external dependencies for the core solver.
- requirements-dev.txt: Suite for pytest, mypy, and black.


## License & Research Disclaimer
This project is licensed under the MIT License. It is designed as a reference implementation for **Computational Complexity** research. While optimized for Python, extreme-scale instances may require migration to low-level implementations (C++/Rust) using the same MITM principles provided here.
