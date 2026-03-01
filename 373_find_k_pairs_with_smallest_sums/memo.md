# 373. Find K Pairs with Smallest Sums

You are given two integer arrays nums1 and nums2 sorted in non-decreasing order and an integer k.

Define a pair (u, v) which consists of one element from the first array and one element from the second array.

Return the k pairs (u1, v1), (u2, v2), ..., (uk, vk) with the smallest sums.

https://leetcode.com/problems/find-k-pairs-with-smallest-sums/description/


Constraints:

- 1 <= nums1.length, nums2.length <= 105
- -10^9 <= nums1[i], nums2[i] <= 10^9
- nums1 and nums2 both are sorted in non-decreasing order.
- 1 <= k <= 10^4
- k <= nums1.length * nums2.length

## Step1

- 手作業で行う
  - 具体的な場面を想像： 
    - 食べ物と飲み物がそれぞれ安い順に置いてある
  - k人分の食べ物と飲み物を買っていきたいが、お金がないので安く済ませたい。
  - 1 <= nums1.length, nums2.length <= 10^5 なので、総当たりで調査は遅くなりそうか？（O(n^2)）
    - nums1、nums2を先頭から見ていく
    - まずはどちらも先頭から（先頭+先頭が一番小さい）
    - 次に大きい和はどちらになるのかを決定：min(nums1先頭+nums2の次の要素 or nums1の次の要素+nums2先頭）
    - おなじように繰り返す：min(nums1[i+1]+nums2[j], num[i]+ nums2[j+1])

```Python3
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        if k > len(nums1) * len(nums2):
            raise ValueException(f"k must be under {len(nums1) * len(nums2)}")
        nums1_i = 0
        nums2_i = 0
        kth_smallest_pair = [[nums1[nums1_i], nums2[nums2_i]]]
        while len(kth_smallest_pair) < k:
            if nums1_i == len(nums1) - 1:
                nums2_i += 1
            elif nums2_i == len(nums2) - 1:
                nums1_i += 1
            elif nums1[nums1_i + 1] + nums2[nums2_i] < nums1[nums1_i] + nums2[nums2_i + 1]:
                nums1_i += 1
            else:
                nums2_i += 1
            kth_smallest_pair.append([nums1[nums1_i], nums2[nums2_i]])
        return kth_smallest_pair
```
  
- これだと一部漏らす
  - 例：
    - nums1 = [1, 7], nums2 = [3, 4], k = 3
    - 1 + 3 < 1 + 4 < 7 + 3 < 7 + 4
    - 上記のコードだと、[1,3] -> [1,4] -> [7,4] と進むが、[7,3] を漏らす。
- 単純化しすぎたか。。。
    - > 1 <= nums1.length, nums2.length <= 10^5 なので、総当たりで調査は遅くなりそうか？（O(n^2)）
    - 嫌な予感はするものの、一旦実装してから判断するか。
    - 総当たりでペアを列挙したのちにsortedを使って並べ替え。
    - heapの章なのでheapq.nth_smallestも使えるか（ヒープの章ではなかったら気づかなかった）
    -
```Python3
import heapq
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        if k > len(nums1) * len(nums2):
            raise ValueException(f"k must be under {len(nums1) * len(nums2)}")
        
        pairs = []
        for num1 in nums1:
            for num2 in nums2:
                pairs.append([num1, num2])
        # return sorted(pairs, key=lambda pair: pair[0]+pair[1])[:k]
        return heapq.nsmallest(k, pairs, key=lambda pair: pair[0]+pair[1])
```


- 代表的なケースはパスするようになったが、num1、num2の要素数が多いケースでメモリエラーになった。
  - 空間計算量がO(m * n)だもんな。
  - pairsがボトルネック。。。
  - 解法思い浮かばず断念

## Step2

### 他の人のコード読む
- https://github.com/hayashi-ay/leetcode/pull/66
  - candidateのpair をheapに入れていく方法→Step1の一番最初の解き方で抜け漏れがなくなるか
  - 二次元の表で考える
    - 右、下に行く限り、和は大きくなるので、右方向、下方向で次のペアをheapに入れていく
    - ペアの和を基準にheapを作る
    - 右→下、下→右で同じところに到達するので、すでに見たところはヒープへの追加をスキップする
    - (和, インデックス)をヒープに追加していけば、和を優先して比較しながらヒープを作ることができる
      - heapqでは、タプルも使える
        - > Heap elements can be tuples. This is useful for assigning comparison values (such as task priorities) alongside the main record being tracked:
        - https://docs.python.org/3/library/heapq.html
      - heapqの内部の実装見れば、タプルでもそのまま要素を比較している
        - https://github.com/python/cpython/blob/main/Lib/heapq.py#L283
      - タプルは一つ目の要素から優先に比較していく
        - >  The comparison uses lexicographical ordering: first the first two items are compared, and if they differ this determines the outcome of the comparison; if they are equal, the next two items are compared, and so on, until either sequence is exhausted. If two items to be compared are themselves sequences of the same type, the lexicographical comparison is carried out recursively.   
        - https://docs.python.org/3/tutorial/datastructures.html#comparing-sequences-and-other-types
  - (和, インデックス)は(和, (i, j))と(和, i, j)の形があるが、後者の方がシンプルか
  - https://discord.com/channels/1084280443945353267/1200089668901937312/1222573940610695341
    - > あと、本当は、(x - 1, y) と (x, y - 1) が両方 pairs の中にある、または、x, y どちらかが0でなければ、heap に足さなくていいとは思うんですよね。
    - (x,y)に到達した時に、そこに到達することが可能な他の経路が残っていなければheapに追加するという感じか
    - →heapに追加するのをできる限り遅くできるので、nums1とnums2で要素の値の大きさが大きく異なるときは有効（無駄なものをheapに追加しなくて良くなる）
- https://github.com/ksaito0629/leetcode_arai60/pull/6
  - setを使わず、next_i/j を用いる方法でのまとめ
  - https://github.com/ksaito0629/leetcode_arai60/pull/6/changes#diff-03a3fb8f1a7b3e86fadbacaa3d5f79bc6125150ee17fbc4bee45a9be9b1a5921R89
- https://github.com/aki235/Arai60/pull/10
  - > enqueue_if_valid_and_not_visited
  - これくらい説明的でもOK
- https://github.com/xbam326/leetcode/pull/12
- https://github.com/Hiroto-Iizuka/coding_practice/pull/10
  - 外部ライブラリを利用するときはimportで
    - https://github.com/Hiroto-Iizuka/coding_practice/pull/10/changes#r2658671322
  - なるほど、二次元表の1行目だけをcandidate（ヒープ）に入れておいて、そこから列ごとに下にいって見ていく感じか。
  - 見ていく方向が一方向なので、重複が起きないから、visitedの管理もいらないのか。
- https://github.com/mamo3gr/arai60/pull/10
- https://github.com/fuga-98/arai60/pull/11
  - popする前に中身があるか確認するのは大事
    - > If the heap is empty, IndexError is raised.
    - https://docs.python.org/3/library/heapq.html#heapq.heappop
  - 以下はwhileの条件に入れても良いかと感じた。（チームで明確なルールがない限り好みの範囲か）
```Python3
while True:
    if not candidate or len(result) >= k:
        break
```
- https://github.com/naoto-iwase/leetcode/pull/10
  - https://github.com/naoto-iwase/leetcode/pull/10/changes#r2409634906
  - 空白の入れ方も明確にルールが定義してあるんだな。

### コメント集読む
- yield generatorを使う方法もある
  - https://discord.com/channels/1084280443945353267/1235829049511903273/1246118347863621652
    - 列ごとに見ていくやり方
    - 関所の例：https://github.com/nittoco/leetcode/pull/33/changes#r1705956329
    - 計算量を求めるのが難しい。。。O(k^2)という理解であってるのかしら。。。
      - 列ごとに関所があるイメージ
      - 関所を全て出る（=出力される）までにindex2分関所をくぐる(yeildされる)
      - > index2 が大きい数字は、出力までに index2 回 yield されますね。
        だから、ここに自乗が付きます。
      - 「自乗」と言っているのは、1+2+3+...+k = k(k+1)/2 →O(k^2) だからってこと？（理解が怪しい）
  - https://discord.com/channels/1084280443945353267/1235829049511903273/1246303084435607682
    - マージソート的な発想
    - 列（num2）を基準に小さい方（左側）、大きい方（右側）に分けて、それぞれで小さい順にペアを生成するジェネレーターを作る
    - それぞれのジェネレーターから次のペアを取ってきて、和が小さい方を結果に追加していく
    - 左側の列数分は右側のいかなるペアよりも小さいので、右側との比較が不要
    - kが小さい場合は特に有効か
- https://discord.com/channels/1084280443945353267/1201211204547383386/1206515949579145216
  - 意図しない使われ方をした時も、使い手の気持ちを考える。
  - > そこで、「約束にない間違った使い方をしているのだから、そいつが悪い。驚くような動作をして、デバッグで苦労していても、私の問題ではない。」というのは好まれる態度ではないでしょう。
- https://github.com/TORUS0818/leetcode/pull/12/changes#diff-12341a70069caa7ec44aba610c42a0123605c2680c11a88728158764788bead7R239-R260
  - > 意図と操作の距離が遠すぎるんですね。こういうときは関数を間に挟むと意図と操作が分離できます。
  - なるほど、関数の役割にはこういうものもあるのか
  - 今まで、なんとなく複雑なコードは関数に分割してたけど、言語化すると、「意図と操作」の分離をしたかっただけなのか。
- https://github.com/Yoshiki-Iwasa/Arai60/pull/9#discussion_r1647019606
  - ヒープを利用する解法の選択肢
    1. 何も考えず右と下を答えの候補としてヒープに追加しようとする。もしすでに候補に入れたものだったらスキップ（=最初のタイミングでどんどん候補を入れるイメージ）
    2. 右を右上がすでに答えの要素として確定している、下を左下がすでに答えの要素として確定している時、それぞれ右・下を答えの候補に追加する（=最後のタイミングでようやく候補を入れるイメージ）
       - setでも管理できるが、next_i/jの配列（各列・行でどこの行・列まで答えの要素に追加して、次どこを答えの候補として取り出すかを管理する配列）でも管理できる
         - next_i/jは、二次元の表で、列・行ごとに答えの要素として確定しているところまでを行・列までマーカーで塗りつぶしていくようなイメージ
    3. 一旦1列目の全ての行を答えの候補として追加する。そして1行目から順番に出していく。
       - 候補を追加していく方向が一方向であるため、ヒープに追加する候補の重複が起きないので、すでに追加した候補の管理は不要
  - ヒープ利用する解法をそれぞれ手元で実装してみる  

1.

```Python3
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        candidates = [(nums1[0] + nums2[0], 0, 0)]
        seen = set([0,0])
        pairs = []

        def add_to_heap_if_necessary(i: int,j: int) -> None:
            if i < len(nums1) and j < len(nums2) and (i, j) not in seen:
                heapq.heappush(candidates, (nums1[i] + nums2[j], i, j))
                seen.add((i,j))

        while candidates and len(pairs) < k:
            _, i, j = heapq.heappop(candidates)
            pairs.append([nums1[i], nums2[j]])
            add_to_heap_if_necessary(i + 1, j)
            add_to_heap_if_necessary(i, j + 1)
        return pairs
```


2-1. set利用
```Python3
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        candidates = [(nums1[0] + nums2[0], 0, 0)]
        pairs = []
        added = set()

        def add_to_heap_if_necessary(i: int,j: int) -> None:
            if i >= len(nums1) or j >= len(nums2):
                return 
            if i == 0 or j == 0 or (i-1, j) in added and (i, j - 1) in added:
                heapq.heappush(candidates, (nums1[i] + nums2[j], i, j))
        
        while candidates and len(pairs) < k:
            _, i, j = heapq.heappop(candidates)
            pairs.append([nums1[i], nums2[j]])
            added.add((i,j))
            add_to_heap_if_necessary(i + 1, j)
            add_to_heap_if_necessary(i, j + 1)
        return pairs
```
2-2. next_i/jの配列利用
- nums1、nums2をそれぞれ行、列として二次元の配列をイメージした命名
  - こういう、実装時の「イメージ」はコメントに書いておいても良いのか気になった
```Python3
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        #  nums1、nums2をそれぞれ行、列として二次元の配列をイメージ
        candidates = [(nums1[0] + nums2[0], 0, 0)]
        next_i_by_column = [0] * len(nums2)
        next_j_by_row = [0] * len(nums1)
        pairs = []

        def add_to_heap_if_necessary(i: int,j: int) -> None:
            if i >= len(nums1) or j >= len(nums2):
                return 
            if i == next_i_by_column[j] and j == next_j_by_row[i]:
                heapq.heappush(candidates, (nums1[i] + nums2[j], i, j))
        
        while candidates and len(pairs) < k:
            _, i, j = heapq.heappop(candidates)
            pairs.append([nums1[i], nums2[j]])
            next_i_by_column[j] += 1 # next_i_by_column[j] = i + 1としても良い
            next_j_by_row[i] += 1 # next_j_by_row[i] = j + 1としても良い
            add_to_heap_if_necessary(i + 1, j)
            add_to_heap_if_necessary(i, j + 1)
        return pairs
```
3 
```Python3
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        candidates = []
        pairs = []
        for i in range(len(nums1)):
            heapq.heappush(candidates, (nums1[i] + nums2[0], i, 0))
        
        while candidates and len(pairs) < k:
            _, i, j = heapq.heappop(candidates)
            pairs.append([nums1[i], nums2[j]])
            if j + 1 < len(nums2):
                heapq.heappush(candidates, (nums1[i] + nums2[j + 1], i, j + 1))
        return pairs
```


## Step3
- next_i/jの配列を使う方法が最終的には良いと思った
  - 最初見た時は一番よくわからなかった。。。
  - コードを読んで、手元で表を書きながら理解を進めていくうちに、無駄がなく、また実際に手でやる時と近いなと感じた

```Python3
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        def generate_candidate(i: int, j: int) -> Tupple[int]:
            return ((nums1[i] + nums2[j], i, j))

        candidates = [generate_candidate(0, 0)]
        pairs = []
        next_i_by_column = [0] * len(nums2)
        next_j_by_row = [0] * len(nums1)

        def add_to_candidates_if_necessary(i: int, j: int) -> None:
            if i >= len(nums1) or j >= len(nums2):
                return
            if i == next_i_by_column[j] and j == next_j_by_row[i]:
                heapq.heappush(candidates, generate_candidate(i, j))

        while candidates and len(pairs) < k:
            _, i, j = heapq.heappop(candidates)
            pairs.append([nums1[i], nums2[j]])
            next_i_by_column[j] += 1
            next_j_by_row[i] += 1
            add_to_candidates_if_necessary(i + 1, j)
            add_to_candidates_if_necessary(i, j + 1)
        return pairs
```

## TODO
- [] yield generatorを使った解法ををより解像度高く理解する