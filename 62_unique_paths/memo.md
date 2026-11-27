# 62. Unique Paths

There is a robot on an m x n grid. The robot is initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.

Given the two integers m and n, return the number of possible unique paths that the robot can take to reach the bottom-right corner.

The test cases are generated so that the answer will be less than or equal to 2 * 109.

- 1 <= m, n <= 100

## Step1

- マス目にそのマスに到達する経路の数を記録していく
  - 左隣の経路数 + 上隣の経路数

Wrong Answer

```Python3 

class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        paths = [[0] * m for _ in range(n)]
        def get_path(i, j):
            if i >= m or j >= n:
                raise ValueError("index out of range")
            if i == -1 or j == -1:
                return 0
            return paths[j][i]
        
        for i in range(m):
            for j in range(n):
                paths[j][i] = get_path(i - 1, j) + get_path(i, j - 1)
        return get_path(m - 1, n - 1)
```
- paths[0][0]は1でないといけない

```Python3
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        paths = [[0] * m for _ in range(n)]
        def get_path(i, j):
            if i >= m or j >= n:
                raise ValueError("index out of range")
            if i == -1 or j == -1:
                return 0
            return paths[j][i]
        
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    paths[0][0] = 1
                    continue
                paths[j][i] = get_path(i - 1, j) + get_path(i, j - 1)
        return get_path(m - 1, n - 1)
```

- pathsにアクセスするときにpaths[j][i]のように、iとjの順序が逆になってしまうのが気持ち悪い→クラスに隠蔽する
```Python3
 class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        paths = self.Paths(m, n)
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    continue
                path_count = paths.get_paths(i - 1, j) + paths.get_paths(i, j - 1)
                paths.set_paths(i, j, path_count)
        return paths.get_paths(m - 1, n - 1)

    class Paths:
        def __init__(self, m, n):
            self.m = m
            self.n = n
            self.paths = [[0] * m for _ in range(n)]
            self.paths[0][0] = 1
        
        def get_paths(self, i, j):
            if i >= self.m or j >= self.n:
                raise ValueError("index out of range")
            if i == -1 or j == -1:
                return 0
            return self.paths[j][i]

        def set_paths(self, i, j, paths_count):
            # 開始位置は1で固定
            if i == 0 and j == 0:
                return
            self.paths[j][i] = paths_count
```


## Step2
### コメント集・他の人のコード
- https://github.com/olsen-blue/Arai60/pull/33#discussion_r1966730122
  - メモ化をしない場合の再帰
- https://github.com/saagchicken/coding_practice/pull/19#discussion_r2007873330 
  - > 私は二重ループを、右の添字のほうが内側のループになるように回しますが、Python の場合はあまり気にするところではないかもしれません。
    C++ とかだと、メモリーの配置と速度にわずかに関係があったりします。
  - https://en.wikipedia.org/wiki/Row-_and_column-major_order
  - CだとRow-major order→右の添字で順番にアクセスしたほうが相性が良い→tmp.cで検証
  - PythonはRow-major orderでもColumn-major orderでもない
  - > Even less dense is to use lists of lists, e.g., in Python

```
>>> a = [[10000, 2, 30000], [4, 50000, 6]]
>>> [id(x) for row in a for x in row]
[4312768048, 4311804240, 4312503664, 4311804304, 4313223248, 4311804368]
>>> addresses = [id(x) for row in a for x in row]
>>> [y - x for x, y in zip(addresses, addresses[1:])]
[-963808, 699424, -699360, 1418944, -1418880]
```

- https://github.com/saagchicken/coding_practice/pull/16#discussion_r1999775338
  - > リストを掛け算で長くすると中身が同じオブジェクトを指すことになるが、数字の場合は immutable で += などをしてもオブジェクトが作り直されるので大きな問題がないが、リストのように mutable なオブジェクトを掛け算で複製すると、実態はひとつなので、一つを変更するとすべてが変更されたように見える、ということです。
  - 数字は掛け算したタイミングでコピーされると勘違いしていた。。。
  - https://docs.python.org/ja/3/builtins/stdtypes.html#common-sequence-operations
  - > シーケンス s の要素はコピーされず、同じ要素が複数回参照されることに注意してください。
- https://github.com/hayashi-ay/leetcode/pull/39
  - `num_of_paths = [ [0] * n for _ in range(m) ]`のようにn x mにすれば、iとjが逆になる問題も解決できる（→step1でn x mは図にマッチしない感じがして違和感があったがそんなこともないか）
  - i = 0 or j = 1は1通りと最初に決めておくやり方
  - 一次元DPでもできる
  - m+n-2Cm-1で解く
    - 末尾再帰（ただしPythonは末尾再帰最適化未実装らしい）
      - > Stock Python implementations do not perform tail-call optimization, though a third-party module is available to do this.
      - https://en.wikipedia.org/wiki/Tail_call#Language_support
    - math.factorialやmath.combを使う方法もあり
- https://github.com/fuga-98/arai60/pull/33
  - > `num_possible[row][column] = num_possible[row-1][column] + num_possible[row][column-1]`
  - indexが-1になるとき、探し方からその値はまだ0の状態がわかる→そのまま利用して良い（`num_possible[0][2] = num_possible[-1][2] + num_possible[0][1]` のとき、`num_possible[-1][2]`はまだ0）
  - 戻り値は[-1][-1]で
- https://github.com/kazuki-official/leetcode/pull/33
  - n + 1 x m + 1 でやる（そうすると-1の時のケアが不要に）
  - 一次元DP（２つ配列を用意）

### Cpythonのcombを読む
- math_comb_impl
- https://github.com/python/cpython/blob/619edb802e10741eff8eeab7dd279406bcd4b39c/Modules/mathmodule.c#L3676
  - overflowするかで処理を場合分け
    - perm_comb
      - j = k / 2として C(n, k) = C(n, j) * C(n-j, k-j) // C(k, j) 
    - perm_comb_small
      - あらかじめ計算結果を持っておく、奇数部分と2の累乗に分けて計算する感じ？
      - 大きめのnに対しては再帰
  - プロダクションコードでもassertって使うの一般的なんだ。
  - まだふわふわした理解だが、非常に多くの最適化がされていることがわかった

### 自分でコードを書いてみる

自前factorial

```Python3
from functools import cache
class Solution:
    @cache
    def factorial(self, k):
        if k == 0:
            return 1
        return k * self.factorial(k - 1)

    def uniquePaths(self, m: int, n: int) -> int:

        return self.factorial(m + n - 2) // (self.factorial(m - 1) * self.factorial(n - 1))
```

math.factorial

```Python3
import math
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:

        return math.factorial(m + n - 2) // (math.factorial(m - 1) * math.factorial(n - 1))
```

math.comb

```Python3
import math
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        return math.comb(m + n - 2, m - 1)
```

## Step3

```Python3
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        paths = [1] * n
        for _ in range(1, m):
            for i in range(1, n):
                paths[i] = paths[i] + paths[i - 1]
        return paths[n - 1]
```