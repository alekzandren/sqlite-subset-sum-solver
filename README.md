#  Advanced SQLite Subset Sum Solver (MITM Optimized)
An academically rigorous Python implementation designed to solve the **Subset Sum Problem** using a hybrid approach: **Meet-in-the-Middle (MITM)** algorithm combined with **SQLite-backed state persistence**.
By leveraging the **Horowitz-Sahni** strategy, this solver reduces computational complexity from $O(2^n)$ to $O(2^{n/2} \cdot \log 2^{n/2})$, allowing for the processing of significantly larger datasets that would traditionally exhaust system memory.

---

## Algorithmic Approach
1. Meet-in-the-Middle (MITM)
The solver partitions the dataset $S$ into $S_1, S_2$ of size $n/2$. This reduces the search space from $O(2^n)$ to $O(2^{n/2})$.
- **Theoretical Complexity:** $O(2^{n/2} \cdot \log 2^{n/2})$
- **Practical Constraint:** Performance is primarily bound by I/O throughput during the B-Tree indexing phase of the $S_1$ sub-sums.
2. FPTAS (Approximation)
For large-scale instances where an exact solution is computationally prohibitive, the engine implements a **Fully Polynomial-Time Approximation Scheme.**
- **Trimming Logic:** Using a trimming parameter $\delta = \epsilon / 2n$, the solver collapses the state space by merging sub-sums within a $(1+\delta)$ proximity.
- **Guarantee:** Returns a sum $V$ such that $(1-\epsilon) \cdot \text{Target} \leq V \leq \text{Target}$.
3. Hybrid Storage Strategy
- **In-Memory Mode (:memory:):** Default mode for $N \leq 45$, utilizing SQLite's internal speed while maintaining a relational interface.
- **Out-of-Core Mode (Disk):** Designed for extreme $N$ or RAM-constrained environments, offloading the $S_1$ hash table to disk.


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
The engine can be integrated into larger cybersecurity or cryptographic tools. To run the demonstration benchmark:
```bash
python subset_sum_solver.py
```

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

## Rigorous Testing
The project maintains high reliability through a comprehensive suite, covering:pytest
- **MITM Intersection:** Validating correct matching between the disk-stored and memory-stored halves.
- **Negative Integer Support:** Handling sets with mixed polarity.
- **Edge Cases:** Empty sets, target zero, and unreachable targets.
- **Performance Benchmarks:** Asserting logarithmic time complexity gains.
Run the test suite:
```bash
pytest tests/
```

---

## Project Structure
- subset_sum_solver.py: Core algorithmic logic and SQLite orchestration.
- tests/: Automated verification suite.
- requirements.txt: Minimal dependencies (standard library focused).
- storage_v3.db: Indexed relational storage (auto-generated).

---

## License & Disclaimer
This project is licensed under the MIT License. It is intended for educational and research purposes in the fields of **Computational Complexity** and **Information Security.**
