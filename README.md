# High-Precision SQLite Subset Sum Solver (FPTAS & MITM)
An academically focused Python implementation designed to tackle the Subset Sum Problem with a focus on mathematical robustness, infinite precision, and algorithmic efficiency. This solver bridges the gap between theoretical NP-complete challenges and practical, high-scale engineering.

---
## Core Technologies & Standards
- **Arbitrary Precision Arithmetic:** Utilizes the Python decimal module with **50-digit precision** to bypass the inherent "drift" and inaccuracies of **IEEE 754** floating-point calculations.
- **Infinite-Scale Storage:** Employs a unique **String-Relational Mapping** in SQLite, using TEXT fields to store numeric states. This bypasses the standard **64-bit (INT64) integer limit**, allowing for the processing of astronomical values (e.g., $> 2^{63}-1$).
- **Out-of-Core Processing:** Designed for RAM-constrained environments, offloading state spaces to an indexed SQLite engine to maintain stability during massive scale-ups.

---

## Algorithmic Innovations
1. Fully Polynomial-Time Approximation Scheme (FPTAS)
Beyond exact matching, the engine implements an approximation logic using **Trimming.**
- **Trimming Logic:** For a given error parameter $\epsilon$, the solver applies a trimming factor $\delta = \epsilon / 2n$, merging sub-sums that fall within the $(1+\delta)$ proximity.
- **Precision Guarantee:** The engine guarantees a solution $V$ such that $(1-\epsilon) \cdot \text{Target} \leq V \leq \text{Target}$.

2. Meet-in-the-Middle (MITM) Optimization
By partitioning the dataset into $N/2$ subsets, the solver achieves a radical complexity reduction:
Theoretical Complexity: $O(2^{n/2} \cdot \log 2^{n/2})$.
B-Tree Intersections: The intersection between the memory-resident second half and the disk-resident first half is performed via indexed SQL queries, ensuring $O(\log N)$ lookup performance.


---

## Installation
Clone the repository:
```bash
git clone https://github.com/alekzandren/sqlite-subset-sum-solver.git
cd sqlite-subset-sum-solver
```
Setup Environment:
```bash
# It is recommended to use a virtual environment
   python -m venv venv
   source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
```

---

## Usage
```bash
from subset_sum_solver import CoreEngine

# Defaulting to :memory: for high-speed computation
engine = CoreEngine(db_name=":memory:")

# Supports massive integers and approximation
numbers = [10**20, 10**20 + 1, 5, 10]
target = 2 * (10**20) + 16

# epsilon=0 for exact match, epsilon > 0 for FPTAS approximation
result = engine.run_solve(numbers, target, epsilon=0.001)
print(f"Verified Solution: {result}")
```

---

## Example Implementation:
```bash
from subset_sum_solver import CoreEngine

engine = CoreEngine(db_name="research_storage.db")
numbers = [12, 45, 78, 34, 56, 91, 23, 47]
target = 157

result = engine.run_solve(numbers, target)
print(f"Subset found: {result}")
```

---

## Stress Testing & Validation
The project includes a StressTests suite designed for "Precision Torture" and "Boundary Analysis":
- **Massive Scale:** Validating $N=60$ datasets where traditional brute force is mathematically impossible.
- **The "One Giant" Problem:** Handling targets composed of vastly different magnitudes (e.g., $10^{18}$ combined with $10^{-9}$) to ensure no loss of data in the low-order bits.
- **Overflow Resistance:** Verifying values exceeding $2^{128}$ to ensure database integrity.

```bash
pytest tests/
```

---

## Structure
- subset_sum_solver.py: The core engine featuring Decimal arithmetic and _trim logic.
- tests/stress_test.py: Validation against IEEE 754 errors and integer overflows.
- requirements.txt: Minimal dependencies.

---

## License & Disclaimer
This project is licensed under the MIT License. It is intended for educational and research purposes in the fields of **Computational Complexity** and **Information Security.**
