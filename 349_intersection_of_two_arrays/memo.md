# 349. Intersection of Two Arrays

Given two integer arrays nums1 and nums2, return an array of their intersection. Each element in the result must be unique and you may return the result in any order.

Constraints:

1 <= nums1.length, nums2.length <= 1000
0 <= nums1[i], nums2[i] <= 1000

## Step1
- 愚直： nums1を各要素ごとにnums2を操作して、同じ要素があれば、結果の配列に追加する
  - ただ、手作業でやると考えると無駄が多すぎる。。。
- nums1、nums2をソートして両方を見ていく
  - A組、B組のゼッケン番号（重複あり）がかぶるものを調べる感じ
  - A組、B組の人を若い順に横一列に並べさせる（A組が前、B組が後ろ）
  - A組、B組それぞれ二人が左端から見ていって、連携しながら両組に現れるゼッケン番号をレポートに記録する
    - A組の人<B組の人だったら、A組の次の人を見るようにする
    - A組の人==B組の人だったら、その番号がレポートに現れてこなかったらレポートに記載する、その後A組、B組次に進める
    - A組の人>B組の人だったら、B組の次の人を見るようにする
```Python3
class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        sorted_nums1 = sorted(nums1)
        sorted_nums2 = sorted(nums2)
        i = 0
        j = 0
        intersection = set()
        while i < len(sorted_nums1) and j < len(sorted_nums2):
            num1 = sorted_nums1[i]
            num2 = sorted_nums2[j]
            if num1 == num2:
                if num1 not in intersection:
                    intersection.add(num1)
                i += 1
                j += 1
            elif num1 < num2:
                i += 1
            else:
                j += 1
        return list(intersection)
```

- 上記のやり方、同じ番号が続く時、毎回A組とB組の人の番号を比較するのは非効率
  - A組の人==B組の人の時、番号同じ人は全てスキップした方が効率的
  - A組の人!=B組の人でも同様のことができそう
```Python3
class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        def get_next_value_index(nums: List[int], current_index: int) -> int:
            next_index = current_index + 1
            while next_index < len(nums) and nums[current_index] == nums[next_index]:
                next_index += 1
            return next_index

        sorted_nums1 = sorted(nums1)
        sorted_nums2 = sorted(nums2)
        i = 0
        j = 0
        intersection = set()
        while i < len(sorted_nums1) and j < len(sorted_nums2):
            num1 = sorted_nums1[i]
            num2 = sorted_nums2[j]
            if num1 == num2:
                if num1 not in intersection:
                    intersection.add(num1)
                i = get_next_value_index(sorted_nums1, i)
                j = get_next_value_index(sorted_nums2, j)
            elif num1 < num2:
                i = get_next_value_index(sorted_nums1, i)
            else:
                j = get_next_value_index(sorted_nums2, j)
        return list(intersection)
``` 

- 計算量
  - 時間計算量: O(N log N + M log M + (N+M))
  - 空間計算量: O(k + N + M)（kは同じものの数）

## Step2
### 他の人のコードを見る
- https://github.com/dorxyxki/arai60/pull/13
  - setを使った解法
  - intersectionメソッドや & を使う方法
    - 問題的に、これを使う場合は自分でも実装できるように
    - 内部実装
    - https://github.com/python/cpython/blob/c9a5d9aae48a9faa553a5e8137ff1b5e261f6bf6/Objects/setobject.c#L1675-L1755
      - otherがsetの時
        - soとotherの要素数を比較して、要素数小さい方をループで回し（平均計算量・最悪計算量ともにO(min(N, M))、要素数大きい方にあるかどうかチェックする（平均計算量: O(1)、最悪計算量O(max(N, M))）
        - 時間計算量
          - 平均計算量: O(min(N, M))
          - 最悪計算量: O(N * M)
          - https://wiki.python.org/moin/TimeComplexity
      - otherはsetではなくても良い
        - この時はotherをループして（O(M)）、soに要素があるかチェックしていく（平均計算量: O(1)、最悪計算量: O(N)）
          - 時間計算量
            - 平均計算量: O(M)
            - 最悪計算量: O(N * M)
          - so の要素数 << otherの要素数で、積集合部分がとても小さい時は多少パフォーマンスが悪化しそう
            - ↑この場合先頭でotherをsetに直した方が時間計算量は改善するかもしれないが、ハッシュテーブル構築のオーバーヘッドが大きすぎるゆえ、結果的にトータルの実行時間は長くなると推測
            - [GPTにベンチマークとってもらう](set_bench_result.txt)
              - soが2桁くらいだったら、setに直してからintersectionを実施した方が良さそうだった
              - ハッシュテーブル構築のオーバヘッドは大きいものの、その後のintersectionをとるところが一瞬
- https://github.com/kitano-kazuki/leetcode/pull/13
  - 初手から選択肢の幅が広い（3つも挙げている）
- https://github.com/X-XsleepZzz/leetcode/pull/14
  - 引数のリストが予期しない形（ただintersectionとりたいだけなのに、引数のリストがソートされてしまう）に破壊されるので怖い
  - 面接で聞くとしても、破壊しない前提で聞くのが良さそう（「sortメソッドを使うのは、メモリ多少節約できますが、引数のリスト破壊するのはこの関数を利用する人に迷惑なのでやめました」的な？）
    - > 面接だったら、引数のリスト破壊していいか聞いたほうがいいのかな。
    - https://github.com/X-XsleepZzz/leetcode/pull/14/changes#diff-1182cc11bee6cacd4b54d0a5619c78583d5bbcabbeca0eba95b5c016c6f811a0R118
- https://github.com/ksaito0629/leetcode_arai60/pull/12 
  - 空間計算量抑える
    - https://github.com/ksaito0629/leetcode_arai60/pull/12/changes#diff-d5203cc6e5aacffb982faf78b89db4a95cf27c1a9609008c47637168c8642c14R85
    - RDBのHashJoinと同じ（RDBのメモリを大量に利用しないように、小さい方をハッシュテーブルに変換している）
- https://github.com/mamo3gr/arai60/pull/13
- https://github.com/fuga-98/arai60/pull/14
- https://github.com/naoto-iwase/leetcode/pull/13
  - いろんな方法のベンチマークを載せている
    - ハッシュテーブル構築のオーバーヘッドは結構大きい
- https://github.com/hayashi-ay/leetcode/pull/21
  - counting sort: https://github.com/hayashi-ay/leetcode/pull/21/changes#diff-801d96f7c65ed1087c93c1615e70fa43096cfbb3478152533d182c4f72933a40R45

### コメント集
- ポインタでMerge Sort的な解法
  - https://discord.com/channels/1084280443945353267/1183683738635346001/1188897668827730010
- https://discord.com/channels/1084280443945353267/1201211204547383386/1208701087264280596
  - assertを使う形
    - https://github.com/shining-ai/leetcode/pull/13/changes#diff-905995d172002081813d1902714e80f26046be22d5e1dd5196835d28d4ceeedeR21
    - assertはテストコードで使うものだと思っていたが、プロダクションコードでも使うのは一般的なのだろうか？
    - 今回はデバッグ用途（ここで落ちることは想定していない）なので、使ってもいいのか
      - https://stackoverflow.com/questions/76019033/how-to-use-assert-in-python-production-source-code
  - nanの仕様（nan == nan はFalse）
- https://github.com/tarinaihitori/leetcode/pull/13#discussion_r1827026532
  - > merge sort ようなことをする作戦や
    - RDBのMerge Joinか
  - > 片方の値でバイナリサーチをする作戦などがあるでしょう
    - リストで二重ループ（RDBでNested Loop Joinで、内部表でインデックスを効かせる形か）
- https://discord.com/channels/1084280443945353267/1336510702742929499/1341607151218593904
  - > そうですね。この問題は問題文自体では終わっていなくて、解けた後に、いくつか追加の条件が出てきて、その下でのアルゴリズムとそれらの pros and cons が要求されると思います。
  - pros/consをGPT利用しつつまとめる（Nはnums1の要素数、Mはnums2の要素数、Kは積集合の重複なしの要素数、ソート=sortedを利用）
    - 1.naiveな実装（二重ループ）
      - 計算量
        - 時間計算量: O(N * M)
        - 空間計算量: O(K)
      - pros
        - 実装がシンプルで、両方とも要素数が少ないならばパフォーマンス面懸念なし
        - メモリ使用量が小さい
      - cons
        - 片方でも大きいとすぐ遅くなる
    - 2.要素数大きい方だけソートしておき、要素数小さい方の各要素に対して要素数大きい方（ソート済み）を二分探索（num2の要素数>nums1の要素数
      - 計算量（nums2の要素数>nums1の要素数とした）
        - 時間計算量: O(M log M + N * log M))
        - 空間計算量: O(M + K)
      - pros
        - 1よりははやい、ソートの部分はネイティブコードが動くのでそこそこ早い
        - 要素数大きい方がソート済みならば、時間計算量をO(N * log M)まで落とせる
      - cons
        - 前処理として要素数が大きい方のソートが必要
        - 要素数が小さい方に重複が多いと、同じ値を何回も二分探索しがち
    - 3.片方をset（ハッシュテーブル）に変換し、もう一方の要素を順に、setにあるかをみていく
      - 計算量
        - 時間計算量: O(N + M)
        - 空間計算量: O(M + K)
      - pros
        - 1よりは早い
        - 問題の前提の重複なしと相性がいい
      - cons
        - ハッシュテーブル構築のオーバーヘッドが気になる
    - 4.マージソート的な解法
      - 計算量
        - 時間計算量: O(M log M + N * log N + (M+N))
        - 空間計算量: O(M + N + K)
      - pros 
        - どちらの要素数も多い時でも安定して早い
        - どちらの要素もソート済みならば、時間計算量をO(M+N)まで落とせる
      - cons
        - 実装がやや複雑化
        - 前処理としてnums1、nums2のソートが必要
  - 実務では、2, 3, 4は要素数によっても実行時間が変わってくるので、計測してみながらどの案を取るかを選択するのが良いか
## Step3
- 色々読んで、RDBのJoinのアルゴリズム（HashJoin / MergeJoin / Nested Loop Join）、クエリオプティマイザの話と繋がりがありそうと思った
  - https://www.cybertec-postgresql.com/en/join-strategies-and-performance-in-postgresql/

```Python3
class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        sorted_nums1 = sorted(nums1)
        sorted_nums2 = sorted(nums2)
        i = 0
        j = 0
        result = set()
        while i < len(sorted_nums1) and j < len(sorted_nums2):
            num1 = sorted_nums1[i]
            num2 = sorted_nums2[j]
            if num1 < num2:
                i += 1
                continue
            elif num1 > num2:
                j += 1
                continue
            result.add(num1)
            while i < len(sorted_nums1) and sorted_nums1[i] == num1:
                i += 1
            while j < len(sorted_nums2) and sorted_nums2[j] == num2:
                j += 1
        return list(result)
```
