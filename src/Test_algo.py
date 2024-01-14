from StructuralCodeComparator import StructuralCodeComparator


code1 = """
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)
        for i in range(n - 1):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []  # No solution found
"""
code2 = (
    """
def add(x, y):
    return x + y
"""
    ""
)

comparator = StructuralCodeComparator()
similarity = comparator.compare_codes(code1, code2)
print(f"Similarity: {similarity}")
