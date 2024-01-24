try:
    from src.code_comparator import compare_codes

except ModuleNotFoundError:
    import sys
    from pathlib import Path

    sys.path.append(str(Path.cwd()))  # to allow importing from src folder

    from src.code_comparator import compare_codes

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
code2 = """
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)
        for i in range(n - 1):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []  # No solution found
"""


similarity = compare_codes(code1, code2)
print(f"Percentage: {similarity['similarity_percentage']}")
print(f"Features: {similarity['common_features']}")
