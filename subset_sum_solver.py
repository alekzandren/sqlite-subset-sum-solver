import sqlite3
import os
from typing import List, Optional

class SubsetSumSolver:
    def __init__(self, db_path: str = "subset_sum.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS left_space (
                    sum_value INTEGER PRIMARY KEY,
                    path_json TEXT
                )
            """)
            conn.commit()

    def solve_exact(self, nums: List[int], target: int) -> Optional[List[int]]:
        if not nums:
            return None if target != 0 else []

        n = len(nums)
        mid = n // 2
        left_half = nums[:mid]
        right_half = nums[mid:]

        self._generate_left_space_to_db(left_half)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for r_sum, r_path in self._yield_right_space(right_half):
                needed = target - r_sum
                
                cursor.execute("SELECT path_json FROM left_space WHERE sum_value = ?", (needed,))
                row = cursor.fetchone()
                
                if row:
                    left_path = eval(row[0])
                    return list(left_path) + list(r_path)

        return None

    def solve_fptas(self, nums: List[int], target: int, epsilon: float) -> int:
        if not nums or target <= 0:
            return 0
        valid_nums = [x for x in nums if x <= target]
        if not valid_nums:
            return 0
            
        n = len(valid_nums)
        delta = epsilon / (2 * n)
        current_sums = [0]

        for x in valid_nums:
            new_sums = [s + x for s in current_sums if s + x <= target]
            combined = sorted(current_sums + new_sums)
            current_sums = self._trim_spectrum(combined, delta)

        return max(current_sums)

    def _trim_spectrum(self, sorted_list: List[int], delta: float) -> List[int]:
        if not sorted_list: return []
        trimmed = [sorted_list[0]]
        last_added = sorted_list[0]

        for i in range(1, len(sorted_list)):
            current = sorted_list[i]
            if last_added == 0:
                if current > 0:
                    trimmed.append(current)
                    last_added = current
            elif current > last_added * (1.0 + delta):
                trimmed.append(current)
                last_added = current
        return trimmed

    def _generate_left_space_to_db(self, items: List[int]) -> None:
        sums_map = {0: ()}
        for x in items:
            new_entries = {}
            for current_sum, path in sums_map.items():
                next_sum = current_sum + x
                if next_sum not in sums_map:
                    new_entries[next_sum] = path + (x,)
            sums_map.update(new_entries)
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            prepared_data = [(s, str(p)) for s, p in sums_map.items()]
            cursor.executemany("INSERT OR IGNORE INTO left_space VALUES (?, ?)", prepared_data)
            conn.commit()

    def _yield_right_space(self, items: List[int]):
        sums_map = {0: ()}
        yield 0, ()
        for x in items:
            new_entries = {}
            for current_sum, path in sums_map.items():
                next_sum = current_sum + x
                if next_sum not in sums_map:
                    new_entries[next_sum] = path + (x,)
                    yield next_sum, new_entries[next_sum]
            sums_map.update(new_entries)

if __name__ == "__main__":
    solver = SubsetSumSolver()
    data_pool = [413, 222, 117, 92, 193, 209, 350, 13]
    target_goal = 414

    print("=== EXECUTING SQLITE SUBSET SUM SOLVER ===")
    exact_res = solver.solve_exact(data_pool, target_goal)
    print(f"Exact Solution: {exact_res} (Sum: {sum(exact_res) if exact_res else 0})")
    
    approx_val = solver.solve_fptas(data_pool, target_goal, epsilon=0.05)
    print(f"FPTAS Approximation: {approx_val}")
