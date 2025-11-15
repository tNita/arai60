
## Step2~Step3をもう一度

### Step2

他の人の解き方見てみる

- https://docs.google.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0#heading=h.z4zz4wpn0zz0
    - 身体性を意識するのはなるほどと思った
    - 最初にnum_to_indexを作ってからループして探すのは、一旦手分けしてどこにどの数字が書いていあるかだけをチェックさせ、二度手間
- https://github.com/docto-rin/leetcode/pull/11#discussion_r2410069093
    - 有名な略語（APIなど）やチームで既知の略語以外は省略しない方が良さそう
    - 今回はチームで既知の略語はない前提
    - elementをeleと略すのは有名な略語とは言い切れないのできちんとelementと略さず書くべきだった
- https://github.com/docto-rin/leetcode/pull/11/files#diff-486e02ef0f44505ce56030d2de6b9d8fad5fd9557caf068d7d14fa45ee2f8af1R12-R14
    - この前提があるから今の実装でも問題ないよという証明を行ったが、自分自身を守っているだけで、ソフトウェアエンジニアリングになっていない
    - Only one valid answer existsじゃなくても耐えれるように考えるのがソフトウェアエンジニアリングのはず
    - そう考えるとnum_to_indexを作るのは自然となしだなとなりそう
- https://github.com/cheeseNA/leetcode/pull/1/files#r1525853095
    - 答えがない時、[]、None、[-1, -1]などを返したり、Exceptionを使ったり色々選択肢はある
    - 好みの範囲であるが、チーム内でルールが決まっていないと辛くなる
    - Exceptionはコードが追いづらくなるので避けた方がいいかも
    - 値として存在しないことを返してあげた方が使う側にとってやや親切


## Step3

```Python3
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_to_index = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_to_index:
                return [num_to_index[complement], i]
            num_to_index[num] = i
        
        # 問題の制約上ここには到達しません
        return [-1, -1]
```


## Step4
レビューを受けて


 ナイーブな実装をもう一度
```Python3
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i, num_i in enumerate(nums):
            for j, num_j in enumerate(nums):
                if i == j:
                    continue
                if num_i + num_j == target:
                    return [i, j]
        # 問題の制約上ここには到達しません
        return [-1, -1]
```

- 2ポインタ法をもう一度
```
from bisect import bisect_left

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        index_and_num = list(enumerate(nums))
        index_and_num.sort(key=lambda x:x[1])
        left = 0
        right = len(index_and_num) - 1
        while left < right:
            num_sum = index_and_num[left][1] + index_and_num[right][1]
            if num_sum == target:
                return [index_and_num[left][0], index_and_num[right][0]]
            elif num_sum > target:
                right -= 1
            else:
                left += 1
        # 問題の制約上ここには到達しません
        return [-1, -1]

```

- 二分探索をもう一度
```
from bisect import bisect_left

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_and_index = [(num, i) for i, num in enumerate(nums)]
        num_and_index.sort()

        for i, (num_i, index_i) in enumerate(num_and_index):
            complement = target - num_i
            j = bisect_left(num_and_index, complement, lo=i+1, key=lambda x:x[0])
            if j < len(num_and_index) and num_and_index[j][0] == complement:
                return [index_i, num_and_index[j][1]]
        # 問題の制約上ここには到達しません
        return [-1, -1]
```