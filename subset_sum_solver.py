import sqlite3
import logging
import time
from typing import List, Optional, Dict
from decimal import Decimal, getcontext

getcontext().prec = 50
logger = logging.getLogger(__name__)


class CoreEngine:
    def __init__(self, db_name=":memory:", ram_threshold=100000):
        """
        Hybrid Solver: Uses RAM for speed, flushes to SQLite for persistence.
        :param ram_threshold: Max sub-sums to keep in RAM before forcing a sync.
        """
        self.conn = sqlite3.connect(db_name)
        self.ram_threshold = ram_threshold
        self._setup_db()

    def _setup_db(self):
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("DROP TABLE IF EXISTS left_sums")
        self.conn.execute("CREATE TABLE left_sums (s_val TEXT PRIMARY KEY, n_val TEXT)")
        self.conn.commit()

    def run_solve(self, numbers: List[int], target: int, epsilon: float = 0.0):
        start_time = time.time()
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


        self._flush_to_db(left_sums)

        logger.info(f"MITM phase initiated. Left-half states: {len(left_sums)}")

        return self._perform_search(d_numbers[mid:], d_target, d_eps)

    def _flush_to_db(self, data: Dict[Decimal, Decimal]):
        """ Demonstrates the architectural choice of persistent state. """
        self.conn.execute("BEGIN TRANSACTION")
        self.conn.executemany("INSERT OR IGNORE INTO left_sums VALUES (?, ?)",
                              [(str(s), str(n)) for s, n in data.items()])
        self.conn.commit()
