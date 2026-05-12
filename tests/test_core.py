import pytest
from decimal import Decimal
from subset_sum_solver import CoreEngine


class TestStressMetrics:
    @pytest.fixture
    def engine(self):
        return CoreEngine(":memory:")

    def test_precision_torture(self, engine):
        """ Test logic with high-magnitude difference to break IEEE 754 """
        numbers = [10 ** 18, 1, 2, 3]
        target = 10 ** 18 + 6
        result = engine.run_solve(numbers, target, epsilon=0)
        assert result is not None
        assert sum(result) == target

    def test_sqlite_overflow_bypass(self, engine):
        """ Test integers larger than SQLite's 64-bit limit """
        huge_val = 2 ** 128
        numbers = [huge_val, 500, 1000]
        target = huge_val + 1500
        result = engine.run_solve(numbers, target, epsilon=0)
        assert result is not None
        assert sum(result) == target

    def test_fptas_massive_scale(self, engine):
        """ N=60 with epsilon should finish fast while brute force would hang """
        import random
        numbers = [random.randint(10 ** 5, 10 ** 6) for _ in range(60)]
        target = sum(random.sample(numbers, 10))

        result = engine.run_solve(numbers, target, epsilon=0.1)
        assert result is not None
        assert sum(result) <= target
        assert sum(result) >= target * Decimal('0.9')

    def test_epsilon_extreme_bounds(self, engine):
        """ Test epsilon that is extremely small or large """
        nums = [10, 20, 30]
        assert engine.run_solve(nums, 50, epsilon=1e-20) == [20, 30]
        assert engine.run_solve(nums, 50, epsilon=1.0) is not None
