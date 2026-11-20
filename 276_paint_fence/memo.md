# Painting the Fence

- https://www.geeksforgeeks.org/problems/painting-the-fence3727/1
- (対応するleetcodeの問題)[https://leetcode.com/problems/paint-fence/]

Given a fence with n posts and k colours, find out the number of ways of painting the fence so that not more than two consecutive posts have the same colours.
Answers are guaranteed to be fit into a 32 bit integer.

Constraints:

1 ≤ n ≤ 300
1 ≤ k ≤ 10^5

## Step1
- 色は1、2、...kで表す
- 手作業でやるとすると樹形図
  - 愚直にリストにすべての選択肢を追加していくやり方あり→非効率になりそうなので別の方法考える
  - 3つ以上連続はNGである性質を使う
    - 直前の2つが同じ色: 次はk-1色（どれも次の直前の２つは色が異なる）
    - 直前の2つが違う色: 次はk色（うち一つは次の直前の２つは色同じ、それ以外は次の直前の２つは色が異なる）
```Python3 
class Solution:
    def countWays(self,n,k):
        if n < 2:
            return k
        last_two_same = k
        last_two_different = k * (k-1)
        for i in range(n - 2):
            last_two_same,last_two_different = last_two_different, last_two_same * (k-1) + last_two_different * (k-1)
        return last_two_same + last_two_different
```


## Step2
### AIレビュー

> - 遷移については、「次の色が直前と同じなら、元の末尾2本は異なる必要があり、選択肢は1色」「次の色が直前と異なるなら、元の状態によらず選択肢は `k - 1` 色」と説明できますね。後者の式は `(last_two_same + last_two_different) * (k - 1)` とまとめると、その説明と対応します。単に掛け算を減らすというより、共通している意味を式に出すためです。

- そうだね。その書き方もある。

> - 更新の行は少し横に長いですね。次の状態を別の変数に置くと、一つずつ意味を追えます。たとえば、現在の名前のままなら次のように書けます。元の同時代入も正しく、単純に2行の代入に分けると更新済みの値を使ってしまう点には注意してください。
  ```python
  for _ in range(n - 2):
      next_same = last_two_different
      next_different = (last_two_same + last_two_different) * (k - 1)
      last_two_same, last_two_different = next_same, next_different
  ```

> - 細かいところでは、使っていないループ変数 `i` は `_` にすると、回数だけが必要だと伝わります。`def countWays(self, n, k):` や `k - 1` のように、空白も揃えると読みやすいでしょう。

- 確かに

### 他の人のコードやコメント集
https://discord.com/channels/1084280443945353267/1233603535862628432/1270597315681456219
  - 再帰の場合はフィボナッチ数列の値を再帰で求めるときと同じ計算量
  - 計算量は黄金比のn乗
- https://github.com/hayashi-ay/leetcode/pull/17
  - > 前回と異なる色で塗る場合、前回と同じ色で塗る場合の2つで考える。
  - `@cache`を利用してメモ化の再帰も可能
  - `@cache`を自作するのを後でやる
- https://github.com/mamo3gr/arai60/pull/57
  - 漸化式をもとにループで実装
- https://github.com/naoto-iwase/leetcode/pull/35
  - LRUCacheクラス自体に`__contain__`メソッドを定義して、このオブジェクトに対してinを使えるようにする
- https://github.com/kazuki-official/leetcode/pull/30
  - > コンパイラのレジスタ割り当ての時のグラフ彩色問題を思い出した
  - https://ja.wikipedia.org/wiki/%E3%83%AC%E3%82%B8%E3%82%B9%E3%82%BF%E5%89%B2%E3%82%8A%E4%BB%98%E3%81%91
  - > 数をノードとし、2つの変数が同時に生存する場合にそれらノード間にエッジを設定した干渉グラフ（interference graph）を構築する。より正確に言えば、ある変数が生存中に別の変数が定義されれば、それらは干渉すると言える。このグラフの彩色をするというのは、エッジで直接結ばれたノード同士が同じ色にならないように、かつなるべく少ない色数でグラフの全ノードを彩色することに他ならない。このグラフを R 色で彩色できる場合、そのコード部分では変数を格納するのに R 個のレジスタが必要ということになる。

### 様々な方法で実装してみる
漸化式ループパターン
$T_i = (k-1)(T_{i-1} + T_{i-2})$

```Python3
class Solution:
    def countWays(self,n,k):
        count = [0] * n
        count[0] = k
        if n == 1:
            return count[-1]
        count[1] = k * k
        if n == 2:
            return count[-1]
        for i in range(2, n):
             count[i] = (k-1) * (count[i-1] + count[i-2])
        return count[-1]
```

@cacheでメモ化

```Python3
import functools

class Solution:
    @functools.cache
    def countWays(self,n,k):
        if n == 1:
            return k
        if n == 2:
            return k * k
        return (k-1) * (self.countWays(n-1, k) + self.countWays(n-2, k))
```

自前@cache
```Python3
class LRUCache:
    def __init__(self):
        # 簡単のため決め打ち
        self.max_size = 10000
        self.cache = {}
        self.sentinel = self.Node()
        self.sentinel.prev = self.sentinel
        self.sentinel.next = self.sentinel
    
    def get(self, key):
        if key not in self.cache:
            return None
        value = self.cache[key].value
        self.remove(key)
        self.insert_front(key, value)
        return value

    def remove(self, key):
        if key not in self.cache:
            return
        removed_node = self.cache[key]
        del self.cache[key]
        removed_node.next.prev = removed_node.prev
        removed_node.prev.next = removed_node.next
        
    def insert_front(self, key, value):
        node = self.Node(key, value)
        node.prev = self.sentinel
        node.next = self.sentinel.next
        self.sentinel.next.prev = node
        self.sentinel.next = node
        self.cache[key] = node
        if len(self.cache) > self.max_size:
            self.remove(self.sentinel.prev.key)

    class Node:
        def __init__(self, key=None, value=None, prev=None, next=None):
            self.key = key
            self.value = value
            self.prev = prev
            self.next = next
            
def my_cache(func):
    cache = LRUCache()
    def inner(*arg, **kargs):
        cached_result = cache.get(arg)
        if cached_result is not None:
            return cached_result
        result = func(*arg, **kargs)
        cache.insert_front(arg, result)
        return result
    return inner

class Solution:
    @my_cache
    def countWays(self,n,k):
        if n == 1:
            return k
        if n == 2:
            return k * k
        return (k-1) * (self.countWays(n-1, k) + self.countWays(n-2, k))
```

## Step3

```Python3
class Solution:
    def countWays(self,n,k):
        counts = [0] * n
        if n == 1:
            return k
        if n == 2:
            return k * k
        counts[0] = k
        counts[1] = k * k
        for i in range(2, n):
            counts[i] = (k - 1) * (counts[i-1] + counts[i-2])
        return counts[n-1]
```