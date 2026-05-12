import sqlite3
import logging
import time
from typing import List, Optional, Dict
from decimal import Decimal, getcontext

getcontext().prec = 50
logger = logging.getLogger(__name__)


class CoreEngine:
    def __init__(self, db_name="checkpoint.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self._setup_db()

    def _setup_db(self):
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA synchronous=NORMAL;")
        self.conn.execute("CREATE TABLE IF NOT EXISTS left_sums (s_val TEXT PRIMARY KEY, n_val TEXT)")
        self.conn.execute("CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT)")
        self.conn.commit()

    def run_solve(self, numbers: List[int], target: int, epsilon: float = 0.0, force_restart: bool = False):
        if force_restart:
            self.conn.execute("DELETE FROM left_sums")
            self.conn.execute("DELETE FROM metadata")

        d_numbers = [Decimal(str(n)) for n in numbers]
        d_target = Decimal(str(target))
        mid = len(d_numbers) // 2

        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT count(*) FROM left_sums")
        exists = self.cursor.fetchone()[0]

        if exists > 1:
            logger.info("Existing checkpoint found. Resuming from persistent state...")
        else:
            logger.info("No checkpoint found. Generating sub-sums...")
            left_sums = {Decimal('0'): Decimal('0')}
            for num in d_numbers[:mid]:
                new_sums = {s + num: num for s in left_sums}
                left_sums.update(new_sums)

            self._flush_to_db(left_sums)

        return self._perform_mitm_search(d_numbers[mid:], d_target, Decimal(str(epsilon)))

    def _flush_to_db(self, data: Dict[Decimal, Decimal]):
        self.conn.execute("BEGIN TRANSACTION")
        self.conn.executemany("INSERT OR IGNORE INTO left_sums VALUES (?, ?)",
                              [(str(s), str(n)) for s, n in data.items()])
        self.conn.commit()
        logger.info(f"State flushed to {self.db_name}")

    def _perform_mitm_search(self, right_part, target, epsilon):
        pass
