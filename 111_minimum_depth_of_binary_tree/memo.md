# 111. Minimum Depth of Binary Tree

Given a binary tree, find its minimum depth.

The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.

Note: A leaf is a node with no children.

https://leetcode.com/problems/minimum-depth-of-binary-tree/description/


制約
> - The number of nodes in the tree is in the range [0, 10^5].
> - -1000 <= Node.val <= 1000

## Step1

- レイヤーごとに見ていき(幅優先）、葉を見つけた羅、その葉の深さを最小の深さとして答えれば良い
  - 前のレイヤーには葉がないことが確定しているので、全てのノードを見ずして最小の深さと答えられる
- 深さ優先で探す場合、全てのノードを見ないといけない。
- 制約的に再帰は怖い（木が偏っていたら再帰が10^5になりデフォルトの1000を超えてしまう）


実装した。
- ノードは有限=ノードの中に葉が必ずあるので、for文の中のreturnには必ず到達するため、while分の後にreturnを書く必要はない
- whileの後に何を書くかは色々方針がある
  - return
  - 想定外であることを伝える例外を投げる
  - エラーログ + return
- 1つ目は予期せぬことが起こっていることに気づけないのでNG
- 2つ目にするか3つ目にするかはユースケースによるが、基本二つ目で例外を投げるのが良さそう。

```Python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def minDepth(self, root: TreeNode | None) -> int:
        if root is None:
            return 0
        frontier = [root]
        depth = 0
        while frontier:
            next_frontier = []
            depth += 1
            for node in frontier:
                if node.left is None and node.right is None:
                    return depth
                if node.left is not None:
                    next_frontier.append(node.left)
                if node.right is not None:
                    next_frontier.append(node.right)
            frontier = next_frontier
        # バグ
        raise RuntimeError("ソースのバグにより最小深さを算出できませんでした。")
```
## Step2

### 自分で他の実装をしてみる

BFSでレイヤーごとの処理にはしない
```Python
class Solution:
    def minDepth(self, root: TreeNode | None) -> int:
        if root is None:
            return 0
        frontier = deque()
        frontier.append((root, 1))
        current_depth = 1
        while len(frontier):
            node, depth = frontier.popleft()
            current_depth = max(current_depth, depth)
            if node.left is None and node.right is None:
                return current_depth
            if node.right is not None:
                frontier.append((node.right, current_depth + 1))
            if node.left is not None:
                frontier.append((node.left, current_depth + 1))
        raise RuntimeError("ソースのバグにより最小深さを算出できませんでした。")
```
### コメント集や他の人のPR

- https://discord.com/channels/1084280443945353267/1251052599294296114/1258477291567317152
  - 左右の子をfrontierにappendする処理を配列を使ってまとめる
- BFSについて、depthを更新するのはfrontierを更新するタイミングに揃える
  - https://github.com/olsen-blue/Arai60/pull/22/changes#r1925335296
  - 自分のStep1の実装では、depthの意味を固定できていなかった
    - depth更新前まで： frontierの一つ上の階層の深さ
    - depth更新後: frontierと同じ深さ
  - frontierの深さをdepthと考えるのが素直
- RuntimerErrorの文言（unreachable error）が端的で良き
  - https://github.com/tom4649/Coding/pull/20/changes#diff-974436ac64380be2414ffa842d4dc5dd641279483233dca84985f0deee4311e2R24
- キューにnil(PythonならNone)も入れるかどうかは好みの範囲。ただし、入れるかどうかは一貫する必要がある
  - https://github.com/miyataka/coding-practice/pull/21
- https://github.com/fuga-98/arai60/pull/22
  - 一般的ではないがBFSを再帰で実現するというやり方もありそう（以下で実装）

行きかけで深さ更新（上から配る）
```Python
class Solution:
    def minDepth(self, root: TreeNode | None) -> int:
        depth = 1
        def update_depth_by_layer(nodes):
            nonlocal depth
            next_layer_nodes = []
            for node in nodes:
                if node.left is None and node.right is None:
                    return
                if node.right is not None:
                    next_layer_nodes.append(node.right)
                if node.left is not None:
                    next_layer_nodes.append(node.left)
            depth += 1
            update_depth_by_layer(next_layer_nodes)
        if root is None:
            return 0
        update_depth_by_layer([root])
        return depth
```
- https://github.com/naoto-iwase/leetcode/pull/21
  - 下から上げる系の再帰(BFS）も可能。下で実装してみる
```Python
class Solution:
    def minDepth(self, root: TreeNode | None) -> int:
        def get_min_depth_of_layer(nodes):
            next_layer_nodes = []
            for node in nodes:
                if node.left is None and node.right is None:
                    return 1
                if node.right is not None:
                    next_layer_nodes.append(node.right)
                if node.left is not None:
                    next_layer_nodes.append(node.left)
            return 1 + get_min_depth_of_layer(next_layer_nodes)
        if root is None:
            return 0
        return get_min_depth_of_layer([root])
            
```
- 葉であることのチェックは関数に切り出したほうが意味が明瞭で好き
  - https://github.com/mamo3gr/arai60/pull/20

## Step3

```Python
class Solution:
    def minDepth(self, root: TreeNode | None) -> int:
        if root is None:
            return 0
        def isleaf(node):
            return node.left is None and node.right is None
        frontier = [root]
        depth = 1
        while frontier:
            next_frontier = []
            for node in frontier:
                if isleaf(node):
                    return depth
                if node.left is not None:
                    next_frontier.append(node.left)
                if node.right is not None:
                    next_frontier.append(node.right)
            frontier = next_frontier
            depth += 1
        raise RuntimeError("unreachable")
```