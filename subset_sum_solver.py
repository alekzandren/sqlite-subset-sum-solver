import bisect
from array import array
from typing import List, Optional, Union


class SubsetSumSolver:
    """
    Academic-grade solver providing both Exact (MITM) and 
    Approximate (FPTAS) solutions for the Subset Sum Problem.
    """

    def solve_exact(self, nums: List[int], target: int) -> Optional[List[int]]:
        """
        Meet-in-the-Middle Algorithm.
        Complexity: O(2^{n/2} * log(2^{n/2}))
        Memory: O(2^{n/2}) using space-efficient arrays.
        """
        n = len(nums)
        if not nums: return None

        mid = n // 2
        left_half = nums[:mid]
        right_half = nums[mid:]

        left_dict = self._generate_sum_map(left_half)

        right_sums_dict = self._generate_sum_map(right_half)
        sorted_right_sums = sorted(right_sums_dict.keys())

        right_array = array('q', sorted_right_sums)

        for l_sum, l_path in left_dict.items():
            needed = target - l_sum
            idx = bisect.bisect_left(right_array, needed)

            if idx < len(right_array) and right_array[idx] == needed:
                return list(l_path) + list(right_sums_dict[needed])

        return None

    def solve_fptas(self, nums: List[int], target: int, epsilon: float) -> int:
        """
        Fully Polynomial-Time Approximation Scheme (FPTAS).
        Complexity: O(n^2 / epsilon)
        Guarantees: Result >= (1 - epsilon) * OPT
        """
        if not nums: return 0
        n = len(nums)
        delta = epsilon / (2 * n)

        l_list = [0]

        for x in nums:
            new_sums = [s + x for s in l_list if s + x <= target]
            combined = sorted(l_list + new_sums)
            l_list = self._trim(combined, delta)

        return max(l_list)

    def _trim(self, sorted_list: List[int], delta: float) -> List[int]:
        """Trims a sorted list to maintain polynomial size."""
        if not sorted_list: return []

        trimmed = [sorted_list[0]]
        last_added = sorted_list[0]

        for i in range(1, len(sorted_list)):
            if sorted_list[i] > last_added * (1 + delta):
                trimmed.append(sorted_list[i])
                last_added = sorted_list[i]

        return trimmed

    def _generate_sum_map(self, items: List[int]) -> dict:
        """Generates all possible subset sums with their components."""
        sums = {0: tuple()}
        for x in items:
            new_sums = {}
            for s, path in sums.items():
                if s + x not in sums:
                    new_sums[s + x] = path + (x,)
            sums.update(new_sums)
        return sums

if __name__ == "__main__":
    solver = SubsetSumSolver()
    data = [31, 41, 59, 26, 53, 58, 97]
    goal = 150

    exact_res = solver.solve_exact(data, goal)
    print(f"Exact Solution: {exact_res} (Sum: {sum(exact_res) if exact_res else 0})")

    approx_val = solver.solve_fptas(data, goal, epsilon=0.1)
    print(f"FPTAS Result (eps=0.1): {approx_val}")
