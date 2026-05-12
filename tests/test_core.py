import pytest
import os
from subset_sum_solver import CoreEngine


@pytest.fixture
def engine():
    """
    Fixture to initialize the engine with a dedicated test database.
    Ensures a clean state for every test case.
    """
    test_db = "test_engine.db"
    engine_instance = CoreEngine(db_name=test_db)
    yield engine_instance

    engine_instance.conn.close()
    if os.path.exists(test_db):
        try:
            os.remove(test_db)
        except PermissionError:
            pass


def test_successful_subset_sum(engine):
    """
    Validates that the engine finds a valid subset for a known target.
    Tests the fundamental Meet-in-the-Middle intersection logic.
    """
    numbers = [10, 20, 30, 40, 50, 60]
    target = 110
    result = engine.run_solve(numbers, target)
    assert result is not None
    assert sum(result) == target
    for x in result:
        assert x in numbers


def test_no_possible_solution(engine):
    """
    Verifies that the engine returns None when the target is unreachable.
    """
    numbers = [1, 2, 3]
    target = 100
    result = engine.run_solve(numbers, target)
    assert result is None


def test_negative_values_support(engine):
    """
    Tests the algorithm's ability to handle negative integers.
    Meet-in-the-Middle naturally supports negatives as long as the 
    search space is correctly partitioned.
    """
    numbers = [-10, 15, 20, -5]
    target = 5
    result = engine.run_solve(numbers, target)
    assert result is not None
    assert sum(result) == target


def test_target_zero(engine):
    """
    Edge case: Target sum of zero should return an empty list 
    representing the empty subset.
    """
    result = engine.run_solve([1, 2, 3], 0)
    assert result == []


def test_large_dataset_performance(engine):
    """
    Complexity test: Ensures the MITM approach handles N=30+ 
    which would be slow for a standard iterative approach.
    """
    import random
    numbers = [random.randint(1, 1000) for _ in range(30)]
    target = sum(random.sample(numbers, 5))

    import time
    start = time.time()
    result = engine.run_solve(numbers, target)
    duration = time.time() - start

    assert result is not None
    assert sum(result) == target
    assert duration < 5.0


def test_single_element_match(engine):
    """
    Tests if the solver identifies a single element that matches the target.
    """
    numbers = [100]
    target = 100
    result = engine.run_solve(numbers, target)
    assert result == [100]
