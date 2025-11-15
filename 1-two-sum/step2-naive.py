class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i, ele_i in enumerate(nums):
            for j, ele_j in enumerate(nums):
                if ele_i + ele_j == target and i != j:
                    return [i, j]
        raise Exception("Answer does not exists.")

        # PythonのListは内部的に配列と表現されるので特定のインデックスから要素を取得するのはO(1)らしい→なので下でもパフォーマンス影響ない
        # https://wiki.python.org/moin/TimeComplexity
        # n = len(nums)
        # for i in range(n):
        #     for j in range(n):
        #         if nums[i] + nums[j] == target and i != j:
        #             return [i, j]
        # raise Exception("Answer does not exists.")
