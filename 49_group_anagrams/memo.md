# 49. Group Anagrams

Given an array of strings strs, group the anagrams together. You can return the answer in any order.

Constraints:

- 1 <= strs.length <= 10^4
- 0 <= strs[i].length <= 100
- strs[i] consists of lowercase English letters.

## Step1

- 文字列の長さは100で短い
- 配列の要素は10^4
- 文字列をソートして同じものをグループ化する。
- データ構造としては辞書型を利用、キーをソートした文字列、値（配列）を元の文字列
  - 文字数高々100なので、ソートの計算コストの影響は小さそう（ネイティブコードが動くし）
  - ソートを使って元の文字列→配列へ、joinで配列→文字列へ
  - https://docs.python.org/3/library/stdtypes.html
  - > Concatenating immutable sequences always results in a new object. This means that building up a sequence by repeated concatenation will have a quadratic runtime cost in the total sequence length. To get a linear runtime cost, you must switch to one of the alternatives below:
      if concatenating str objects, you can build a list and use str.join() at the end or else write to an io.StringIO instance and retrieve its value when complete
  - 他の方法もある: [io.StringIO](https://docs.python.org/3/library/io.html#io.StringIO)
    - 純粋なメモリバッファーなので、大きな文字列を構築する用って感じがする
  - by GPT-5: 
    - list + ''.join()
      - Pros 
        - 速い（線形時間、公式推奨）https://docs.python.org/3/library/stdtypes.html
        - シンプルで可読性が高い 
      - Cons 
        - 最後まで完成文字列を取得できない 
        - 断片リスト分のメモリを保持 
      - io.StringIO 
        - Pros 
          - .write() / print(..., file=...) で書ける（ストリーム設計に合う）https://docs.python.org/3/library/io.html
          - 逐次出力ロジックと相性が良い 
        - Cons 
          - やや冗長（getvalue() が必要） 
          - 単純連結だけなら join の方が素直
- valuesを利用すれば、dictの値のビューを作れる（配列ではない）
  - https://docs.python.org/3/library/stdtypes.html#dict.values

```Python3
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for original_str in strs:
            sorted_str = "".join(sorted(original_str))
            groups[sorted_str].append(original_str)
        return list(groups.values())
```

- 計算量（※ N = 文字列数, K = 1文字列あたりの平均長さ）
  - 時間計算量は O(N × K log K)
  - 空間計算量は O(N × K)

## Step2
### 他の人のコードを読む
- https://github.com/kitano-kazuki/leetcode/pull/12
  - TODO: 後で理解
  - Union findも検討されている
  - 自前でハッシュを作る方法も検討されている
- https://github.com/dorxyxki/arai60/pull/12
  - ソートした文字列をキーとする時、`tuple(sorted(s))`や`str(sorted(s))`もある
    - https://github.com/dorxyxki/arai60/pull/12/changes#diff-67ed0a90cad1f2106cd30d7f72d6ea46293f7b399ff1aac08bcfd6eb05c2f49fR15
    - tupleはhashableなのでdictのキーにできる
      - https://docs.python.org/3/glossary.html#term-hashable
- https://github.com/ksaito0629/leetcode_arai60/pull/11
  - アルファベットの出現回数をキーとする方法
    - https://github.com/ksaito0629/leetcode_arai60/pull/11/changes#diff-0e9b06f125622811740ec5b217d1d58851ee355271b9ca8f1deab15ad7261df4R54
    - ordはUnicodeのコードポイント（整数）を返す関数
  - a-zのコードポイントが+1ずつ増えていくことを利用
  - 時間計算量自体はO(klogk)→O(k)に改善できるかもしれないが、PythonコードでO(k)なので、実際の実行時間は遅い
    - k <= 100であり、ネイティブコードはPythonコードの100倍早いので、ソートした文字列をキーとする方がシンプルで速い（LeetCodeの実行時間もソートした文字列をキーとする方が速い）
      - ソートした文字列をキーとする時：100 log 100 = 664
      - アルファベットの出現回数をキー：100 
- https://github.com/mamo3gr/arai60/pull/12
  - https://github.com/mamo3gr/arai60/pull/12/changes#r2647994625
    - ヒストグラムの方法：Counterを使う
      - ユニークな文字の数が少ないと有利か
      - https://github.com/naoto-iwase/leetcode/pull/12
    - dictを継承してdefaultdictを自前で実装する話からクラスの話
      - https://github.com/mamo3gr/arai60/pull/12/changes#r2648387939
- https://github.com/hayashi-ay/leetcode/pull/19
- https://github.com/fuga-98/arai60/pull/13
- https://github.com/naoto-iwase/leetcode/pull/12
  - アルファベット小文字
    - https://docs.python.org/ja/3.13/library/string.html#string.ascii_lowercase
  - https://github.com/naoto-iwase/leetcode/pull/12/changes#r2413331965
    - 定数倍は重要だが、手段の一つに過ぎない
      - > 具体的にかかる計算時間とその計算時間で目的を達成できるかが重要です。
- https://github.com/ichika0615/arai60/pull/11/changes#r1978511189
  - ランレングスエンコーディング
    - https://ja.wikipedia.org/wiki/%E9%80%A3%E9%95%B7%E5%9C%A7%E7%B8%AE
    - 「AAAAABBBBBBBBBAAA」は「A5B9A3」

### コメント集を読む
- https://discord.com/channels/1084280443945353267/1247673286503039020/1252265786660356168
  - アルファベットの出現回数をキーとする方法に対して
  - > 小文字アルファベット以外が来ると何が起きるか考えておきましょう。
  - > どうでなくてはいけないというよりは、その帰結としてありうるシナリオの幅を広く考えておきたい、くらいの意図です。
- https://github.com/ichika0615/arai60/pull/11/changes#r1975712971
  - 可変長数値表現
    - https://ja.wikipedia.org/wiki/%E5%8F%AF%E5%A4%89%E9%95%B7%E6%95%B0%E5%80%A4%E8%A1%A8%E7%8F%BE
  - エスケープシーケンス
    - 区切り文字を使うなら、区切り文字が文字列に含まれる可能性を考慮する必要がある
      - この解答
        - `$`で文字と文字の出現回数を区切っているが、`$`自体が文字列に含まれると問題が起きるため、`$`を`\$`にエスケープする必要がある
      - JSON
        - https://www.rfc-editor.org/rfc/rfc8259#section-7
        - > All Unicode characters may be placed within the
          quotation marks, except for the characters that MUST be escaped:
          quotation mark, reverse solidus, and the control characters (U+0000
          through U+001F)

## Step3

```Python3
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        sorted_key_to_original_words = defaultdict(list)
        for original_word in strs:
            key = tuple(sorted(original_word))
            sorted_key_to_original_words[key].append(original_word)
        return list(sorted_key_to_original_words.values())
```

## TODO
- [] https://github.com/nktr-cp/leetcode/pull/13/changes#r2087242821
  - cppの理解を深めてから
  - > (コピーを減らす価値があるかはともかく)
    s については、strs の中身へのポインターでもいいかもしれませんね。
    strs のサイズ周りを変えない限りは、ポインターは valid だったと思います。 
    でも、下のようにどうせ move するんだったら vector 作ったほうがいいですね。
- [] 