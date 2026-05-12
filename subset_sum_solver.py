import sqlite3
import random
import time
import logging
from typing import List, Optional, Dict

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class CoreEngine:
    def __init__(self, db_name=":memory:"):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA synchronous=OFF;")
        self.cursor = self.conn.cursor()
        self._setup_db()

    def _setup_db(self):
        self.cursor.execute("DROP TABLE IF EXISTS left_sums")
        self.cursor.execute('''CREATE TABLE left_sums 
                               (s_val REAL PRIMARY KEY, n_val REAL)''')
        self.conn.commit()

    def _trim(self, sums: Dict[float, float], delta: float) -> Dict[float, float]:
        """
        Real FPTAS trimming logic.
        Reduces the number of sums by merging those that are close to each other.
        """
        sorted_keys = sorted(sums.keys())
        if not sorted_keys: return {0: 0}

        trimmed = {0: 0}
        last_kept = sorted_keys[0]
        for s in sorted_keys:
            if s > last_kept * (1 + delta):
                trimmed[s] = sums[s]
                last_kept = s
        return trimmed

    def run_solve(self, numbers: List[int], target: int, epsilon: float = 0.0):
        """
        MITM Solver with optional FPTAS trimming.
        """
        n = len(numbers)
        mid = n // 2
        left_part = numbers[:mid]
        right_part = numbers[mid:]

        delta = epsilon / (2 * n) if epsilon > 0 else 0

        logger.info(f"Solving with MITM. Epsilon: {epsilon} (Delta: {delta})")

        left_sums = {0: 0}
        for num in left_part:
            new_sums = {s + num: num for s in left_sums}
            left_sums.update(new_sums)
            if delta > 0:
                left_sums = self._trim(left_sums, delta)

        self.cursor.execute("BEGIN TRANSACTION")
        self.cursor.executemany("INSERT OR IGNORE INTO left_sums VALUES (?, ?)",
                                list(left_sums.items()))
        self.conn.commit()

        right_sums = {0: 0}
        for num in right_part:
            new_right = {}
            for rs in right_sums:
                curr_rs = rs + num

                if epsilon == 0:
                    self.cursor.execute("SELECT n_val FROM left_sums WHERE s_val = ?", (target - curr_rs,))
                else:
                    # Range search for FPTAS
                    lower = (target - curr_rs) / (1 + epsilon)
                    upper = (target - curr_rs)
                    self.cursor.execute("SELECT s_val, n_val FROM left_sums WHERE s_val BETWEEN ? AND ?",
                                        (lower, upper))

                match = self.cursor.fetchone()
                if match:
                    # Match found
                    matched_s = match[0] if epsilon > 0 else (target - curr_rs)
                    path_left = self._get_db_path(matched_s)
                    path_right = self._reconstruct_mem_path(right_sums, rs) + [num]
                    return path_left + path_right

                new_right[curr_rs] = num
            right_sums.update(new_right)
            if delta > 0:
                right_sums = self._trim(right_sums, delta)

        return None

    def _get_db_path(self, target: float) -> List[float]:
        path = []
        curr = target
        while curr > 1e-9:
            self.cursor.execute("SELECT n_val FROM left_sums WHERE s_val=?", (curr,))
            res = self.cursor.fetchone()
            if not res: break
            val = res[0]
            path.append(val)
            curr -= val
        return path

    def _reconstruct_mem_path(self, sums_dict: dict, end_val: float) -> List[float]:
        path = []
        curr = end_val
        while curr > 1e-9:
            val = sums_dict.get(curr)
            if val is None or val == 0: break
            path.append(val)
            curr -= val
        return path
