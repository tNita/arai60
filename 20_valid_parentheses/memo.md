# 20. Valid Parentheses

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.


制約：

- 1 <= s.length <= 10^4
- s consists of parentheses only '()[]{}'.

## Step1

```Python3
class Solution:
    PARENTHESES = {
        ")": "(",
        "}": "{",
        "]": "["
    }
    def isValid(self, s: str) -> bool:
        # 制約より、スタックに積む、文字列をループで見れば良さそう
        # 辞書型で、閉じた括弧に対応する開いた括弧を持っとく
        # 一文字ずつチェック
        #  開いた括弧の時→スタックにpush
        #  閉じた括弧の時→スタックからpopして対応する括弧かどうかチェック、対応しない場合はNGとして終了
        # 全ても文字チェックしてスタックに残っていたらNG, 残っていなかったらOKとする
        stack = []
        for c in s:
            # open
            if c not in self.PARENTHESES:
                stack.append(c)
                continue
            # close
            if len(stack) == 0:
                return False
            prev = stack.pop()
            if prev != self.PARENTHESES[c]:
                return False
        return len(stack) == 0
```

- 計算量
    - 時間計算量 O(n)
    - 空間計算量 O(n)

- 
## Step2

- https://github.com/bumbuboon/Leetcode/pull/7/files#r1814477339
    - 最後で `return len(stack) == 0`、`return not stack`とするかは趣味の範囲
    - Google Style的には`return not stack` （implicit）
    - https://google.github.io/styleguide/pyguide.html#2144-decision
- https://github.com/SanakoMeine/leetcode/pull/7#discussion_r1903350766
    - 番兵を置いておけば条件減らせるし、stackが空かどうかの心配しなくていい
    - 括弧を扱うメソッドなので、番兵はそれ以外の文字列にしておけば良いか？(空文字、アスタリスクとか)
- https://discord.com/channels/1084280443945353267/1206101582861697046/1216945010189144085
    - プッシュダウンオートマトン（PDA）を連想するらしい（オートマトンは知っていたがPDAは初めて知った）
    - > valid parentheses は、チョムスキー階層、タイプ-2、文脈自由文法だから、プッシュダウンオートマトンで書ける、を多分連想します。
    - ↑用語は「常識」らしいが、ひとつもわからなかった。
        - https://en.wikipedia.org/wiki/Chomsky_hierarchy
        - http://www2.ics.teikyo-u.ac.jp/takei/pdf/2003FL12.pdf
        - https://www.jaist.ac.jp/~uehara/course/2010/ti118/13pda-n.pdf
        - https://stackoverflow.com/questions/8398030/chomsky-hierarchy-in-plain-english（一番わかりやすかった説明）
        - 形式文法
            - G = (T,N,S,P)
        -  チョムスキー階層（理解を言語化、間違ってるかも。。。）
            - タイプ-0: 帰納的可算文法
                - 制約なし
                - チューリングマシンTM（有限個の状態、有限個のルール、補助記憶:無限長のテープ）
            - タイプ-1: 文脈依存文法
                - αAβ →αγβ（前後の文脈α・βに応じて規則に沿って変換）
                - 線形拘束オートマトンLBA（有限個の状態、有限個のルール、補助記憶: 有限長のテープ）
            - タイプ-2: 文脈自由文法
                - A→α（前後に関係なく規則に沿って変換できる）
                - プッシュダウンオートマトンPDA（有限個の状態、有限個のルール、記憶装置：無限容量のスタック）
            - タイプ-3: 正規文法
                - A→a | a A（前後に関係なく規則に沿って変換できる、変換先の非終端記号は1つだけ=タイプ-2より制約が強い）
                - 有限オートマトンFA（有限個の状態、有限個のルール、記憶装置持たない）
            - テープ=どこでも参照できる、スタック=最も上にあるデータ（最後につまれたデータ）のみ参照できる
            - aは終端記号、A, Bは非終端記号、α・β・γ終端記号および/または非終端記号の文字列
    - なんとなくわかった気になっているだけなので、基礎から学びたい
        - discordでは、『計算理論の基礎　[原著第3版] 1.オートマトンと言語』がおすすめされていた
            - https://www.kyoritsu-pub.co.jp/book/b10030021.html



- https://discord.com/channels/1084280443945353267/1225849404037009609/1231646037077131315
- https://discord.com/channels/1084280443945353267/1225849404037009609/1231648833914802267
    - 問題文の制約が緩くなって括弧以外が来ても落ちないようにしたい→open_to_close
    - こんな感じがいいかな
疑似コード（＊1）
```
if ch in open_to_close:
    # 括弧：開
    # スタックに積む
elif ch in open_to_close.values():
    # 括弧：閉
    # チェック
else:
    # カッコ以外 → 無視
```
- https://discord.com/channels/1084280443945353267/1225849404037009609/1231646037077131315
    - > 私は、open_to_close でデータは持ちたいです。文字列にカッコ以外が来たときに落ちないで欲しいからです。
    - 理解できていない。。。（close_to_openだとしても（＊1）のように閉、開、その他で場合分けできそう。。。）
    - ただし、開→閉→その他の方が思考の流れとしては自然に感じる

- https://docs.python.org/3/library/collections.html#collections.deque
    - dequeを使っても実装できる
    - リストとの違い、だれかがエンジニアリングをして課題を解決してくれた
    - > Though list objects support similar operations, they are optimized for fast fixed-length operations and incur O(n) memory movement costs for pop(0) and insert(0, v) operations which change both the size and position of the underlying data representation.

- https://discord.com/channels/1084280443945353267/1225849404037009609/1231648833914802267
    - 文字が入ってきた時の好ましい挙動
    - コンパイラが念頭にありそうなので、エラーにせず無視がいい気がする（が、問題の制約においては好みの範囲な気がする）
- https://github.com/komdoroid/arai60/pull/12#discussion_r2630417643
    - Implicit False

## Step3

```Python3
from collections import deque

class Solution:
    OPEN_TO_CLOSE = {
        "(": ")",
        "[": "]",
        "{": "}"        
    }
    def isValid(self, s: str) -> bool:
        stack = deque()
        for ch in s:
            if ch in self.OPEN_TO_CLOSE:
                stack.append(ch)
            elif ch in self.OPEN_TO_CLOSE.values():
                if not stack:
                    return False
                prev_open = stack.pop()
                if ch != self.OPEN_TO_CLOSE[prev_open]:
                    return False
        return not stack
```