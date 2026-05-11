# High-Precision Subset Sum Solver (SQLite Optimized)

A high-performance Python engine designed to solve the Subset Sum Problem using astronomical scales of data. This project demonstrates how to bypass RAM limitations by utilizing a database-backed dynamic programming approach.

## The Challenge
Standard dynamic programming solutions for the Subset Sum Problem fail when:
1. The numbers are extremely large (beyond 64-bit integers).
2. The set of possible sums exceeds the available RAM.

This solver handles 5,000 numbers with a precision of up to 10^99 each, using SQLite as a swap-space for intermediate states.

## Key Features
- Infinite Precision: Leverages Python's arbitrary-precision integers to process numbers up to 100 digits long.
- SQLite CoreEngine: Uses SQLite3 as an external memory buffer to prevent MemoryError during the state-expansion phase.
- Performance Tuning:
    - PRAGMA journal_mode=WAL for high-speed concurrent writes.
    - PRAGMA synchronous=OFF to maximize I/O throughput.
    - Large RAM cache allocation (2GB) for the database engine.
- Smart Backtracking: Implements an efficient path-reconstruction algorithm to retrieve the exact elements forming the target sum.

## Technical Specs
- Data Set: 5,000 random integers.
- Range: From $-10^{99}$ to $10^{99}$.
- Computational Limit: Capped at $10^{1000}$ for intermediate sums to maintain stability.
- Storage: storage_v1.db (auto-managed).

## Project Structure
- subset_sum_solver.py: Main engine and logic.
- my_numbers.txt: The generated dataset.
- solution.txt: Final verification and the resulting subset.
- .gitignore: Configured to keep the repository clean from DB artifacts.

## How to Run
```bash
python subset_sum_solver.pym-solver
```
