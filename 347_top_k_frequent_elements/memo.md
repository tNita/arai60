# 347. Top K Frequent Elements


Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.


Constraints:

1 <= nums.length <= 105
-104 <= nums[i] <= 104
k is in the range [1, the number of unique elements in the array].
It is guaranteed that the answer is unique.
 

Follow up: Your algorithm's time complexity must be better than O(n log n), where n is the array's size.


## Step1
- 愚直に手作業で
    - 要素とその出現回数をメモ
    - 出現回数順にソートして上からk個を返す

```Python3
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        occurrences = {}
        for num in nums:
            if num in occurrences:
                occurrences[num] += 1
            else:
                occurrences[num] = 1
        topk_occurrences = sorted(occurrences.items(), key=lambda x:x[1], reverse=True)[:k]
        return [num for num, frequency in topk_occurrences]
```

- 時間計算量: O(nlogn)、空間計算量O(n)
- 時間計算量をO(nlogn)より小さくできないか？
    - kは小さいことが多いならばheapq.nlargestを使える？
        - https://docs.python.org/3/library/heapq.html#heapq.nlargest
        - > The latter two functions perform best for smaller values of n. For larger values, it is more efficient to use the sorted() function.
        - 時間計算量はO(nlogk)
            - https://stackoverflow.com/questions/23038756/what-is-the-time-complexity-of-heapq-nlargest

```
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        occurrences = {}
        for num in nums:
            if num in occurrences:
                occurrences[num] += 1
            else:
                occurrences[num] = 1
        topk_occurrences = heapq.nlargest(k, occurrences.items(), key=lambda x:x[1])
        return [num for num, frequency in topk_occurrences]
```

## Step2

- https://github.com/TrsmYsk/leetcode/pull/11/changes#diff-cc847b434ca1353106944eaf84e5666ec1319df7e7ca0d864adf5f260cd48035R16-R19
    - 発想の仕方
    - > - 発想: 選挙の開票
    - >    - ある団体で新たにk人の理事を選出するために団体の構成員全員を投票者かつ候補者とする選挙が行われた。私はこの選挙の開票作業を担当する。
    - 実世界で起こりうる具体的な場面を設定してやるとより発想しやすくなりそう
    - 確かにodaさんも電車を本線に送る話、部屋の中で数字を数字を数字を探す話など具体的な例を挙げられていた
    - > 身体性を持った考え方みたいなのがある気がしています。
    - https://discord.com/channels/1084280443945353267/1237649827240742942/1249892025948573706
- https://github.com/TrsmYsk/leetcode/pull/11/changes#diff-cc847b434ca1353106944eaf84e5666ec1319df7e7ca0d864adf5f260cd48035R22
    - Counter オブジェクトに出現回数のカウントを任せられる
    - https://docs.python.org/3.14/library/collections.html#collections.Counter.most_common
    - most_commonを使えば今回のやりたいことができる
- https://github.com/TrsmYsk/leetcode/pull/11/changes#r2752795074
    - `defaultdict(int)` を使うとよりシンプルにかける（辞書に該当キーがない場合も `int()` を呼び出して値を生成してそのキーと値を辞書に追加）
    - 出てきた数字がすでにカウントされているものか未だカウントされていないものかのチェックが不要になる
    - https://docs.python.org/ja/3.6/library/collections.html#collections.defaultdict
- https://github.com/fuga-98/arai60/pull/10#discussion_r1967591652
    - > sorted(num_count, key=num_count.get, reverse=True) で、key だけが並んでくれるでしょう。
    - https://docs.python.org/3.11/library/stdtypes.html#dict
    - iter(dict)でキーだけ返す。
    - > Return an iterator over the keys of the dictionary. This is a shortcut for iter(d.keys()).
- https://github.com/potrue/leetcode/pull/9/changes#diff-dce85bf5bc3acb0f755f06a75043875e90f52eadc5e761421acc856335cfec86R55
    - bucket sortを使う方法
- https://github.com/olsen-blue/Arai60/pull/9#discussion_r1905335335
    - heapqよりもsortの方が早い
        - 計算量よりも定数倍が大事ないい例
        - sortedはネイティブコードが動く
- https://github.com/TORUS0818/leetcode/blob/347/medium/347/answer.md
    - Quick Select
        - Quick Sortが元になっている。
    - countをマイナスにしているのが少し気になるが、好みの範囲か。
    - 個人的にはcountはマイナスせずに降順でquick selectする方が素直で好き
```
pairs_of_num_and_minus_count = [
    (num, -count) for num, count in Counter(nums).items()
]
return [num for num, _ in quick_select(pairs_of_num_and_minus_count, k)]
```
    - k番目までselectしたいから `len(array) < k` ではなく `len(array) <= k:` の方が良さげ
        - `len(array) < k` とした場合、`len(array) = k` の時は `if k <= len(smaller_than_pivot) + len(equal_to_pivot):`の分岐に入り、実質array全体を返すので問題はない。
```
if len(array) < k:
    return array
```
- https://github.com/mamo3gr/arai60/pull/9/changes#diff-a37074479894b4877931e1e7e4c928bd1569960d52976092e863130125fa8856R11
    - 辞書型はgetでキーを取得できる。こちらの方は該当キーがない時にはNoneが返るので、存在しないキーにもアクセスするようなコードを書くならばdict[key]ではなくdict.get(key)の書き方が良いかも
    - https://docs.python.org/3/howto/sorting.html?utm_source=chatgpt.com#operator-module-functions-and-partial-function-evaluation
- https://github.com/Hiroto-Iizuka/coding_practice/pull/9/changes#r2658894461
    - most_commonの実装：https://github.com/python/cpython/blob/6d05e55de0f9c0b07fb14b4d2b9cf9c8eee2042c/Lib/collections/__init__.py#L625-L640
        - most_commonの引数n（ n most commont element ） が指定された時は`heapq.nlargest`、nが指定されていない時には `sorted` を利用している
        - なぜ？（出現種類数をmとする）
            - nが指定されていない：`heapq.nlargest` も `sorted` もO(mlogm)だが、後者はネイティブコードが動き早いので後者を用いる
            - nが指定されている：`heapq.nlargest` はO(mlogn)であり、`n<<m` ならば`heapq.nlargest`の方が早いのでこちらを用いる
        - この実装はユースケース的に `n<<m`であることが多いだろうという前提に基づいている？
        - top 10 words、top 10 errorsなど、大量データの中からtop 数件を絞りたいケースに適していそう
- `heapq.nlargest`の実装：https://github.com/python/cpython/blob/main/Lib/heapq.py#L411-L475
    - `k<<n` の前提での比較をすると、O(nlogk)でnより僅かに大きくなるだけなので効率的
    - この問題には `k<<n` は書いていないので、この関数がどういうケースで使われるのかを会話して、もし `k<<n`ならばこの方法を使うのが良いか。
    - https://code.activestate.com/recipes/577573-compare-algorithms-for-heapqsmallest
        - 様々な方法の比較：このくらい幅広い選択肢を見れるようになりたい
    - https://github.com/python/cpython/blob/main/Lib/heapq.py#L428-L475
        - comparisons = n + k * (log₂k · log(n/k) + log₂k + log(n/k))
        - `k<<n` ならば comparisons≈n

- https://discord.com/channels/1084280443945353267/1183683738635346001/1185972070165782688
    - > クイックソートについて知っていなくてはいけないことは
    - > 最悪・平均計算量
        - 最悪: O(n^2): ソート済みの配列で端を選ぶ場合などで発生。
        - 平均: O(nlogn)
    - > 末尾再帰最適化
        - スタックオーバーフローを避けるためにコンパイラがやってくれる
        - pivotを基準に2分割した場合、右半分は再帰ではなくループにしてくれる
    - > ピボット選択
        - 端を選ぶと危ない
        - ランダムや中央値などが良い
        - median of medianとかある。
    - > マージソートとのプロコン
        - pros
            - クイックソートはin-placeのソートなので空間計算量O(n)のマージソートよりメモリ使用量は小さい
            - 実用面ではクイックソートの方が早いことが多いらしい
                - https://stackoverflow.com/questions/70402/why-is-quicksort-better-than-mergesort
                - クイックソートはin-placeのソートなのでアクセスするデータが局所的→PUのキャッシュに乗りやすくて早い？（理解怪しい）
        - cons
            - クイックソートは最悪計算量がO(n^2)な一方、マージソートは最悪計算量がO(nlogn)
    - アルゴリズムイントロダクションに上記は書いてある
        - ざっと読んでみて概要はつかんだが、証明までは理解しきれていない
    - https://github.com/naoto-iwase/leetcode/pull/9/changes#diff-2d1f664c4bc1102fa070db0b0b8329b974594503435ab3437b253c140ebb78f1R127
        - クイックソート常識まとめ
- https://discord.com/channels/1084280443945353267/1227073733844406343/1231268645628416020
    - > 常に Top K Frequency をモニタリングし続けるというストリーミングアルゴリズムとして解くことも可能
    - ストリーミングであれば、LFUでも書ける
        - LFUの場合は、hash mapで平衡木のノードへのリンクを張り、平衡木で出現回数を管理
    - （脱線） LRUの場合
        - hash map + doubly liked list OR hash map + 平衡木
        - 更新時の時間計算量的には前者の方が良いという理解で合ってますか？（質問）
            - 前者は削除、挿入にO(1)
            - 後者は削除、挿入、再平衡の時間計算量がO(logn)
- https://discord.com/channels/1084280443945353267/1337642831824814192/1371893051823358046
    - https://docs.python.org/3/library/operator.html#operator.itemgetter
    - sortedのkeyに渡す関数 `lambda x:x[1]` は`itemgetter`でも書ける

## Step3

```Python3
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        num_count = defaultdict(int)
        for num in nums:
            num_count[num] += 1
        return sorted(num_count, key=num_count.get, reverse=True)[:k]
```

