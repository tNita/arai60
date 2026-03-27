# 387. First Unique Character in a String

Given a string s, find the first non-repeating character in it and return its index. If it does not exist, return -1.

Constraints:

1 <= s.length <= 105
s consists of only lowercase English letters.

## Step1
案1. 先頭から1文字ずつ確認していく、重複している文字を管理するsetを作る方法
- 対象の文字が重複している文字を管理するsetにない場合、以降左の文字をチェックしていく
- 重複が見つからなければその文字が答えなので位置をreturn
- 重複があれば、重複がある文字としてsetに入れる

- 計算量（出現する文字の種類をk、文字列の長さN） 
  - 時間計算量：O(k * N)
  - 空間計算量：O(k)

```Python3
class Solution:
    def firstUniqChar(self, s: str) -> int:
        duplicate_chars = set()
        for i, char in enumerate(s):
            if char in duplicate_chars:
                continue
            j = i + 1
            while j < len(s) and s[j] != char:
                j += 1
            if j == len(s):
                return i
            duplicate_chars.add(char)
        return -1
```

案2. 先頭から1文字ずつ確認する、文字の出現位置を記録するdictを作る方法
- dictのデータ構造はkeyをアルファベット、valueを出現位置の配列とする
- 一文字ずつ先頭から文字の出現位置を記録
- すべての記録が終わったら、dictの中で、valueの配列の要素数が1でもっとも値が小さいものをreturnする。配列の要素数が1のものがない時は-1をreturn

- 計算量（一回しか出現しない文字の種類数をm、出現する文字の種類の数をk、文字列の長さN）
  - 時間計算量: O(N + k + m log m)
  - 空間計算量: O(k + m)

```Python3
class Solution:
    def firstUniqChar(self, s: str) -> int:
        char_position = defaultdict(list)
        for i, char in enumerate(s):
            char_position[char].append(i)
        
        first_unique_positions = [v[0] for k, v in char_position.items() if len(v) == 1]
        if len(first_unique_positions) == 0:
            return -1
        first_unique_positions.sort()
        return first_unique_positions[0]
```

- 計算量だけ見ると案2が良さそう
- 案1は早期returnが可能なので、文字列sの文字をすべて見る前に処理を終了できるのはメリット
- sの構成文字はある程度ランダムな文字→案1を選択（leetcodeの実行時間も案1の方が短い：案1: 39msec、案2: 59msec）

## Step2
- https://github.com/hayashi-ay/leetcode/pull/28
  - 文字のindex値を利用する（a-zのUnicodeコードポイントは連番であるため、ordを利用して比較的簡単に実装できる） 
  - 文字の出現回数を数えるのにdictを使う方法(自分の案2に類似)
    - v3.7以降から、辞書の順番は挿入順になるため、自分の案2で行っていたソートは不要
      - https://docs.python.org/3/library/stdtypes.html#dict
      - > Changed in version 3.7: Dictionary order is guaranteed to be insertion order.
    - OrderedDictを使っても、辞書の順番は挿入順になる
      - https://docs.python.org/3/library/collections.html#collections.OrderedDict
  - Counterを利用する方法
    - Counterもdictのサブクラスであり、以下の実装より、Counterの順番（forループで回した時の順番）は文字の出現順になる。
    - iterableなオブジェクトをCounterに詰める処理：https://github.com/python/cpython/blob/main/Lib/collections/__init__.py#L540-L544
- https://github.com/naoto-iwase/leetcode/pull/15
  - https://github.com/naoto-iwase/leetcode/pull/15/changes#diff-7edcc4c1426405d421fc29bd0711bf94515bc082deab76160ea42efc9b5324d1R46
    - >  -1が代入される回数をカウントし、それが文字種の数（今回なら26）に達したら早期returnします。
    - なるほど、確かに文字種の上限に到達すれば、それ以上見なくても良い（それ以降はすべて重複要素が確定している）
  - https://github.com/naoto-iwase/leetcode/pull/15/changes#diff-7edcc4c1426405d421fc29bd0711bf94515bc082deab76160ea42efc9b5324d1R86-R115
    - キューを使った解法。キューに出現文字を入れていって、2回以上出現する文字をとっていく
    - 原案（nodaさん） https://github.com/colorbox/leetcode/pull/29/changes#r1861430039
    - iwaseさんの案はnodaさんの改良版で、すでに出現回数が2以上のものはキューには追加しない
- https://github.com/fuga-98/arai60/pull/16
  - 再帰を利用
    - https://github.com/fuga-98/arai60/pull/16/changes#diff-e937677c130f69c922b44f409c0b879d2026e69ef85d7624612be88a2a23697cR50
- https://github.com/kitano-kazuki/leetcode/pull/15
  - https://github.com/kitano-kazuki/leetcode/pull/15/changes#diff-0ec46bd78c96c48cbfa4269694a8b6a78a051cd4e9d07f3a46d355337c9122ecR8
  - sを二回走査すれば文字の出現位置を記憶する必要なし
- https://github.com/tom4649/Coding/pull/14
  - https://github.com/tom4649/Coding/pull/14/changes#diff-41b5bd0609767abf5c9be1810bac807e8eb867b12071851814c42105a001db34R12-R14
    - キューを使う解法で、deque以外にもqueue.Queueが利用できる
    - ただし、peekがない

### コメント集
- https://github.com/colorbox/leetcode/pull/29/changes#r1860892662
  - 文字ごとに(文字種、出現位置)を管理し文字種でソートして文字種ごとに隣接させたうえで、先頭から舐める
- https://discord.com/channels/1084280443945353267/1233603535862628432/1238208008182562927
  - 現実世界に置き換えて発想するば、1回のループで済ませる方法が思いつきそう
  - > 仮に、文字全体が2回流れてくれるんだったら、1回目に2文字以上流れてくる文字を数えて、2回目に、1文字しか流れてこないやつが初めて流れてくる日を確認するという戦法が可能ですね。 
    > では、1回だったとしましょう。 
    > 何を引き継ぎ資料にしますか。
- https://discord.com/channels/1084280443945353267/1233603535862628432/1237823214168576112
  - LinkedHashMapを使う
    - Pythonで: https://discord.com/channels/1084280443945353267/1201211204547383386/1210484389692313610
      - LinkedHashMap#popでhashmapから要素を削除しなくていいのかしら。
  - ハッシュ+要素の挿入順を保持する双方向連結リスト
  - jdkの実装
    - https://github.com/AdoptOpenJDK/openjdk-jdk8u/blob/master/jdk/src/share/classes/java/util/LinkedHashMap.java
      - 追加時、末尾にノードをリンク
      - 削除時、afterNodeRemovalでノードのリンクの外しも行う
    - これを継承: https://github.com/AdoptOpenJDK/openjdk-jdk8u/blob/master/jdk/src/share/classes/java/util/HashMap.java
- https://github.com/t0hsumi/leetcode/pull/15/changes#r1930362913
  - find、rfindを使う
    - 時間計算量はO(n^2)だが、ネイティブコードが動くので早い
      - findの時間計算量はO(1 * n) https://stackoverflow.com/questions/29728969/worst-case-time-complexity-of-str-find-in-python

## Step3
```Python3
class Solution:
    def firstUniqChar(self, s: str) -> int:
        unique_char_poisitions = {}
        duplicate_chars = set()
        for i, char in enumerate(s):
            if char in duplicate_chars:
                continue
            if char in unique_char_poisitions:
                del unique_char_poisitions[char]
                duplicate_chars.add(char)
                continue
            unique_char_poisitions[char] = i
        return next(iter(unique_char_poisitions.values()), -1)
```

