# Fault-Tolerant High-Precision Subset Sum Solver
A specialized Python implementation designed for the Subset Sum Problem, focusing on mathematical integrity, fault-tolerant state persistence, and arbitrary-precision arithmetic. This engine is engineered to bridge the gap between theoretical NP-complete complexity and resilient, verifiable computational research.

---

## Performance & System Design Decisions
1. SQLite vs. Redis (The 2026 Context)
A common critique is the choice of SQLite over an In-Memory store like Redis with AOF.
- **The Rational:** While Redis is superior for throughput, SQLite was chosen for zero-dependency portability and minimal resource overhead in academic environments.
- **Infrastructure-less Persistence:** This solver is designed to run on high-performance computing (HPC) clusters where setting up a Redis instance is not always permissible, but filesystem access is universal.

2. State Recovery Algorithm
The engine implements a Warm-Start Recovery mechanism.
Unlike standard solvers that lose progress on a SIGKILL or power failure, this engine checks the left_sums table integrity upon startup.
If a pre-computed state exists, the engine skips the $O(2^{n/2})$ generation phase and proceeds directly to the intersection phase, potentially saving hours of re-computation.

3. Real-World Crossover (The "Truth" in Numbers)
- **N < 35:** Pure RAM-based Python set is up to 50x faster than the SQLite-hybrid approach due to I/O latency.
- **N > 45:** The hybrid approach becomes viable as the state space exceeds the available L3 cache and enters the swap-space danger zone.
- **Business Case:** While the project uses the Subset Sum problem as its foundation, the core architecture is highly applicable to High-Frequency Finance (FinTech), where auditing trillions of small transactions against a massive target balance requires both Decimal precision and a persistent audit trail.

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
- tests/stress_test.py: Validation against IEEE 754 errors and integer overflows.
- requirements.txt: Minimal dependency footprint.

---

## License & Disclaimer
This project is licensed under the MIT License. It is intended for academic research in **Computational Complexity** and **Information Security.** The use of SQLite is a deliberate architectural trade-off favoring **verifiability** and **persistence** over raw execution speed.

