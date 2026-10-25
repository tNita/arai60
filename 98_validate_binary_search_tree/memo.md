# 98. Validate Binary Search Tree

Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:

- The left subtree of a node contains only nodes with keys strictly less than the node's key. 
- The right subtree of a node contains only nodes with keys strictly greater than the node's key. 
- Both the left and right subtrees must also be binary search trees.

Constraints 
- The number of nodes in the tree is in the range [1, 10^4].
- -2^31 <= Node.val <= 2^31 - 1

## Step1

- すべてのノードで、以下が成り立っていればよいか
  - （左の子がnull　or 自分より小さい）and （右の子がnull or 自分より大きい）
- DFS、BFSどちらでもできる。
- DFSについて、木が偏ると、再帰数が最大ノード数分（最大10000 > 再帰数のデフォルトの最大1000）になりうるので、再帰は避ける

```Python3
class Solution:
    def isValidBST(self, root: TreeNode | None) -> bool:
        if root is None:
            return False
        nodes = [root]
        while nodes:
            next_nodes = []
            for node in nodes:
                if node.left:
                    if node.val <= node.left.val:
                        return False
                    next_nodes.append(node.left)
                if node.right:
                    if node.val >= node.right.val:
                        return False
                    next_nodes.append(node.right)
            nodes = next_nodes
        return True
```

- acceptしなかった。
- 問題文を誤読していた。左の子の部分木全体のノード < ノード < 右の子の部分木全体のノードを求めないといけない（直下のノードだけが対象ではない）
- 左の子の部分木の最大 < ノード < 右の子の部分木の最小ノードが確認できれば良い
- 下から最大値、最小値を上げていく必要がある
  - 再帰 or 下から上げくるstackでとけそう
  - stackで実装してみようとしたが、混乱し、実装できなかった。
  - 代わりに再帰で実装する

```Python3
class SubTreeValidAndRange:
    def __init__(self, valid, min_val=None, max_val=None):
        self.valid = valid
        self.min_val = min_val
        self.max_val = max_val

class Solution:
    def isValidBST(self, root: TreeNode | None) -> bool:
        if root is None:
            return False
        
        def get_valid_bst_and_range(subtree_root: TreeNode) -> SubTreeValidAndRange:
            root_val = subtree_root.val
            min_val = max_val = root_val
            if subtree_root.left:
                left_valid_and_range = get_valid_bst_and_range(subtree_root.left)
                if not left_valid_and_range.valid or root_val <= left_valid_and_range.max_val:
                    return SubTreeValidAndRange(False)
                min_val = left_valid_and_range.min_val
            if subtree_root.right:
                right_valid_and_range = get_valid_bst_and_range(subtree_root.right)
                if not right_valid_and_range.valid or root_val >= right_valid_and_range.min_val:
                    return SubTreeValidAndRange(False)
                max_val = right_valid_and_range.max_val
            return SubTreeValidAndRange(True, min_val, max_val) 
        
        return get_valid_bst_and_range(root).valid
```
- 計算量
  - 時間計算量: O(N)（すべてのノードを見ないといけないため）
  - 空間計算量: O(N)（再帰数は木の深さとなるため、平衡木だったらO(logN)となる）


## Step2
### 自分のコードについて
- 再帰を使わない実装方法について。（by AI）
- postorder（帰りがけ順）
- resultsで、子の範囲をもっておき、親で回収
```Python3
class Solution:
    def isValidBST(self, root: TreeNode | None) -> bool:
        if root is None:
            return False

        stack = [(root, False)]
        results = {}
        while stack:
            node, visited = stack.pop()
            if not visited:
                stack.append((node, True))
                if node.right is not None:
                    stack.append((node.right, False))
                if node.left is not None:
                    stack.append((node.left, False))
                continue
            # 子の検証結果を親に持ち帰る
            left = results.pop(node.left, None)
            right = results.pop(node.right, None)

            if left is not None:
                if not left[0] or left[2] >= node.val:
                    return False
            if right is not None:
                if not right[0] or right[1] <= node.val:
                    return False

            minimum = left[1] if left else node.val
            maximum = right[2] if right else node.val
            results[node] = (True, minimum, maximum)
        return True
```

- inorder（通りがけ順）
- 左から、大きくなる（はずの）順でみていく
```Python3
class Solution:
    def isValidBST(self, root: TreeNode | None) -> bool:
        stack = []
        current = root
        prev = None
        while current is not None or stack:
            while current is not None:
                stack.append(current)
                current = current.left
            current = stack.pop()
            if prev is not None and prev >= current.val:
                return False
            prev = current.val
            current = current.right
        return True
```

### AIレビュー

>  **「下から最大値、最小値を上げていく必要がある」は、選択肢を狭めています。**
> 下から範囲を返すのは正しい方法です。一方で、祖先から「この部分木の値はこの範囲に収まる」という制約を渡す方法もあります。根を `10` とすると、左部分木の上限は `10`。その中で `5` の右へ進むなら、許される範囲は `5 < 値 < 10` になります。
> この方法なら、スタックに `(node, lower, upper)` を積んで上から検証できます。上下限がない場合の表現と、境界値を含まないことを決めればよいですね。「子の結果を待つ必要があるか」という観点で、下から集める方法と比べてみてください。
- 確かに、「部分木がこの範囲にあれば良い」というふうに読み替えれば、上から配る形で実装できそう。
- 試しに実装してみる

```Python3
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        # nodeを頂点とする木が(bottom, uppper)にあるよねの確認
        def is_valid_bst_helper(node: TreeNode, bottom: int, upper: int) -> bool:
            if not bottom < node.val < upper:
                return False
            if node.left and not is_valid_bst_helper(node.left, bottom, node.val):
                return False
            if node.right and not is_valid_bst_helper(node.right, node.val, upper):
                return False
            return True
        return is_valid_bst_helper(root, -inf, inf)
```

### コメント集・他の人のコード
- https://discord.com/channels/1084280443945353267/1192736784354918470/1235116690661179465
  - Generatorでの実装
  - > 走りかけの Generator を木の深さ分だけ作るのでそこそこ重いことがありそうですね。
- https://discord.com/channels/1084280443945353267/1262688866326941718/1303256354332348458
  - Goだとgoroutineのchanを使って実装できるのか。
  - バックグラウンドでノードをinorderで一つづつ送信する
  - メイン側で一つづつ受け取って値を比較
- https://discord.com/channels/1084280443945353267/1421920158506549470/1433529697983139883
  - iterativeな帰りがけ
  - 自分でも書いてみる
```Python 
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        if root is None:
            return True
        nodes = [([], root, [], [])]
        while nodes:
            node_range, node, left_range, right_range = nodes[-1]
            if not left_range and node.left:
                nodes.append((left_range, node.left, [], []))
                continue
            if not right_range and node.right:
                nodes.append((right_range, node.right, [], []))
                continue
            if left_range and node.val <= left_range[1]:
                return False
            if right_range and node.val >= right_range[0]:
                return False
            node_values = left_range + [node.val] + right_range
            node_range += [node_values[0], node_values[-1]]
            nodes.pop()
        return True
```
- https://github.com/naoto-iwase/leetcode/pull/33
  - postorderで実装するとき、preorderとpostorderの２つのstackを用意する
    - 個人的にはわかりやすくて好きかも
  - postorderの再帰関数でvalid, min, maxを返すとき、valid=Falseのときはmin, maxを0で返す（一貫して実装できていれば好みの範囲）
- https://github.com/fuga-98/arai60/pull/28
  - https://github.com/fuga-98/arai60/pull/28/changes#r2018420862
  - 通りがけで値のリストを作ってそれが昇順かをチェックする方法もあるが、リストを作る、昇順かチェックを分けなくて良い
```Python
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        prev = -inf
        def is_valid_bst(node) -> bool:
            nonlocal prev
            if node is None:
                return True
            if not is_valid_bst(node.left):
                return False
            if node.val <= prev:
                return False
            prev = node.val
            if not is_valid_bst(node.right):
                return False
            return True
        return is_valid_bst(root)
```
- https://github.com/mamo3gr/arai60/pull/26
  - rootがNoneのとき
    - 空の木として良さそう
    - Optionalな木を引数とする関数を再帰的に呼び出すときはNoneのときはTrueと扱うほうが扱いやすい（再帰的に呼び出すとき、部分木がない場合は二分木かどうかの観点では問題なしなため）
- https://github.com/hayashi-ay/leetcode/pull/38/
  - inorderでiterative

## Step3
上から範囲を「配る」DFSとinorderが自然に感じた

再帰上限超過の懸念からどちらもiterativeに書いておく

DFS

```Python3
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        if root is None:
            return True
        nodes = [(root, -inf, inf)]
        while nodes:
            node, lower_bound, upper_bound = nodes.pop()
            if not lower_bound < node.val < upper_bound:
                return False
            if node.right:
                nodes.append((node.right, node.val, upper_bound))
            if node.left:
                nodes.append((node.left, lower_bound, node.val))
        return True
```

inorder

```Python3
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def append_left_nodes(node: TreeNode):
            while node:
                nodes.append(node)
                node = node.left
        nodes = []
        append_left_nodes(root)
        prev = -inf
        while nodes:
            node = nodes.pop()
            if node.val <= prev:
                return False
            prev = node.val
            append_left_nodes(node.right)
        return True
```