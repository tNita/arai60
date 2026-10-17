# 102. Binary Tree Level Order Traversal

Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).


The number of nodes in the tree is in the range [0, 2000].
-1000 <= Node.val <= 1000

## Step1
- ユースケースとしては、ディレクトリの一覧を出力するのが一例
- 階層ごと見ていくので幅優先が相性良いか
- 深さ優先の場合は、今自分がどの階層に入るのかを記録する必要があるので少し面倒

```Python3
class Solution:
    def levelOrder(self, root: TreeNode | None) -> list[list[int]]:
        if root is None:
            return []
        nodes = [root]
        level_order_traversal = []
        while nodes:
            level_order_traversal.append([node.val for node in nodes])
            next_nodes = []            
            for node in nodes:
                if node.left:
                    next_nodes.append(node.left)
                if node.right:
                    next_nodes.append(node.right)
            nodes = next_nodes
        return level_order_traversal
```

- 時間計算量: 全ノードを見ないといけないのでO(N)
- 空間計算量: キューは最大の幅分なのでO(N)、返り値もノード数分なのでO(N)

## Step2

### 他の選択肢
DFSでやってみる

再帰
```Python3
class Solution:
    def levelOrder(self, root: TreeNode | None) -> list[list[int]]:
        if root is None:
            return []
        left_node_values = self.levelOrder(root.left)
        right_node_values = self.levelOrder(root.right)

        merged_child_values = [[] for _ in range(max(len(left_node_values), len(right_node_values)))]
        for level, left_nodes in enumerate(left_node_values):
            merged_child_values[level].extend(left_nodes)
        for level, right_nodes in enumerate(right_node_values):
            merged_child_values[level].extend(right_nodes)

        result = [[root.val]]
        result.extend(merged_child_values)
        return result
```
スタック利用
```Python3
class Solution:
    def levelOrder(self, root: TreeNode | None) -> list[list[int]]:
        if root is None:
            return []
        result = []
        def safeAppend(i: int, val: int):
            original_result_length = len(result)
            if i > original_result_length:
                # 例外迷ったが、値が不適切ということを教えたいのでこれを選択
                raise ValueError(f"i should be {original_result_length} or less.")
            if i < original_result_length:
                result[i].append(val)
            else:
                result.append([val])

        frontier = [(root, 0)]
        while frontier:
            node, depth = frontier.pop()
            safeAppend(depth, node.val)

            # 順序は大事、結果が各層でleft→rightとなるようにするため、stackにはright、leftの順で入れる
            if node.right:
                frontier.append((node.right, depth + 1))
            if node.left:
                frontier.append((node.left, depth + 1))
        return result
```

### AIレビュー
> **`safeAppend`が何を保証する関数なのか、整理したいです。**
   名前からは、何に対して安全なのかが分かりません。また、負の`i`を拒否せず、Pythonの負の添字として扱います。
- index out of rangeにはならないように要素を追加するというのをうまく表現できず、なんとなくsafeという言葉を使った。
  - > • その意図なら、**「必要なら段を作り、その段に値を追加する」**と捉えると名前を付けやすそうです。今回ならappend_to_level(depth, value)が候補です。
  - 確かにしっくり来る。
- levelOrderの中でしか使わないメソッドだから、どこまで入力を検査すべきか迷った
  - 検査する方針にするならば、iが負の時の検査模するべきか

> **2つのDFSは、情報を渡す方向が違います。**
再帰版は「子で作った結果を親に返して結合する」、スタック版は「親から子へ深さを渡して、共通の結果に追加する」です。この違いを説明できるようにしておくとよいと思います。再帰でも深さと共通の結果を使えば、結合処理は省けます。
- 上から配る再帰を実際に書いてみた。こちらのほうがシンプルと感じた

```Python3
class Solution:
    def levelOrder(self, root: TreeNode | None) -> list[list[int]]:
        result = []
        def append_to_level(depth, val):
            result_length = len(result)
            if depth < result_length:
                result[depth].append(val)
            elif depth == result_length:
                result.append([val])
            else:
                raise ValueError("i should be {result_length} or less.")

        def set_result(node, depth):
            if node is None:
                return
            append_to_level(depth, node.val)
            set_result(node.left, depth + 1)
            set_result(node.right, depth + 1)
        
        set_result(root, 0)
        return result
```

### コメント集

- https://discord.com/channels/1084280443945353267/1200089668901937312/1211248049884499988
  - Step2の再帰の実装のappend_to_levelに関して
  - depthまでresultを拡張してからdepth二値をセットするほうが自然かもな
- https://github.com/kazuki-official/leetcode/pull/26
  - > * `result`という変数名は抽象的すぎるので`node_chunks_by_level`に変更
  - 結果に加えるタイミングが次の階層のノードを配列にセットした後（forの後）→どっちにするかは好みの問題だと思った
- https://github.com/nanae772/leetcode-arai60/pull/26
  - itertools.chainの使い方
  - アンパックについて
    - イテラブルの要素を展開してそれぞれの引数に渡す
    - https://docs.python.org/ja/3.12/tutorial/controlflow.html#unpacking-argument-lists

```Python3
import itertools
class Solution:
    def levelOrder(self, root: TreeNode | None) -> list[list[int]]:
        if root is None:
            return []
        nodes = [root]
        result = []
        while nodes:
            result.append([node.val for node in nodes])
            next_nodes = []
            next_nodes_candidates = itertools.chain(
                *[[node.left, node.right] for node in nodes]
            )
            for candidate in next_nodes_candidates:
                if candidate:
                    next_nodes.append(candidate)
            nodes = next_nodes
        return result
```

## Step3

```Python3
class Solution:
    def levelOrder(self, root: TreeNode | None) -> list[list[int]]:
        if root is None:
            return []

        nodes = [root]
        nodes_level_by_level = []
        while nodes:
            nodes_level_by_level.append([node.val for node in nodes])
            next_nodes = []
            for node in nodes:
                if node.left:
                    next_nodes.append(node.left)
                if node.right:
                    next_nodes.append(node.right)
            nodes = next_nodes
        return nodes_level_by_level
```