# 127. Word Ladder

https://leetcode.com/problems/word-ladder/description/

A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:

Every adjacent pair of words differs by a single letter.
Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
sk == endWord
Given two words, beginWord and endWord, and a dictionary wordList, return the number of words in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.

Constraints
- 1 <= beginWord.length <= 10
- endWord.length == beginWord.length
- 1 <= wordList.length <= 5000
- wordList[i].length == beginWord.length
- beginWord, endWord, and wordList[i] consist of lowercase English letters.
- beginWord != endWord
- All the words in wordList are unique.

## Step1
- 長さ高々10なので、先頭から1文字ずつかえてみて、wordListにあったら前進めるやり方（樹形樹上に探していく）
  - 文字を変えてみてなければその経路はNG
  - 同じ文字は2回現れないようにする（2回現れた=ループしているならば、その経路は最短ではないため）

```Python3
"""
- 長さ高々10なので、先頭から1文字ずつかえてみて、wordListにあったら前進めるやり方（樹形樹上に探していく）
    - 文字を変えてみてなければその経路はNG
    - 同じ文字は2回現れないようにする（2回現れた=ループしているならば、その経路は最短ではないため）

"""
class Solution:
    LOWER_ENGLISH_LETTERS = "abcdefghijklmnopqrstuvwxyz"
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        # 与えられた文字列のi番目を差し替えた時の候補
        def get_candidate_next_word(current_word: str, change_at: int, previous_sequence: List[str]) -> List[str]:
            candidates = []
            for letter in self.LOWER_ENGLISH_LETTERS:
                # 必ず1文字変えないといけないので
                if letter == current_word[change_at]:
                    continue
                new_word_candidates = current_word[:change_at] + letter + current_word[change_at+1:]
                if new_word_candidates in wordList and new_word_candidates not in previous_sequence:
                    candidates.append(new_word_candidates)
            return candidates

        # start_wordを含む長さ
        # endWordに至らない時はNoneを返す
        def get_min_sequence_length(start_word: str, previous_sequence: List[str]) -> Optional[int]:
            if start_word == endWord:
                return 1
            next_min_length = None
            for i in range(len(start_word)):
                candidates = get_candidate_next_word(start_word, i, previous_sequence)
                for candidate in candidates:
                    candidate_sequence = deepcopy(previous_sequence)
                    candidate_sequence.append(start_word)
                    candidate_min_length = get_min_sequence_length(candidate, candidate_sequence)
                    if candidate_min_length is None:
                        continue
                    if next_min_length is None:
                        next_min_length = candidate_min_length
                        continue
                    next_min_length = min(next_min_length, candidate_min_length)
            return None if next_min_length is None else next_min_length + 1
        
        min_sequence_length = get_min_sequence_length(beginWord, [])
        return 0 if min_sequence_length is None else min_sequence_length
```
- TTLでアクセプトしなかった
  - 24 / 52 testcases passed
- どこがボトルネックなのだろう？
  - 毎回deeepcopyしているところ？
    - 今は深さ優先なのでprevious_sequenceが増えたり減ったりするため毎回deepcopyしている
    - 幅優先にしたら毎回deepcopyしなくてよくなるか？
    - 混乱してしまい、わからなくなってしまったためStep2に行く

## Step2

### 他の人のコードを読む

- https://github.com/hayashi-ay/leetcode/pull/42
  - > 事前に"\*it"などの一文字を任意にした状態のワードの一覧を作ってあげれば次のノードを見つけるのが楽になる。
  - これ、一発で候補が取れるようになるので賢い
  - 一方で、文字自体に*が入ってくるとNG→ 前後のtupleをキーにすれば良さげ（from コメント集）
- 隣接リストを作ってから幅優先で解く
  - 最短経路を求める問題で、幅優先（距離 l が同じものを全て見たあとに l + 1を見にいく）でみていく
  - 初めてあるワードはでた場合、そこはその語に到達するまでの最短経路だから、変数 `seen` １つで既出を管理すればOK（経路ごとに用意する必要なし）
```Python3
words = [beginWord]
seen = set(words)
num_of_words = 1
while words:
  next_words = []
  num_of_words += 1
  for word in words:
    for next_word in adj[word]:
      if next_word in seen:
        continue
      if next_word == endWord:
        return num_of_words
      seen.add(next_word)
      next_words.append(next_word)
  words = next_words
```
- https://github.com/fuga-98/arai60/pull/20
  - 見積もり
    - https://github.com/t0hsumi/leetcode/pull/20/files#r1944383585
- https://github.com/naoto-iwase/leetcode/pull/19
  - zipの利用
    - `for char1, char2 in zip(word1, word2):`
  - indexを利用して処理
    - 省メモリを狙ってのこと
    - 開発するソフトウェア次第にはなるが、メモリにそこまで厳しい制約がないならばindexでの処理はしなくても良いか、ケースバイケース
    - > - int参照の方が多少軽量かもしれないが、ボトルネックにはなってないのであまり意味はなく、可読性のためにそのまま文字列でいいだろう。
  - ap*leで、(ap, le)をキーとして候補をvalueにもつ（ap*leをキーにすると元の文字列に*が含まれるとうまく動かない）
  - 双方向BFSでもっと時間を短縮可能
  - dense
    - 密に、反対は sparse（疎）
- https://github.com/rimokem/arai60/pull/20
  - setから要素があれば取り除く→ set.discardを利用すればsetに要素があるかのチェックは不要
    - https://docs.python.org/ja/3/library/stdtypes.html#set.discard
- https://github.com/Manato110/LeetCode-arai60/pull/19
  - https://github.com/Manato110/LeetCode-arai60/pull/19/changes#diff-6af1d3766cdb1f360b48f7d205c69c10ddb1b71987ff02621ecc329a349892a0R4
    - 具体のイメージ
    - > イメージはダイヤル錠を回してリストのある単語を作っていく縛りをつけながらゴールを目指す感じ？
  - layerごとのDFSで解いている（個人的にはlayerごとの方が距離の管理を一元的にできるので好みだな）
- https://github.com/kitano-kazuki/leetcode/pull/19
  - beginWordがなければ、wordListに入れて処理
  - Nodeを定義し、wordListの位置とNodeの関係を管理するdictを作る
  - former latterでやるやり方
    - → 複雑で理解できない。。。
    - 一旦後回し
- https://github.com/h-masder/Arai60/pull/21
  - 幅優先の方が相性が良いことの言語化
    - > 幅優先なら、1文字違い -> 2文字違い -> ・・・のように、順にみていくので最短経路を保証しながら探索できる。
    - > 一方、深さ優先は、出現した経路が文字の長さを超えた場合、それが最短経路である保証はないので調べ続ける必要がある。
  - 一文字違いを生成するのはクラスとして切り出す
- https://github.com/rimokem/arai60/pull/20
  - 見積もり

### コメント集

https://discord.com/channels/1084280443945353267/1183683738635346001/1199046289686548581
https://cs.stackexchange.com/questions/93467/data-structure-or-algorithm-for-quickly-finding-differences-between-strings
> 頭から半分または尻尾から半分が一致しているはずなので、それでバケットを作ってバケット内でのみ比較すればいいというやりかたもありますね。

AIに書かせてみる
```Python3
from collections import defaultdict
from itertools import combinations

def differ_by_one(a: str, b: str) -> bool:
    diff = 0
    for x, y in zip(a, b):
        if x != y:
            diff += 1
            if diff > 1:
                return False
    return diff == 1

def find_pair_differ_by_one(words: list[str]) -> tuple[str, str] | None:
    if not words:
        return None

    k = len(words[0])
    mid = k // 2

    # 前半一致で探す
    buckets = defaultdict(list)
    for w in words:
        buckets[w[:mid]].append(w)

    for bucket in buckets.values():
        for a, b in combinations(bucket, 2):
            if differ_by_one(a, b):
                return a, b

    # 後半一致で探す
    buckets = defaultdict(list)
    for w in words:
        buckets[w[mid:]].append(w)

    for bucket in buckets.values():
        for a, b in combinations(bucket, 2):
            if differ_by_one(a, b):
                return a, b

    return None
```
- https://discord.com/channels/1084280443945353267/1200089668901937312/1201846091868540948
コードが長くなると名前空間が汚れてくる

## Step3

```Python3
class WordNeighbors:
    def __init__(self):
        self.word_pattern_to_neighbors = defaultdict(list)

    def add(self, word):
        for i in range(len(word)):
            self.word_pattern_to_neighbors[(word[:i], word[i+1:])].append(word)

    def generate_neighbors(self, word):
        for i in range(len(word)):
            for neighbor in self.word_pattern_to_neighbors[(word[:i], word[i+1:])]:
                yield neighbor

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        word_set = set(wordList)
        word_neighbors = WordNeighbors()
        for word in word_set:
            word_neighbors.add(word)
        frontier = deque([(beginWord, 1)])
        seen = {beginWord}
        while frontier:
            word, depth = frontier.popleft()
            if word == endWord:
                return depth
            for neighbor in word_neighbors.generate_neighbors(word):
                if neighbor not in seen:
                    seen.add(neighbor)
                    frontier.append((neighbor, depth + 1))
        return 0
```
## TODO

[] former latterでやるやり方を理解

## その他
- わからないところに時間をかけすぎてしまった（結局わからなかった）
  - 考える時間の制限を設けて、それでもわからなければ一旦次に行くのが良さそう
