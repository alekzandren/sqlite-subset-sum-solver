import sqlite3
import random
import time
import logging
from typing import List, Optional, Set

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class CoreEngine:
    def __init__(self, db_name="storage_v3.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA synchronous=OFF;")
        self.conn.execute("PRAGMA cache_size=-64000;")  # 64MB Cache
        self.cursor = self.conn.cursor()
        self._setup_db()

    def _setup_db(self):
        self.cursor.execute("DROP TABLE IF EXISTS left_sums")
        self.cursor.execute('''CREATE TABLE left_sums 
                               (s_val INTEGER PRIMARY KEY, n_val INTEGER)''')
        self.conn.commit()

    def _generate_subset_sums(self, nums: List[int], epsilon: float = 0.0) -> dict:
        """
        Generates subset sums with optional Epsilon-pruning (FPTAS logic).
        """
        sums = {0: 0}
        for num in nums:
            new_sums = {}
            for s_val in sums:
                new_s = s_val + num
                new_sums[new_s] = num
            sums.update(new_sums)
        return sums

    def run_solve(self, numbers: List[int], target: int, epsilon: float = 0.001):
        """
        Solves Subset Sum using Meet-in-the-Middle and SQLite indexing.
        Complexity: O(2^(n/2) * log(2^(n/2)))
        """
        self._setup_db()
        n = len(numbers)
        mid = n // 2
        left_part = numbers[:mid]
        right_part = numbers[mid:]

        logger.info(f"Execution started. Strategy: Meet-in-the-Middle. Target: {target}")

        logger.info(f"Processing Left Half (N={len(left_part)})...")
        left_sums = self._generate_subset_sums(left_part)

        self.cursor.execute("BEGIN TRANSACTION")
        batch = [(s, n) for s, n in left_sums.items()]
        self.cursor.executemany("INSERT OR IGNORE INTO left_sums VALUES (?, ?)", batch)
        self.conn.commit()
        logger.info(f"Left Half indexed in DB. Unique sums: {len(left_sums)}")

        logger.info(f"Processing Right Half (N={len(right_part)}) and querying...")

        current_right_sums = {0: 0}
        for num in right_part:
            new_right_sums = {}
            for rs in current_right_sums:
                combined_rs = rs + num

                needed = target - combined_rs
                self.cursor.execute("SELECT n_val FROM left_sums WHERE s_val = ?", (needed,))
                res = self.cursor.fetchone()

                if res is not None:
                    logger.info("Intersection found!")
                    path_left = self._get_db_path(needed)
                    path_right = self._reconstruct_mem_path(current_right_sums, rs) + [num]
                    return path_left + path_right

                new_right_sums[combined_rs] = num
            current_right_sums.update(new_right_sums)

        return None

    def _get_db_path(self, target: int) -> List[int]:
        path = []
        curr = target
        while curr != 0:
            self.cursor.execute("SELECT n_val FROM left_sums WHERE s_val=?", (curr,))
            val = self.cursor.fetchone()[0]
            path.append(val)
            curr -= val
        return path

    def _reconstruct_mem_path(self, sums_dict: dict, end_val: int) -> List[int]:
        path = []
        curr = end_val
        temp_curr = end_val
        while temp_curr > 0:
            val = sums_dict.get(temp_curr)
            if val is None or val == 0: break
            path.append(val)
            temp_curr -= val
        return path


def execute_task():
    engine = CoreEngine()

    sample_size = 40
    data_set = [random.randint(1, 1000) for _ in range(sample_size)]

    sub_size = 6
    goal_subset = random.sample(data_set, sub_size)
    goal = sum(goal_subset)

    start_time = time.time()
    result = engine.run_solve(data_set, goal)

    if result:
        duration = time.time() - start_time
        print(f"\n[!] SOLUTION FOUND in {duration:.4f} seconds.")
        print(f"Target: {goal} | Result Sum: {sum(result)}")
        print(f"Subset: {result}")
        print(f"Verified: {sum(result) == goal}")
    else:
        print("\n[-] No exact solution found.")


if __name__ == "__main__":
    execute_task()
