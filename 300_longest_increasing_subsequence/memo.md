# 300. Longest Increasing Subsequence

Given an integer array nums, return the length of the longest strictly increasing subsequence.

Constraints:

- 1 <= nums.length <= 2500
- -10^4 <= nums[i] <= 10^4

## Step1

- 配列を用意し、numsそれぞれに対してその要素を末尾とする最大のsubsequenceの要素数を記録する
  - 位置0~i-1の要素のうち、位置iの要素より小さいものを対象
  - 対象とした要素のうちもっとのsubsequenceが長いもの+1が位置iの要素の最大subsequnce

```Python3
class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        nums_count = len(nums)
        subsequence_lengths = [0] * nums_count
        for i in range(nums_count):
            prev_max_subsequnce = 0
            for j in range(i):
                if nums[i] > nums[j]:
                    prev_max_subsequnce = max(prev_max_subsequnce, subsequence_lengths[j])
            subsequence_lengths[i] = prev_max_subsequnce + 1
        return max(subsequence_lengths)
```
- 時間計算量: O(n^2)
- 空間計算量: O(n)

時間計算量を改善したい。
- 内側のforを改善できる気がするが、思いつかなかった。。。

## Step2

### AIレビュー

> - `prev_max_subsequnce` は部分列そのものが入っているように読めますが、実際に入っているのは長さですね。たとえば `max_previous_length` など、長さであることが分かる名前にすると読みやすいと思います。`subsequnce` の綴りも `subsequence` ですね。

- 納得。

> - 「内側の for を改善できる気がする」はよい着眼点だと思います。では、これまでに見つかった部分列の情報を全部持つ必要はあるでしょうか。たとえば、同じ長さの部分列 `[2, 5]` と `[2, 8]` があったとして、後ろに要素をつなげるにはどちらが有利でしょう。末尾が 8 のものにつなげられる値は、末尾が 5 のものにもつなげられますね。この先に作れる長さだけを考えるなら、同じ長さの部分列では、末尾の最小値だけを残せそうです。
> - そこから、`min_tails[k]` を「ここまでに見た要素で作れる、長さ `k + 1` の増加部分列の末尾の最小値」としてみてください。この配列は狭義の昇順になります。長さ `k + 2` の部分列から末尾を外せば、それより小さい末尾を持つ長さ `k + 1` の部分列が得られるためです。新しい値 `x` に対して、初めて `x` 以上になる位置を置き換え、なければ末尾に追加すると、この意味を保って更新できます。昇順なので位置を二分探索でき、全体で時間 `O(n log n)`、空間 `O(n)` にできます。
> - ここで、探す位置を「`x` より大きい」にするとどうなるか、`[2, 2, 2]` で確認してみてください。今回は同じ値では長さを伸ばせないので、「`x` 以上」を探す必要があります。また、`[3, 5, 6, 2]` を手で追うと、最後の `min_tails` は `[2, 5, 6]` になりますが、これは元の配列の部分列ではありません。それぞれの長さに対する末尾の最小値を別々に記録している、という点は押さえておくとよいでしょう。

- min_tailsに長さごとの末尾を記録していく感じ、良さそう

### コメント集・他の人のコード
- https://discord.com/channels/1084280443945353267/1200089668901937312/1209563502407065602
  - https://leetcode.com/problems/longest-increasing-subsequence/solutions/1326308/c-python-dp-binary-search-bit-segment-tree-solutions-picture-explain-o-nlogn/
  - セグメント木を使う方法（3-5）
  - セグメント木: https://algo-logic.info/segment-tree/
  - BIT: https://algo-logic.info/binary-indexed-tree/
  - 座標圧縮: 実際の値をindexにしてセグメント木 or BITを作ると無駄が多い →今回は値の大小関係だけが大事なので、それぞれの値は小さいものから数えて何番目かの情報でセグメント木 or BITを作る
- https://github.com/thonda28/leetcode/pull/16/changes#diff-5d85004121fdaf34abe9af172f266e7f57f39e2165ac80e3ecbd849d1831c141R12
  - セグメント木別実装
    - 再帰
    - 最大値以外も対応（判断基準の関数を引数に渡す）
- https://github.com/Mike0121/LeetCode/pull/50#discussion_r1966726918
  - > つまり、そういう可能性を見ながらコードを書けるかなのです。そういう風に話が変わったときにどれくらい柔軟であるべきかなども俎上に載せて計算して書いています。
  - https://github.com/Mike0121/LeetCode/pull/50#discussion_r1966726918

- https://github.com/naoto-iwase/leetcode/pull/36
  - セグメント木
    - 左端が右の子の場合はmax更新して右隣の上のセグメントへ
    - 右端が左の子の場合はmax更新して左隣の上のセグメントへ
- https://github.com/kazuki-official/leetcode/pull/31
  - 二分探索を自分で実装
    - left_inclusive, right_incluesiveという命名わかりやすい
  - 座標圧縮: rankという命名
  - セグ木
    - getが非効率。全ての葉を見てしまっている

### 自分でも実装してみる

セグメント木実装
```Python3
class SubsequnceMaxLengthSegmentTree:
    def __init__(self, size):
        self.leaf_nodes = 1
        while self.leaf_nodes < size:
            self.leaf_nodes *= 2
        self.data = [0] * (2 * self.leaf_nodes)
    
    def query(self, queried_left, queried_right):
        def query_helper(segment_index, segment_left, segment_right):
            if queried_right < segment_left or segment_right < queried_left:
                return 0
            if queried_left <= segment_left and segment_right <= queried_right:
                return self.data[segment_index]
            segment_mid = (segment_left + segment_right) // 2
            left_max = query_helper(2 * segment_index, segment_left, segment_mid)
            right_max = query_helper(2 * segment_index + 1, segment_mid + 1, segment_right)
            return max(left_max, right_max)
        
        return query_helper(1, 1, self.leaf_nodes)
    
    def update(self, index, value):
        segment_index = index + self.leaf_nodes - 1
        while segment_index > 0:
            self.data[segment_index] = max(self.data[segment_index], value)
            segment_index //= 2

class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        value_to_rank = {num: i + 1 for i, num in enumerate(sorted(set(nums)))}
        rank_nums = [value_to_rank[num] for num in nums]
        max_rank = max(rank_nums)
        subsequences = SubsequnceMaxLengthSegmentTree(max_rank)
        for rank in rank_nums:
            max_length = subsequences.query(1, rank - 1)
            subsequences.update(rank, max_length + 1)
        return subsequences.query(1, max_rank)
```

BIT実装
```Python3
class SubsequnceMaxLengthBit:
    def __init__(self, size):
        self.bit_size = 1
        while self.bit_size < size:
            self.bit_size *= 2
        self.data = [0] * (self.bit_size + 1)
    
    def query(self, index):
        max_length = 0
        while index > 0:
            max_length = max(max_length, self.data[index])
            index -= index & (-index)
        return max_length
    
    def update(self, index, value):
        while index < self.bit_size + 1:
            self.data[index] = max(value, self.data[index])
            index += index & (-index)

class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        value_to_rank = {num: i + 1 for i, num in enumerate(sorted(set(nums)))}
        rank_nums = [value_to_rank[num] for num in nums]
        max_rank = max(rank_nums)
        subsequences = SubsequnceMaxLengthBit(max_rank)
        for rank in rank_nums:
            max_length = subsequences.query(rank - 1)
            subsequences.update(rank, max_length + 1)
        return subsequences.query(max_rank)
```


## Step3

```Python3
class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        min_tail_by_length = []
        # num未満の最大のtailのindexを求める（ないときは-1）
        def find_max_tail_index(num):
            # [left, right]にある可能性
            left = 0
            right = len(min_tail_by_length) - 1
            while left <= right:
                mid = (left + right) // 2
                if min_tail_by_length[mid] < num:
                    left = mid + 1
                else:
                    right = mid - 1
            # leftは最大のtailの次にあるので
            return left - 1

        for num in nums:
            index = find_max_tail_index(num) + 1
            if index < len(min_tail_by_length):
                min_tail_by_length[index] = min(min_tail_by_length[index], num)
                continue
            min_tail_by_length.append(num)
        return len(min_tail_by_length)
```



