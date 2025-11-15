class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        index_to_num = list(enumerate(nums))
        index_to_num.sort(key=lambda x: x[1])
        nums_length = len(nums)
        left = 0
        right = nums_length - 1
        while (left < right) and (left > -1) and (right < nums_length):
            num_sum = index_to_num[left][1] + index_to_num[right][1]
            if num_sum == target:
                return [index_to_num[left][0], index_to_num[right][0]]
            elif num_sum > target:
                right -= 1
            else:
                left += 1

        raise Exception("Answer does not exists.")
