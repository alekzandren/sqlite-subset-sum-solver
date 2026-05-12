# Advanced SQLite Subset Sum Solver (MITM Optimized)
An academically rigorous Python implementation designed to solve the **Subset Sum Problem** using a hybrid approach: **Meet-in-the-Middle (MITM)** algorithm combined with **SQLite-backed state persistence**.
By leveraging the **Horowitz-Sahni** strategy, this solver reduces computational complexity from $O(2^n)$ to $O(2^{n/2} \cdot \log 2^{n/2})$, allowing for the processing of significantly larger datasets that would traditionally exhaust system memory.

---

## Key Improvements & Features
**Meet-in-the-Middle Architecture:** Partitions the dataset into two halves, generating sub-sums independently to achieve an exponential reduction in operations.
**Disk-Based Lookup Engine:** Utilizes SQLite with **B-Tree Indexing** as a high-speed search space for the $O(1)$ or $O(\log N)$ complement lookup phase.
**FPTAS Ready:** Structured to support **Fully Polynomial-Time Approximation Schemes** (Epsilon-pruning) for handling near-target solutions in extreme $N$ scenarios.
**High-Concurrency I/O:** Optimized with **WAL (Write-Ahead Logging)** and asynchronous-ready database transactions to minimize disk bottlenecks.
**Modern Python Core:** Built for **Python 3.12+** utilizing strict type hinting and advanced memory management.

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
**MITM Intersection:** Validating correct matching between the disk-stored and memory-stored halves.
**Negative Integer Support:** Handling sets with mixed polarity.
**Edge Cases:** Empty sets, target zero, and unreachable targets.
**Performance Benchmarks:** Asserting logarithmic time complexity gains.
Run the test suite:
```bash
pytest tests/
```

---

## Project Structure
subset_sum_solver.py: Core algorithmic logic and SQLite orchestration.
tests/: Automated verification suite.
requirements.txt: Minimal dependencies (standard library focused).
storage_v3.db: Indexed relational storage (auto-generated).

---

## License & Disclaimer
This project is licensed under the MIT License. It is intended for educational and research purposes in the fields of **Computational Complexity** and **Information Security.**





