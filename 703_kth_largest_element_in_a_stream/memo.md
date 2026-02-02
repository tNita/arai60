# 703 Kth Largest Element in a Stream

You are part of a university admissions office and need to keep track of the kth highest test score from applicants in real-time. This helps to determine cut-off marks for interviews and admissions dynamically as new applicants submit their scores.

You are tasked to implement a class which, for a given integer k, maintains a stream of test scores and continuously returns the kth highest test score after a new score has been submitted. More specifically, we are looking for the kth highest score in the sorted list of all scores.

Implement the KthLargest class:

KthLargest(int k, int[] nums) Initializes the object with the integer k and the stream of test scores nums.
int add(int val) Adds a new test score val to the stream and returns the element representing the kth largest element in the pool of test scores so far.


制約

- 0 <= nums.length <= 10^4
- 1 <= k <= nums.length + 1
- -10^4 <= nums[i] <= 10^4
- -10^4 <= val <= 10^4
- At most 10^4 calls will be made to add.

## Step1


- 手作業
    - 点数配列を降順でソートして、1~k番目までの点数配列を持っておく
    - 二分探索でvalが入るところを探す
        - 1~k番目でvalが入るところがある→そのまま入れて最後の要素（一番点低い）を追い出す
        - valが入るところがない→そのままスルー
- そもそも配列を1~k番目までに限定せずに実装できそう
    - もちろんk番目までに限定すれば、制約 `1 <= k <= nums.length + 1` からソート済みの点数配列のメモリ使用量を平均1/2に抑えられる
    - ただ、k番目までに限定すれば点数を追加する時にk+1番目を配列から除外する処理が必要
- 二分探索は標準ライブラリがあるのでそちらを使う（https://docs.python.org/3/library/bisect.html）
    - ただし、昇順でソートされた配列にしか適用できないので、昇順で点数配列を持っておき、後ろからk番目を答えとする必要あり
        - https://github.com/python/cpython/issues/87466
        - （脱線：てかこのイシューをあげている人、提案の幅が広いな。これが専門家の選択肢の幅の広さなのかな）
    - 挿入位置を探すだけではなく、そのまま挿入してしまって良さそう
    - 今回は点数が同じものは区別しないので、`insort_left`、`insort_right`どちらを使っても良さそう
- 後ろからk番目
    - （点数追加後の配列の長さ） - k
    - 点数追加後の配列の長さは nums.length + 1以上であるので、1 <= k <= nums.length + 1であれば問題なさそう

```Python3
from bisect import insort_left

class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        if k < 0 or k > len(nums) + 1:
            raise ValueError("kは0以上nums.length + 1以下である必要があります。k={k}")
        self.nums = sorted(nums)
        self.k = k
        
    def add(self, val: int) -> int:
        insort_left(self.nums, val)
        upper_kth_index = len(self.nums) - self.k
        return self.nums[upper_kth_index]
```

- 計算量
    - init:
        - 時間計算量：O(nlogn)
        - 空間計算量: O(n)
    - add:
        - 時間計算量：O(n)
        - 空間計算量: O(1)

- 実行時間に制約あるならば、addの時間計算量を小さくできた方がいいかもと思ったが、解法思い付かず。。。

## Step2

- 二分探索、自前で実装してみる
    - 途中混乱してしまった。。。
    - 自分なりに整理して一応書いたがpassしなかった（無限ループ）→コメント集の二分探索の箇所を読んで理解してから解き直す
```Python3
class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        if k < 0 or k > len(nums) + 1:
            raise ValueError("kは0以上nums.length + 1以下である必要があります。k={k}")
        self.k = k
        # k個以下の上位点数の配列
        self.kth_largest_nums = sorted(nums)[-k:]
        
    def add(self, val: int) -> int:
        self._my_insort_left(val)
        # 配列の要素数がk+1になってしまっていたら先頭（最も低い点数）の要素を削除
        if len(self.kth_largest_nums) == self.k + 1:
            del self.kth_largest_nums[0]
        return self.kth_largest_nums[0]

    # _my_insort_leftのleft= valと同じ要素があった時に「左端」に挿入
    # やること
    #  valと同じ要素があった時は左端の要素のindexを特定しそこにinsert
    #  valと同じ要素がない時はvalより大きい最小要素のindexを特定しそこにinsert
    # 手作業：
    #   左端、右端に一人ずつ配置して欲しいindexがありうる範囲を縮めていく
    #   左端、右端の人が出会ったらそこが答え
    def _my_insort_left(self, val) -> None:
        # 探索左端
        left = 0
        # 探索右端
        right = len(self.kth_largest_nums) - 1
        # 真ん中
        mid = (left + right) // 2
        while left < right:
            mid_val = self.kth_largest_nums[mid]
            if mid_val >= val:
                right = mid # mid以下に見つけたいindexがある
            else:
                left = mid + 1 # mid+1以上に見つけたいindexがある
        self.kth_largest_nums.insert(left, val)
```
- 後から見返すと、right=midにしているところでrightが単調減少せずに無限ループを起こしうる原因になっていた

- コメント集読む
    - https://discord.com/channels/1084280443945353267/1252267683731345438/1253724345369624596
        - 二分探索にもいろんな種類がある
    - https://github.com/yamashita-ki/codingTest/pull/13/changes/BASE..dd6fab41a3cf9c95d06ffa7a05a6a9c0744d43a6#r2396353508
        - コードを書く前に問題設定を明確にする。（何を探したいのか）
    - https://discord.com/channels/1084280443945353267/1245404801177616394/1308062891609428028
    - https://github.com/yamashita-ki/codingTest/pull/13#discussion_r2396399509
        - まずは何を探すのかをはっきりさせる
        - その上で必要な手段を決める
            - left、rightはなんなのか
            - 探索中に守られる不変条件はなにか
            - 終了時はどうなっているか
            - きちんと有限回で終了するか→
- _my_insort_leftの解き直し
    - やること：kth_largest_numsにソート順を保ったままvalを挿入
    - val以上の最小の要素の位置（これが複数あるときは一番左）を特定し、その直前にvalを挿入
        - val未満の最大要素の位置を特定してその直後にvalを挿入する方法も考えたが、list.insert(i, x)がiの直前にxに挿入する仕様であり、相性の良さを考慮しこの方法を選択
    - 方法: 二分探索にて
        - 初期：val以上の最小要素の位置はわからない→わからないので候補は末尾+1
        - 二分探索する
            - left, rightについて
                - [0, left)にはval以上の要素はない
                - (right, last]にはval以上の最大要素がありright+1がval以上の最小要素の候補
                - [left, right]にはval以上の要素があるかもしれない
            - middleの値がval未満であるとき：[left, middle]にはval以上最小要素がないので次のイテレーションで[middle+1, right]を調査
            - middleの値がval以上の時：middleを一旦候補として保存し、次のイテレーションで[left, middle-1]を調査
    - middleを候補として一旦保存する方法はGPTの助けを得て着想
    - val以上の最小の要素の位置の候補を右からずらしていくイメージか。

```Python3
class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        if k < 0 or k > len(nums) + 1:
            raise ValueError("kは0以上nums.length + 1以下である必要があります。k={k}")
        self.k = k
        # k個以下の上位点数の配列
        self.kth_largest_nums = sorted(nums)[-k:]
        
    def add(self, val: int) -> int:
        self._my_insort_left(val)
        # 配列の要素数がk+1になってしまっていたら先頭（最も低い点数）の要素を削除
        if len(self.kth_largest_nums) == self.k + 1:
            del self.kth_largest_nums[0]
        return self.kth_largest_nums[0]

    # valをkth_largest_numsにソートされた状態を保ったまま挿入
    def _my_insort_left(self, val) -> None:
        left = 0
        right = len(self.kth_largest_nums) - 1
        max_val_lt_val = right + 1
        while left <= right:
            middle = (left + right) // 2
            if self.kth_largest_nums[middle] < val:
                left = middle + 1
            else:
                max_val_lt_val = middle
                right = middle - 1
        self.kth_largest_nums.insert(max_val_lt_val, val)
```

### 他の人のPR見る
- https://github.com/hayashi-ay/leetcode/pull/54
    - heapを使うと計算量小さくできた（logk）
    - > insort割と早い。Heapとそこまで変わらない（普通にappendするより5倍くらい速い）
        - 確かに実行時間見ると異様に早い（9msくらい）のが気になったが、ネイティブコードが動くからなのか
        - 定数倍が重要な例
    - insortの場合は del self.nums[k:]で長さk以上を捨てるのも手
    - 最後からk番目→ `self.nums[-self.k]` でアクセス可能
    - https://github.com/ichika0615/arai60/pull/8/files#r1898337850
        - >  add() 1 回あたりの時間計算量は O(n log n) で、最大で 104 回呼ばれます。よって 10^4 * log 10^4 * 10^4 = 1.5 * 10^9 ステップくらいになると思います。 Python は 1 秒に 100 万ステップ = 1.0 * 10^6 ステップ程度処理できますので、 1.5 * 10^9 / 10^6 = 1.5 * 10^3 = 1500 秒程度かかる
- https://github.com/xbam326/leetcode/pull/10
    - init:heapify→trim、add: pushしてtrimと個人的にシンプルでいいなと感じた
    - https://github.com/xbam326/leetcode/pull/10/changes#r2679314757
        - 関数を切り出す粒度、trimという切り口で切り出すの良さげ
- https://github.com/docto-rin/leetcode/pull/8
    - https://github.com/docto-rin/leetcode/pull/8/files#diff-7cc49926a76cf0dcdcce4baa67d2f64e35b83ab2e3a1868b4b2fef1e035e3381R66-R72
    - heap作る時、ひとつづつheapにpushして、個数がkを超えていたらpopするのではなく、最初のk個でheapを作る、k個以降はpushpopで
    - 個数がk個以上だったら〜という分岐が減って好き
- https://github.com/mamo3gr/arai60/pull/8
    - addする時にwhileで取り除く
    - ここで取り除かれるのは1つだけなのでループにするのは違和感がある（けど、明確なデメリットないし好みの範囲かな？）
        - self.top_k_ascendingの要素数は高々k+1という決まりがあるかないかの違いか
        - 決まりがあるならばif、決まりがないならばwhileというかたちで、一貫したコーディングができていればOK？
```Python3
while len(self.top_k_ascending) > self.k:
    heapq.heappop(self.top_k_ascending)
```
- https://github.com/Yuto729/LeetCode_arai60/pull/14
    - 二分探索的に挿入位置を探すロジックを自前で書くパターン

### コメント集見る
- https://discord.com/channels/1084280443945353267/1201211204547383386/1203365833099972628
    - > 単に init で add を呼んでしまったほうが見通しがいいです。
- heapの実装について
    - https://github.com/Ryotaro25/leetcode_first60/pull/9/files#diff-acd0c668a878606e93a357625d52e84c2f6fd8206191daf0aa1043e4401a7be8R63-R74
        - 自分もheap.pyに実装してみる
    - https://github.com/python/cpython/blob/a8e93d3dca086896e668b88b6c5450eaf644c0e7/Lib/heapq.py
        - 標準ライブラリ
            - shiftup: 子を「up」
            - shiftdown: 親を「down」
        - shiftupでは一旦対象要素を葉まで下げてからshiftdownして適切な位置まであげる形で実装
            - popする時、根に大きい要素が来るので、根から順に比較して下げていっても結局葉付近に来てしまう→であれば一旦葉まで下げてしまってあげた方が良さそうということか
            - Knuth Volume 3 でこちらの方が示されているらしい
                - Knuth Volume3とは[『The Art of Computer Programming』](https://ja.wikipedia.org/wiki/The_Art_of_Computer_Programming)の３章ことかな
                - 有名な本らしい（専門家の常識の範囲？）
- https://github.com/katataku/leetcode/pull/8#discussion_r1856437996
    - 自分の実装ではコンストラクタでkのバリデーションはしていたものの、理由や背景（使い道）まで考えれていなかった
    - https://github.com/TrsmYsk/leetcode/pull/10/changes#diff-d72c252032c4f27b8e0389326f620bdf20ff4e75d11f1ac0b0254867cc156dc0R46
        - > 入学試験の合格者の管理が目的なら間違ったまま動き続けるよりは止まってくれた方がよさそう。
        - 例えばこんな感じか。

## Step3


```Python3
class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        if k < 0 or k > len(nums) + 1:
            raise ValueError(f"kは0以上{len(nums) -1}以下である必要があります")
        self.k = k
        self.kth_largest_nums = []
        for n in nums:
            self.add(n)

    def add(self, val: int) -> int:
        heapq.heappush(self.kth_largest_nums, val)
        if len(self.kth_largest_nums) == self.k + 1:
            heapq.heappop(self.kth_largest_nums)
        return self.kth_largest_nums[0]
```
