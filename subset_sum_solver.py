import sqlite3
import random
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class CoreEngine:
    def __init__(self, db_name="storage_v2.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA synchronous=OFF;")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS data_points 
                               (s_val INTEGER PRIMARY KEY, n_val INTEGER)''')
        self.conn.commit()

    def run_solve(self, numbers: list[int], target: int):
        """
        Solves the Subset Sum problem with enhanced pruning and progress metrics.
        """
        self.cursor.execute("DELETE FROM data_points")
        self.cursor.execute("INSERT INTO data_points VALUES (?, ?)", (0, 0))
        self.conn.commit()

        logger.info(f"Execution started. Target: {target}")

        has_negatives = any(n < 0 for n in numbers)
        if not has_negatives:
            numbers.sort()
            logger.info("Dataset is strictly positive. Optimized pruning enabled.")

        for i, num in enumerate(numbers):
            self.cursor.execute("SELECT s_val FROM data_points")

            batch = []
            self.cursor.execute("BEGIN TRANSACTION")

            for (s_val,) in self.cursor:
                new_s = s_val + num

                if not has_negatives and new_s > target:
                    continue

                if new_s == target:
                    self.cursor.execute("INSERT OR REPLACE INTO data_points VALUES (?, ?)", (new_s, num))
                    self.conn.commit()
                    return self.get_path(target)

                batch.append((new_s, num))

            self.cursor.executemany("INSERT OR IGNORE INTO data_points VALUES (?, ?)", batch)
            self.conn.commit()

            if i % 5 == 0:
                self.cursor.execute("SELECT COUNT(*) FROM data_points")
                total_sums = self.cursor.fetchone()[0]
                logger.info(f"Step {i}/{len(numbers)} | Current unique sums: {total_sums}")

        return None

    def get_path(self, target: int) -> list[int]:
        path = []
        curr = target
        while curr != 0:
            self.cursor.execute("SELECT n_val FROM data_points WHERE s_val=?", (curr,))
            res = self.cursor.fetchone()
            if not res or res[0] == 0:
                break
            val = res[0]
            path.append(val)
            curr -= val
        return path

def execute_task():
    engine = CoreEngine()

    sample_size = 50
    data_set = [random.randint(-100, 500) for _ in range(sample_size)]

    goal = sum(random.sample(data_set, 5))

    start_time = time.time()
    result = engine.run_solve(data_set, goal)

    if result:
        duration = time.time() - start_time
        print(f"\n[!] SOLUTION FOUND in {duration:.2f} seconds.")
        print(f"Target: {goal} | Result Sum: {sum(result)}")
        print(f"Subset: {result}")
    else:
        print("\n[-] No solution found.")

if __name__ == "__main__":
    execute_task()