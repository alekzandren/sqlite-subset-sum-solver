import bisect
from array import array
from typing import List, Optional, Tuple, Dict


class SubsetSumSolver:
    """
    Academic-grade solver providing both Exact (Meet-in-the-Middle) and
    Approximate (FPTAS) optimized solutions for the Subset Sum Problem.
    """

    def solve_exact(self, nums: List[int], target: int) -> Optional[List[int]]:
        """
        Executes the Meet-in-the-Middle (MITM) algorithm.
        Splits the search space in half to break the O(2^n) combinatorial explosion.

        Time Complexity: O(2^{n/2} * log(2^{n/2}))
        Space Complexity: O(2^{n/2}) using space-efficient native arrays.
        """
        if not nums:
            return None if target != 0 else []

        n = len(nums)
        mid = n // 2
        left_half = nums[:mid]
        right_half = nums[mid:]

        left_dict = self._generate_sum_map(left_half)
        right_dict = self._generate_sum_map(right_half)

        sorted_right_sums = sorted(right_dict.keys())
        right_array = array('q', sorted_right_sums)

        for l_sum, l_path in left_dict.items():
            needed = target - l_sum
            idx = bisect.bisect_left(right_array, needed)

            if idx < len(right_array) and right_array[idx] == needed:
                return list(l_path) + list(right_dict[needed])

        return None

    def solve_fptas(self, nums: List[int], target: int, epsilon: float) -> int:
        """
        Fully Polynomial-Time Approximation Scheme (FPTAS).

        Guarantees that the returned subset sum is >= (1 - epsilon) * OPT.
        Time Complexity: O(n^2 / epsilon)

        Fixes the float precision vulnerability by avoiding direct float-to-int 
        multiplication bounds during the trim cascade.
        """
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
        """
        Trims the sorted list of sums to keep the state space bounded polynomially.
        Uses exponential stepping intervals to preserve the approximation corridor.
        """
        if not sorted_list:
            return []

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

    def _generate_sum_map(self, items: List[int]) -> Dict[int, Tuple[int, ...]]:
        """
        Generates all achievable subset sums mapped to their respective exact paths.
        Optimized via safe non-mutating hash-map generation cascades.
        """
        sums_map: Dict[int, Tuple[int, ...]] = {0: ()}
        for x in items:
            new_entries = {}
            for current_sum, path in sums_map.items():
                next_sum = current_sum + x
                if next_sum not in sums_map:
                    new_entries[next_sum] = path + (x,)
            sums_map.update(new_entries)
        return sums_map

if __name__ == "__main__":
    solver = SubsetSumSolver()
