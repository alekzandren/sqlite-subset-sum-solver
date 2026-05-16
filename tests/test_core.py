import pytest
from subset_sum_solver import SubsetSumSolver

@pytest.fixture
def solver() -> SubsetSumSolver:
    """Fixture to initialize the solver instance before running tests."""
    return SubsetSumSolver()


@pytest.fixture
def sample_data() -> tuple[list[int], int]:
    """Fixture providing the target testing data suite."""
    data_pool = [413, 222, 117, 92, 193, 209, 350, 13]
    target_goal = 414
    return data_pool, target_goal


def test_solve_exact_success(solver: SubsetSumSolver, sample_data: tuple[list[int], int]) -> None:
    """
    Validates that the Meet-in-the-Middle (MITM) algorithm successfully finds
    an exact subset that sums up precisely to the target goal.
    """
    data_pool, target_goal = sample_data

    exact_solution = solver.solve_exact(data_pool, target_goal)

    assert exact_solution is not None, "Exact solution should be found for this dataset"
    assert sum(exact_solution) == target_goal, f"Subset elements sum {sum(exact_solution)} must equal {target_goal}"

    for item in exact_solution:
        assert item in data_pool, f"Element {item} in solution was not present in the input data pool"


@pytest.mark.parametrize("epsilon", [0.05, 0.1, 0.01])
def test_solve_fptas_bounds(solver: SubsetSumSolver, sample_data: tuple[list[int], int], epsilon: float) -> None:
    """
    Validates that the Fully Polynomial-Time Approximation Scheme (FPTAS)
    respects the theoretical lower bound constraints: Result >= (1 - epsilon) * OPT.
    """
    data_pool, target_goal = sample_data

    approx_value = solver.solve_fptas(data_pool, target_goal, epsilon=epsilon)

    assert approx_value <= target_goal, f"FPTAS returned {approx_value}, exceeding maximum capacity {target_goal}"

    guaranteed_floor = (1.0 - epsilon) * target_goal
    assert approx_value >= guaranteed_floor, (
        f"FPTAS violated lower error corridor boundary. "
        f"Returned: {approx_value}, Expected at least: {guaranteed_floor}"
    )
