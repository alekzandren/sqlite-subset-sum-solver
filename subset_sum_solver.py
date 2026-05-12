import bisect
import logging
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)


class SubsetSumSolver:
    """
    Academic-grade solver implementing Meet-in-the-Middle (MITM)
    with O(2^{n/2} * log(2^{n/2})) complexity.
    """

    def solve(self, nums: List[int], target: int) -> Optional[List[int]]:
        n = len(nums)
        if n == 0: return None

        mid = n // 2
        left_half = nums[:mid]
        right_half = nums[mid:]

        left_sums = self._generate_subsums(left_half)
        right_sums = self._generate_subsums(right_half)

        sorted_right = sorted(right_sums.keys())

        for l_sum, l_path in left_sums.items():
            needed = target - l_sum
            idx = bisect.bisect_left(sorted_right, needed)

            if idx < len(sorted_right) and sorted_right[idx] == needed:
                return list(l_path) + list(right_sums[needed])

        return None

    def _generate_subsums(self, items: List[int]) -> dict:
        """Generates a mapping of sum -> components."""
        sums = {0: tuple()}
        for x in items:
            new_sums = {}
            for s, path in sums.items():
                new_sums[s + x] = path + (x,)
            sums.update(new_sums)
        return sums
