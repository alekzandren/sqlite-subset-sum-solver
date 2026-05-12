# Fault-Tolerant High-Precision Subset Sum Solver

A specialized Python implementation designed for the Subset Sum Problem, focusing on mathematical integrity, fault-tolerant state persistence, and arbitrary-precision arithmetic. This engine is engineered to bridge the gap between theoretical NP-complete complexity and resilient, verifiable computational research.

---

## Engineering Design & Philosophy
Unlike standard RAM-resident solvers, this engine utilizes a hybrid relational-state architecture to address the limitations of volatile memory and standard hardware types.

1. Persistent State Machine (The SQLite Choice)
For $N > 45$, Subset Sum computations can reach several hours of execution time.
- **Checkpointing & Fault Tolerance:** By offloading the $S_1$ sub-sum generation to an indexed SQLite engine, the solver acts as a Persistent State Machine. This prevents total data loss in the event of process termination or memory exhaustion—a critical requirement for long-running research tasks.
- **Relational Indexing:** Utilizing B-Tree indexing, the engine performs complement lookups at $O(\log N)$ scale, allowing the disk-resident sub-sums to be queried with high efficiency.

2. Numerical Robustness (Beyond IEEE 754)
To ensure absolute reliability in cryptographic or astronomical datasets:
- **Arbitrary Precision:** Leveraging the module with 50-digit precision, the engine eliminates bit-drift and rounding errors inherent in standard floating-point arithmetic.decimal
- **String-Relational Mapping:** Numeric values are stored in the database as objects. This bypasses the INT64 (8-byte) limit, enabling the processing of values far exceeding TEXT$2^{63}-1$ (e.g., $2^{256}$ and beyond).

---

## Algorithmic Stack
- **Meet-in-the-Middle (MITM) Optimization**
The solver partitions the dataset into two subsets of size $N/2$, reducing computational complexity from $O(2^n)$ to $O(2^{n/2} \cdot \log 2^{n/2})$. This is the theoretical limit for exact subset sum solving without specialized hardware.
- **FPTAS (Approximation Scheme)**
For extreme-scale instances where exact solutions are computationally prohibitive, a Fully Polynomial-Time Approximation Scheme is implemented.
- **Trimming Logic:** The engine merges sub-sums within a relative proximity determined by a trimming factor $\delta = \epsilon / 2n$.
- **Quantifiable Error:** High-precision arithmetic allows for meta-analysis of the "Trimming Error," providing a verifiable guarantee that the result Decimal$V$ satisfies $(1-\epsilon) \cdot \text{Target} \leq V \leq \text{Target}$.

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

# Use ":memory:" for high-speed computation 
# Use a file path (e.g., "data.db") for persistent checkpointing
engine = CoreEngine(db_name="research_checkpoint.db")

# Example: Massive integer solving
numbers = [10**25, 10**25 + 5, 12, 18]
target = 2 * (10**25) + 35

# Set epsilon=0 for exact solving, epsilon > 0 for FPTAS
result = engine.run_solve(numbers, target, epsilon=0.0001)
print(f"Verified Subset: {result}")
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
The engine is validated against a "Boundary Analysis" suite:
- **Precision Torture:** Solving targets composed of magnitudes spanning $10^{18}$ and $10^{-9}$ simultaneously.
- **Integer Overflow:** Validating consistency for values exceeding $2^{128}$ to ensure the mapping is robust.TEXT
- **Complexity Benchmarking:** Executing $N=60$ datasets using FPTAS to demonstrate polynomial-time behavior under approximation.

```bash
pytest tests/
```

---

## Structure
- subset_sum_solver.py: Core logic featuring arithmetic and algorithms.Decimal_trim
- tests/test_core.py: Validation against IEEE 754 errors and integer overflows.
- requirements.txt: Minimal dependency footprint.

---

## License & Disclaimer
This project is licensed under the MIT License. It is intended for academic research in **Computational Complexity** and **Information Security.** The use of SQLite is a deliberate architectural trade-off favoring **verifiability** and **persistence** over raw execution speed.

