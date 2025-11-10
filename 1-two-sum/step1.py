class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        numsDict = {ele: i for i, ele in enumerate(nums)}
        for i, ele in enumerate(nums):
            jValue = target - ele
            if jValue in numsDict:
                j = numsDict[jValue]
                if i != j:
                    return [i, j]

        raise Exception("Answer does not exists.")
