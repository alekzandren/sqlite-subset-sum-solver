# Persistent High-Precision Subset Sum Solver
A specialized research framework for the Subset Sum Problem, optimized for fault-tolerant computation and memory-constrained environments. This project bridges the gap between theoretical NP-complete complexity and resilient, verifiable engineering by utilizing a hybrid out-of-core processing model.

---

##  Engineering Philosophy & Design
Unlike standard in-memory solvers, this engine implements a "Disk-as-a-Swap" architecture, utilizing SQLite as a robust extension of the system's address space.

1. Why SQLite? (Persistence over Latency)
In MITM algorithms, the exponential growth of sub-sums often leads to a MemoryError.
- **Overcoming RAM Limits:** When the state space ($2^{n/2}$) exceeds physical memory, the engine flushes states to an indexed database. This allows the solver to complete tasks on hardware that would otherwise fail.
- **Atomic Warm-Start Recovery:** A dual-table commit strategy tracks the last_processed_idx. If the process is terminated (SIGKILL) or the system loses power, the solver resumes from the exact point of failure rather than restarting hours of computation.
- **Zero-Dependency Portability:** SQLite was chosen over Redis/NoSQL to ensure the framework runs on high-performance computing (HPC) clusters without requiring administrative service installations.

2. Numerical Robustness (Beyond IEEE 754)
- **Arbitrary Precision:** Utilizing the decimal module with 50-digit precision eliminates the bit-drift and accumulation errors inherent in standard floating-point types.
- **String-Relational Mapping:** Numeric values are stored as TEXT in the database. This bypasses the 64-bit integer limit (INT64), enabling the processing of astronomical values (e.g., $> 2^{256}$) while maintaining B-Tree searchability.

---

## Algorithmic Stack
**Meet-in-the-Middle (MITM) Optimization**
The solver partitions the dataset into two subsets, reducing computational complexity from $O(2^n)$ to $O(2^{n/2} \cdot \log 2^{n/2})$. Intersection lookups are performed via optimized SQL Range Queries (BETWEEN), leveraging disk-resident indexes for memory efficiency.

**FPTAS (Approximation Scheme)**
For extreme-scale instances ($N > 60$), a Fully Polynomial-Time Approximation Scheme is provided.
- **Trimming Logic:** The state space is compressed using a trimming factor $\delta = \epsilon / 2n$.
- **Quantifiable Error:** High-precision arithmetic allows for a verifiable guarantee that the result $V$ satisfies: $(1-\epsilon) \cdot \text{Target} \leq V \leq \text{Target}$.

---

## Benchmarking & Constraints
- **N < 35:** Pure RAM-based Python sets are significantly faster due to zero I/O overhead.
- **N > 45:** The hybrid model becomes viable as the state space begins to compete with the L3 cache and system swap.
- **The Trade-off:** This is a Reliability-First framework. It prioritizes the completion and verifiability of a task over raw execution speed in low-resource environments.


---

## Installation & Usage
```bash
git clone https://github.com/alekzandren/sqlite-subset-sum-solver.git
cd sqlite-subset-sum-solver
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

**Basic Usage:**
```bash
from subset_sum_solver import CoreEngine

# The DB file acts as a persistent checkpoint
engine = CoreEngine(db_name="research_checkpoint.db")

numbers = [10**25, 10**25 + 7, 15, 22]
target = 2 * (10**25) + 37

# epsilon=0 for exact match, epsilon > 0 for FPTAS
result = engine.run_solve(numbers, target, epsilon=0.001)
print(f"Verified Solution: {result}")
```

---

## Stress Testing
The included StressTests suite validates:
- **Precision Torture:** Handling targets spanning magnitudes of $10^{18}$ and $10^{-9}$ simultaneously.
- **Atomic Recovery:** Integrity checks after simulated process crashes.
- **Overflow Resistance:** Validation of values exceeding $2^{128}$.

```bash
pytest tests/
```

---

## Project Structure
- subset_sum_solver.py: Core engine featuring atomic checkpoints and MITM logic.
- tests/: Boundary analysis and precision validation.
- requirements.txt: Minimal dependency footprint.

---

## License & Disclaimer
This project is licensed under the MIT License. It is intended for academic research in **Computational Complexity** and **Information Security.** The use of SQLite is a deliberate architectural trade-off favoring **verifiability** and **persistence** over raw execution speed.

