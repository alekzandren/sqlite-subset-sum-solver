import sqlite3
import logging
from typing import List, Optional, Dict
from decimal import Decimal, getcontext

getcontext().prec = 50

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
                               (s_val TEXT PRIMARY KEY, n_val TEXT)''')
        self.conn.commit()

    def _trim(self, sums: Dict[Decimal, Decimal], delta: Decimal) -> Dict[Decimal, Decimal]:
        if not sums: return {Decimal('0'): Decimal('0')}

        sorted_keys = sorted(sums.keys())
        trimmed = {Decimal('0'): Decimal('0')}
        last_kept = sorted_keys[0]

        for s in sorted_keys:
            if s > last_kept * (Decimal('1') + delta):
                trimmed[s] = sums[s]
                last_kept = s
        return trimmed

    def run_solve(self, numbers: List[int], target: int, epsilon: float = 0.0):
        d_numbers = [Decimal(str(n)) for n in numbers]
        d_target = Decimal(str(target))
        d_eps = Decimal(str(epsilon))

        n_len = len(d_numbers)
        mid = n_len // 2
        delta = d_eps / (Decimal('2') * Decimal(str(n_len))) if d_eps > 0 else Decimal('0')

        left_sums = {Decimal('0'): Decimal('0')}
        for num in d_numbers[:mid]:
            new_sums = {s + num: num for s in left_sums}
            left_sums.update(new_sums)
            if delta > 0:
                left_sums = self._trim(left_sums, delta)

        self.cursor.execute("BEGIN TRANSACTION")
        self.cursor.executemany("INSERT OR IGNORE INTO left_sums VALUES (?, ?)",
                                [(str(s), str(n)) for s, n in left_sums.items()])
        self.conn.commit()

        right_sums = {Decimal('0'): Decimal('0')}
        for num in d_numbers[mid:]:
            new_right = {}
            for rs in right_sums:
                curr_rs = rs + num
                needed = d_target - curr_rs

                if d_eps == 0:
                    self.cursor.execute("SELECT n_val FROM left_sums WHERE s_val = ?", (str(needed),))
                else:
                    lower = needed / (Decimal('1') + d_eps)
                    self.cursor.execute("SELECT s_val, n_val FROM left_sums WHERE s_val BETWEEN ? AND ?",
                                        (str(lower), str(needed)))

                match = self.cursor.fetchone()
                if match:
                    path_left = self._get_db_path(Decimal(match[0]))
                    path_right = self._reconstruct_mem_path(right_sums, rs) + [num]
                    return [int(x) for x in path_left + path_right]

                new_right[curr_rs] = num
            right_sums.update(new_right)
            if delta > 0:
                right_sums = self._trim(right_sums, delta)

        return None

    def _get_db_path(self, target: Decimal) -> List[Decimal]:
        path = []
        curr = target
        while curr != 0:
            self.cursor.execute("SELECT n_val FROM left_sums WHERE s_val=?", (str(curr),))
            res = self.cursor.fetchone()
            if not res: break
            val = Decimal(res[0])
            path.append(val)
            curr -= val
        return path

    def _reconstruct_mem_path(self, sums_dict: dict, end_val: Decimal) -> List[Decimal]:
        path, curr = [], end_val
        while curr != 0:
            val = sums_dict.get(curr)
            if val is None: break
            path.append(val)
            curr -= val
        return path
