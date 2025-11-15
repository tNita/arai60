from bisect import bisect_left


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_to_index = [(v, i) for (i, v) in enumerate(nums)]
        num_to_index.sort(key=lambda x: x[0])
        nums_sorted = [v for (v, _) in num_to_index]
        nums_length = len(num_to_index)
        for pos, (num, i) in enumerate(num_to_index):
            complement = target - num
            j = bisect_left(nums_sorted, complement, pos + 1, nums_length)
            if j < nums_length and nums_sorted[j] == complement:
                return [i, num_to_index[j][1]]

        raise Exception("Answer does not exists.")
