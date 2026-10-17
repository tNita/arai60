# 103. Binary Tree Zigzag Level Order Traversal

Given the root of a binary tree, return the zigzag level order traversal of its nodes' values. (i.e., from left to right, then right to left for the next level and alternate between).

Constraints:

The number of nodes in the tree is in the range [0, 2000].
-100 <= Node.val <= 100

## Step1
- 幅優先で、幅ごとに処理していくのが良い
- 深さごとにどちら向きかわかる
  - 深さが奇数であればleft→right, 偶数であればright→left

```Python3
class Solution:
    def zigzagLevelOrder(self, root: TreeNode | None) -> list[list[int]]:
        if root is None:
            return []
        nodes = [root]
        left_to_right = True
        nodes_level_by_level = []
        while nodes:
            nodes_level_by_level.append([node.val for node in nodes])

            next_nodes = []
            last_index_of_nodes = len(nodes) - 1
            left_to_right = not left_to_right
            for i in range(len(nodes)):
                node = nodes[last_index_of_nodes - i]
                first = node.left
                second = node.right
                if not left_to_right:
                    first, second = second, first
                if first:
                    next_nodes.append(first)
                if second:
                    next_nodes.append(second)
            nodes = next_nodes
        return nodes_level_by_level
```

## Step2

### AIレビュー

> 1. **探索する順序まで交互に変える必要があるか、考えてみてください。**
> 「親を逆順に読む」「子を追加する順番を変える」の組み合わせで次の階層を作っていますね。正しく動きますが、読み手はこの二つがどう組み合わさるかを考える必要があります。
> 毎回左から右へ次の階層を作り、結果に追加する値のリストだけ必要に応じて反転すれば、説明も実装も単純になると思います。手作業を他人に頼むとして、どちらの説明が伝えやすいでしょうか。

- 納得した。
- 深さが偶数のときは結果に逆順につめるようにするだけで良い。

> **`left_to_right` が、どの階層の向きを表すのか追いかける必要があります。**

- 今のノードの階層の向きを表していた
- ただ、逆順に入れる処理は次の階層。ズレが生じていたため、whileの途中でleft_to_rightを反転する処理をしてしまっていた。。。。

> - **逆順に読む操作は、そのまま書けます。**
> 今の方針を維持する場合でも、`for node in reversed(nodes):` と書けますね。添字の計算を読み解かなくても、「逆順に読む」が直接伝わります。
- 反転の仕方の「幅」が見えていなかった

まとめ by GPT-6

| 方法                     | 戻り値      | 元のリストを変更 | 計算量      |
|------------------------|----------|----------|----------|
| `list(reversed(a))`    | 新しいリスト   | しない      | O(n)     |
| `a[::-1]`              | 新しいリスト   | しない      | O(n)     |
| `a.reverse()`          | `None`   | する       | O(n)     |
| `for x in reversed(a)` | 要素を順番に取得 | しない      | 全走査 O(n) |

### 他の人のコード

- https://github.com/kazuki-official/leetcode/pull/27
  - > * 結果を格納する配列で 28 bytes * 2000 / 1024 = 56KB
  - 空間計算量の見積もり。28 bytesはintのサイズ、2000は個数。
  - > C++ はコピーうるさめですが、Python は細かいことをいってもしょうがないところもありますね。 いずれにせよどれくらい遅いかは定量的に考えておきましょう。
  - C++がコピーにうるさい理由はこんな感じか？
    - C++はGCがなく自分でメモリを解放する必要がある
    - C++は高トラフィックで、処理時間やメモリ使用量に対する制約が比較的厳しい環境で利用されることが多い
- https://github.com/mamo3gr/arai60/pull/27
  - 幅単位の再帰でもかけそう（目立ったメリットはなさそう）
- https://github.com/naoto-iwase/leetcode/pull/31
  - 反転するかを高さを2で割ったあまりで判断（好みの範囲だが、フラグのほうが直接的か）
- https://github.com/fuga-98/arai60/pull/27
  - ノードの値を逆順にリストに追加する場合、dequeのappendleftで一つづつ右に追加するというやり方もあり

## Step3

```Python3
class Solution:
    def zigzagLevelOrder(self, root: TreeNode | None) -> list[list[int]]:
        if root is None:
            return []
        
        nodes_layer_by_layer = []
        nodes = [root]
        right_to_left = False
        while nodes:
            node_values = []
            next_nodes = []
            for node in nodes:
                node_values.append(node.val)
                if node.left:
                    next_nodes.append(node.left)
                if node.right:
                    next_nodes.append(node.right)
            if right_to_left:
                node_values = node_values[::-1]
            nodes_layer_by_layer.append(node_values)
            nodes = next_nodes
            right_to_left = not right_to_left
        return nodes_layer_by_layer
```
