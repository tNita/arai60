# 1. Two Sum

## 問題

Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.
You can return the answer in any order.

https://leetcode.com/problems/two-sum/description/



## STEP1

- 二重ループによるナイーブな解法だとO(n^2)
- nums[i] が決まればnums[j]がとるべき値は一意に定まる（target - nums[i]）
- numsの要素をキー、インデックスをバリューとした辞書型を使えばO(1)で存在するかどうかを確認できる→そうすれば全体としてはO(n)
- 同じ要素を2回使うことはできないので、nums[j]が見つかった場合も答えとしてreturnする前にi!=jをチェックすること
- 正解はひとつのみという制約により、答えが見つかればすぐにreturnしてよい
- numsに重複要素がある場合は破綻するのでは？
    - 結論：No
    - 正解が一つのみという制約があるので、重複要素をd、そのほかをoとすると
        - 答えが[d, o]→複数組が答えになりあり得ない
        - 答えが[d, d]→一つのみなのでdはnumsに二つしかない、dのうちどちらか一つは辞書に現れるので正解を導き出せる
    - ただ、正解が一つのみという制約に依存した解法でありHACK的な感じがする



## STEP2

### 辞書（hash）
- jValueは補数（complement）と命名すればよさそう
- 辞書の名前はnum_to_indexがわかりやすい
- 辞書でやる場合、numsをループする時に合わせてdictも作るようにすればループが一回で済む
    - 最初に空の辞書を宣言
    - numsをループ(i, num)
        - complementを算出
        - complementをキーとするものが辞書にあれば答え
        - なければ{num: i}を辞書に追加
    - 重複問題はSTEP1の解法と同様、正解が一つのみという制約があるので気にしなくて良い
    - また同じ要素かどうかの判定も不要
- Pythonではスネークケースで記述するのが一般的とされているが、普段JavaやKotlinを扱っているため、ついキャメルケースで書いてしまっている
    - https://peps.python.org/pep-0008/#function-and-variable-names
    - https://www.oracle.com/java/technologies/javase/codeconventions-namingconventions.html
- 計算量
    - 時間計算量: O(n)
    - 空間計算量: O(n)


### ソート+2ポインタ法
- (index, value)のタプルのリストに変換、value基準で昇順で並べ替え（O(nlogn)して、left=0, right=len(nums)-1から2ポインタ法試す
    - sorted関数を使う方法とsortメソッドを使うがあるらしいが、sortの方が若干効率的だが副作用出す。
    - ソート前のリストは不要なのでsortを使った（ただ、副作用は予期しないバグを及ぼすので、たとえ今はソート前のリストが不要だとしても副作用は避けた方が良い？）
    - https://docs.python.org/ja/3/howto/sorting.html
- 計算量
    - 時間計算量: O(nlogn)
    - 空間計算量: O(n)

### ソート+二分探索利用
- (value, index)のタプルのリストに変換、value基準で昇順で並べ替え（O(nlogn)
- valueのみの昇順の配列を作っておく
- このリストをループ
    - target - nums[i]となるものを二分探索で特定（[i+1, len(n)-1]で探索）
- bisectを利用
    - https://docs.python.org/ja/3.13/library/bisect.html#bisect.bisect_left
    - [lo, hi)で挿入すべきjを返す。
    - 別途存在確認必要
- 計算量
    - 時間計算量: O(nlogn)
    - 空間計算量: O(n)

### ナイーブ
- とりあえず実装してみた
- Pythonのリストは内部的には配列なんだ
    - https://wiki.python.org/moin/TimeComplexity
- 計算量
    - 時間計算量: O(n^2)
    - 空間計算量: O(1)


### STEP3
- 3回連続通せるようになった
