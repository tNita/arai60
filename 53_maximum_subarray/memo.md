# 53. Maximum Subarray

Given an integer array nums, find the subarray with the largest sum, and return its sum.

constraint
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4


## Step1
- 各要素をtailとするsubsequnceの最大値を記録していけば良さそう

```Python3
class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        # 番兵
        max_sums_by_tail = [0]
        for num in nums:
            max_sum = max(max_sums_by_tail[-1] + num, num)
            max_sums_by_tail.append(max_sum)
        return max(max_sums_by_tail)
```
- `nums=[-1]`のときNG
- 番兵まで入れてしまっていた
```Python3
class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        if len(nums) == 0:
            return 0
        # 番兵
        max_sums_by_tail = [0]
        for num in nums:
            max_sum = max(max_sums_by_tail[-1] + num, num)
            max_sums_by_tail.append(max_sum)
        return max(max_sums_by_tail[1:]) 
```
- 時間計算量: O(N)
- 空間計算量: O(N)

## Step2
### AIレビュー
> - 配列に状態を残す実装として、時間 O(N)、空間 O(N) の見積もりは合っています。なお、`max_sums_by_tail[1:]` も新しいリストを作るため、ここでも O(N) の時間と追加領域を使います。次の状態の計算に必要なのは直前の状態だけなので、「現在の要素で終わる最大和」と「これまでの最大和」の二つの変数にすれば、追加領域は O(1) にできます。たとえば `max_sum_ending_here` と `max_sum_so_far` なら、二つの最大値の違いも名前から読み取れます。こちらを試すなら、走査にも `nums[1:]` を使わず、添字やイテレータで進めるとよいでしょう。
- 確かに

### 他の人のコード、コメント集
- https://discord.com/channels/1084280443945353267/1206101582861697046/1208414507735453747
  - kadaneへの発想
  - 愚直にやる→[i, j]の和を求めるのに累積和を利用→jを固定して考えるとjを末尾とする部分列の最大はjまでの累積和 - jより前までの累積和の最小値 → jまでの累積和 - jより前までの累積和の最小値 を位置変数として式変形するとkadane
- https://github.com/Fuminiton/LeetCode/pull/32#discussion_r2050216094
  - 分割統治でもとける
  - 真ん中を基準に左右それぞれと真ん中をまたぐパターンを考慮
- https://github.com/fuga-98/arai60/pull/32
  - 自分のstep1のやり方に近いが少し違う
    -  前の和がマイナスかどうかで前の和につなげるかどうかをチェックする
- https://github.com/hayashi-ay/leetcode/pull/36
  - 分割統治のやり方
- https://github.com/naoto-iwase/leetcode/pull/37
  - 分割統治 O(N) で

### 自分で実装してみる

分割統治

```Python3
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        # [left, right)の部分配列の最大
        def max_sub_array_helper(left, right):
            if left == right:
                return -inf
            if left == right - 1:
                return nums[left]
            mid = (left + right) // 2
            # midよりも左
            left_max = max_sub_array_helper(left, mid)
            # midよりも右
            right_max = max_sub_array_helper(mid + 1, right)
            # midを含む
            inner_max = calculate_inner_max_sum(left, right, mid)
            return max(left_max, right_max, inner_max)
            
        def calculate_inner_max_sum(left, right, mid):
            left_sum = 0
            left_max = 0
            # mid - 1まで
            for i in range(mid - 1, left - 1, -1):
                left_sum += nums[i]
                left_max = max(left_max, left_sum)
            right_sum = 0
            right_max = 0
            # mid + 1から
            for i in range(mid + 1, right):
                right_sum += nums[i]
                right_max = max(right_max, right_sum)
            return left_max + nums[mid] + right_max


        return max_sub_array_helper(0, len(nums))
```
jを末尾とする部分配列の最大和 = jまでの累積和 - jより左の最小の累積和
```Python3
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        previous_min_prefix_sum = 0
        prefix_sum = 0
        max_sum = -inf
        for num in nums:
            prefix_sum += num
            current_max_sum = prefix_sum - previous_min_prefix_sum
            max_sum = max(max_sum, current_max_sum)
            previous_min_prefix_sum = min(previous_min_prefix_sum, prefix_sum)
        return max_sum
```
current_max_sumを引き継ぐ形にしてkadane

current_max_sum
= prefix_sum - previous_min_prefix_sum
= prefix_sum_1つ前 + num - min(prefix_sum_1つ前, previous_min_prefix_sum_1つ前)
= prefix_sum_1つ前 + num - min(prefix_sum_1つ前,  prefix_sum_1つ前 - current_max_sum_1つ前)
= num + max(0, current_max_sum_1つ前)

```Python3
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        current_max_sum = -inf
        max_sum = -inf
        for num in nums:
            current_max_sum = max(0, current_max_sum) + num
            max_sum = max(max_sum, current_max_sum)
        return max_sum
```


## Step3

```Python3
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        prefix_sum = 0
        previous_min_prefix_sum = 0
        max_sum = -inf
        for num in nums:
            prefix_sum += num
            current_max_sum = prefix_sum - previous_min_prefix_sum
            max_sum = max(max_sum, current_max_sum)
            previous_min_prefix_sum = min(previous_min_prefix_sum, prefix_sum)
        return max_sum
```
