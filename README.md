# SQLite Subset Sum Solver

A high-performance Python tool designed to solve the **Subset Sum Problem** using **SQLite** for state persistence. This approach allows processing larger datasets by offloading the search space to a disk-based database, bypassing typical RAM limitations.

---

## Features
- **Persistence:** Uses SQLite with WAL (Write-Ahead Logging) for optimized I/O operations.
- **Pruning:** Includes optimized pruning for strictly positive datasets.
- **Type Safety:** Fully annotated with Python 3.12+ type hints.
- **Logging:** Professional execution tracking using the `logging` module.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/alekzandren/sqlite-subset-sum-solver.git](https://github.com/alekzandren/sqlite-subset-sum-solver.git)
   cd sqlite-subset-sum-solver
2. **Install dependencies:**
```bash
            pip install -r requirements.txt
```

---

## Usage
Run the main execution script to see the solver in action:
```bash
           python subset_sum_solver.py
```

---

## Testing
The project includes a suite of unit tests to ensure algorithm reliability and edge-case handling.
Run tests using :pytest
```bash
          pytest tests/
```

---

## Project Structure
- subset_sum_solver.py: The main solver logic and database orchestration.
- tests/: Unit tests for validating different sum scenarios.
- requirements.txt: Project dependencies.
- storage_v2.db: Local SQLite database (auto-generated).

---

## License
MIT
