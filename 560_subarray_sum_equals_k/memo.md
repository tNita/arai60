# 560. Subarray Sum Equals K

Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k.

A subarray is a contiguous non-empty sequence of elements within an array.


Constraints:

- 1 <= nums.length <= 2 * 10^4
- -1000 <= nums[i] <= 1000
- -10^7 <= k <= 10^7

## Step1

ナイーブな実装
- 先頭から順にループ見ていく
  - ループの対象要素が先頭の先頭の部分配列を考える
  - 和がkだったら和がkのカウントを1増やす
- 時間計算量がO(n^3)
- 配列の要素数が2 * 10^44になりうるので、まずは毎回sumをとっているところ効率化したい（ただ、ネイティブコードが動くので早く、実行速度が大幅に改善することはないか？）
```Python3
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        k_count = 0
        for i in range(len(nums)):
            j = i
            while j < len(nums):
                if sum(nums[i: j + 1]) == k:
                    k_count += 1
                j += 1
        return k_count
```
- 実際TLE

- 毎回sumは撮らないようにする
- 時間計算量はO(n^2)にできそうだが、ネイティブコードが動くところを削っただけで大幅に早くなることはないか？
```Python3
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        k_count = 0
        for i in range(len(nums)):
            j = i
            total = 0
            while j < len(nums):
                total += nums[j]
                if total == k:
                    k_count += 1
                j += 1
        return k_count
```
- 実際TLE
- ただ、上の実装ではTLEになっているけど、この実装ではTLEにならないテストケースがあり、若干の速度改善はできていそう
- そもそも解き方を変えた方が良いと思って考えたが、思いつかず。。。

## Step2
### 他の人のコード
- https://github.com/hayashi-ay/leetcode/pull/31
  - cppだったら愚直な方法（Step1の２番目の解法と同じ）でもOK
    - https://github.com/hayashi-ay/leetcode/pull/31/changes#diff-302b3c57a99f55a6ede5338b83f17a5d903d52dbeddd3fe485ae5f5d1cdc4badR21-R40
  - 一個前の要素が終端になる部分配列と今の要素が終端になる部分配列それぞれで、和ごとの部分配列の数を管理するdictを用意してとく

```Python3
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # 一個前の要素が終端になる部分配列で、和ごとの部分配列の数を集計
        prev_sums = defaultdict(int)
        ans = 0
        for num in nums:
            # この要素が終端になる部分配列で、和ごとの部分配列の数を集計
            current_sums = defaultdict(int)
            # prevを含んだ形
            for total in prev_sums:
                current_sums[total + num] += prev_sums[total]
            # num単体の部分配列
            current_sums[num] += 1
            ans += current_sums[k]
            prev_sums = current_sums
        return ans
```

- 累積和を使う方法もあるらしい
  - hayashi-ayさん以外のPRも読んでみたが理解できない
  - 一旦discordなど漁ってみる

### 累積和の理解（コメント集を軸にdiscordを読む）

https://discord.com/channels/1084280443945353267/1233603535862628432/1252232545056063548
- 標高差がkの区間を列挙すると問題を読み替える

- 自分でも実装してみる
  - 88 / 93 testcases passed
  - 一部Memory Limited Exceeded

実装1
```Python3
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        cumulative_sum_to_indexes = defaultdict(list)
        cumulative_sum = 0
        sum_k_pairs = []
        for i, num in enumerate(nums):
            cumulative_sum += num
            # 先頭から
            if cumulative_sum == k:
                sum_k_pairs.append((0,i))
            # 途中から
            # S_i - S_j = k となるjがあれば[j+1, i]の和がkである（ただし、S_は[0,i]の和で、j<i）
            # S_j = S_i - k だから、S_i - k となる和の位置が知れれば良い
            for j in cumulative_sum_to_indexes[cumulative_sum - k]:
                sum_k_pairs.append((j+1, i))
            cumulative_sum_to_indexes[cumulative_sum].append(i)
        return len(sum_k_pairs)
```
- 実装1を番兵を使ってシンプルに
  - `# 先頭から`の分岐は 仮想的に -1 番目までの累積和は0としておけば、`# 途中から` に統一できる
実装2
```Python3
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        cumulative_sum_to_indexes = defaultdict(list)
        cumulative_sum_to_indexes[0].append(-1)
        cumulative_sum = 0
        sum_k_pairs = []
        for i, num in enumerate(nums):
            cumulative_sum += num
            for j in cumulative_sum_to_indexes[cumulative_sum - k]:
                sum_k_pairs.append((j+1, i))
            cumulative_sum_to_indexes[cumulative_sum].append(i)
        return len(sum_k_pairs)
```

- https://discord.com/channels/1084280443945353267/1195700948786491403/1253847901969580082
  - > これは自明な書き換えに見えますか?
  - ここと同様に書き換えてみる
- 実装2をシンプルに：欲しいのは和がkである区間の数なので、和がkの区間を具体的に記録する必要なし

実装3
```Python3
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        cumulative_sum_to_indexes = defaultdict(list)
        cumulative_sum_to_indexes[0].append(-1)
        cumulative_sum = 0
        sum_k_count = 0
        for i, num in enumerate(nums):
            cumulative_sum += num
            sum_k_count += len(cumulative_sum_to_indexes[cumulative_sum - k])
            cumulative_sum_to_indexes[cumulative_sum].append(i)
        return sum_k_count
```
- 実装3をシンプルに：和がkである区間の数を求めるのに、累積話の具体的な位置は記録する必要なし、累積和の和ごとの位置の数を記録すれば十分

実装4
```Python3
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        cumulative_sum_to_indexes = defaultdict(int)
        cumulative_sum_to_indexes[0] += 1
        cumulative_sum = 0
        sum_k_count = 0
        for i, num in enumerate(nums):
            cumulative_sum += num
            sum_k_count += cumulative_sum_to_indexes[cumulative_sum - k]
            cumulative_sum_to_indexes[cumulative_sum] += 1
        return sum_k_count
```
- 実装1（和がkの区間を列挙する件）から実装4に書き換えてみると、累積和の実装が理解できた
- （一晩考えを寝かした後）標高差を考えた時、標高差kの駅の数→今の標高 - k をみるのは当たり前と理解できた
  - やっぱり、身近な例に置き換えるの大事

https://discord.com/channels/1084280443945353267/1183683738635346001/1192368274705498243
> 累積和の問題を、各駅の隣同士の標高差に変えた。
> 組み合わせの数ではなくて、組み合わせ自体を出力しように変えた。
> どちらも、こう、なんていうか、より確認しやすいものに変えています。

#### その他（discrodを漁る中でなるほどと思ったところをメモ）
https://discord.com/channels/1084280443945353267/1195700948786491403/1254402602666430594
> 別に私もややこしいものを理解するときに、分からないといって腕組をしているわけではなくて、こういうふうに自明な変形を組み合わせて理解しようとしています。
- 自分自身、手を動かすことをサボる癖があるので気をつける

https://discord.com/channels/1084280443945353267/1183683738635346001/1192145962479665304
> なんか、抽象概念を抽象概念のまま処理しようとしているように感じました。


https://discord.com/channels/1084280443945353267/1192736784354918470/1195265633022128168
可読性=（他人が簡単に）読むことができる性質
>  なんか、一番重要なポイント、他人に読みやすいか、じゃないじゃないですか。
> 「浅はかな理解で書かない」とか「息も絶え絶えに到達しない」とかそういうイメージですね。
https://discord.com/channels/1084280443945353267/1200089668901937312/1207200647594639391
> そういうことを考えながら頭の中で走らせています。だから、ワーキングメモリーをさっさと開放してあげることが大事です。

https://discord.com/channels/1084280443945353267/1206101582861697046/1208414507735453747

> 一番最悪なのは、かっこいい公式が思いつかないかを、ぼーっと眺めていることです。たとえば、10時間一つの問題を考えることは悪いことではないですが、この問題の複雑さで10時間考えているということは、そもそも何かを間違っている可能性が高いです。
> 
> それで、15分くらいで切って次に行ったほうがいいだろうと私は判断しています。
> 15分の使い方として、「かっこいい公式を連想してみせよう」とかやっているのは、あまり意味がなくて、とりあえず、いいから手を動かしてくれと思っています。
かっこいい公式を思いついたからそれをどうやって振り回すかを考えている15分もあんまり意味がないという感覚です。
> 
> [-2,1,-3,4,-1,2,1,-5,4]を例に取れば、100回ちょっとも足し算すれば、全通り出せるわけで、とりあえずそれをやってから考えたらどうでしょう。

https://discord.com/channels/1084280443945353267/1200089668901937312/1211191157221097552
> LeetCodeの解法を見てそんな発想はなかったと思いましたが、標高差で考えるとなんか当たり前のことですね。
- イメージしやすい事象に具体的に置き換えると発想しやすい

### 他の人のコード（続き）
- https://github.com/naoto-iwase/leetcode/pull/16
  - https://discord.com/channels/1084280443945353267/1303257587742933024/1322011962598625280
    - sum_counter[0] += 1 をループの先頭へまとめることも可能。
    - ループひとつ前の累積和の数を更新→今の累積和を更新→
- https://github.com/Shunii85/arai60/pull/16
  - https://discord.com/channels/1084280443945353267/1478763507963924522/1485215939602419722
    - > つまり、最初に(0, 1)を追加するというのは、地面(アース)の標高を記録するということだろうか。
    - > そうでないと、道中の標高差しか読み取ることができない。
    - 標高差の例に置き換えると、最初に累積和=0の数を1とするのは腑に落ちる
- https://github.com/tom4649/Coding/pull/15
  - sol1.py
    - 最初に累積和の配列を作っていって、次に累積和の配列を逆順に舐めていく
    - 逆順に舐めていく際、辞書型の変数`needed_prefix_sum_counts`を作って、今いる標高から逆算して標高差kになるための必要な標高をあらかじめメモし、あとでその標高の地点に到達したときに回収するスタイル
- https://github.com/kitano-kazuki/leetcode/pull/16
  - https://github.com/kitano-kazuki/leetcode/pull/16/changes#diff-0c860cd754249868513e4f9054206317fa33d0f548fc3896ac2b3e11822fd852R11
    - > prefix_sumsをあらかじめ用意しておく. 各開始点ごとに, prefix_sumを元に終了点を辞書から探す.
      - まずは標高がkのところを数え→その後標高差（駅間の標高差）がkのところを数える
        - 標高差kを数えるところを二分探索を使って工夫されている

### コメント集（続き）など

- https://github.com/Hurukawa2121/leetcode/pull/16#discussion_r1898332261
  - パフォーマンス不足と言うときは、ちゃんとどういう実害がありうるのかを具体的にする

- https://discord.com/channels/1084280443945353267/1300342682769686600/1357378682163036160
  - > computeIfAbsent や getOrDefault を使うというのもありですが、まず、やりたいこととその表現が遠いと感じます。

## Step3

- 累積和をGoogle 翻訳で翻訳してみるとcumulative sumだが、SWEの常識としては prefix sumなのか
  - https://en.wikipedia.org/wiki/Prefix_sum
  - https://ja.wikipedia.org/wiki/%E7%B4%AF%E7%A9%8D%E5%92%8C

```Python3
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        prefix_sum_to_count = defaultdict(int)
        prefix_sum_to_count[0] = 1
        prefix_sum = 0
        sum_k_subarray_count = 0
        for num in nums:
            prefix_sum += num
            sum_k_subarray_count += prefix_sum_to_count[prefix_sum - k]
            prefix_sum_to_count[prefix_sum] += 1
        return sum_k_subarray_count
```
