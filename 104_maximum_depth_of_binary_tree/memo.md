# 104. Maximum Depth of Binary Tree

https://leetcode.com/problems/maximum-depth-of-binary-tree/description/

Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

```Python3
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```
Constraints:
- The number of nodes in the tree is in the range [0, 10^4].
- 100 <= Node.val <= 100

## Step1
- Nodeのvalの制約が与えられているが、今回の要件的には関係ない
- ノード数は最高10^4。木構造が偏っていたら、深さは最大10^4
- 幅優先、深さ優先でやる方法があるが、今回はどちらでも大差なし（最大の深さを求める必要があるため、どちらの手段でも全てのノードを見ないといけない）
- 再帰で実装する方法もあるが、再帰の最大が10^4になりうる、再帰上限のデフォルトは1000であることを考慮して採用しない
  - https://docs.python.org/3/library/sys.html#sys.setrecursionlimit

幅優先で実装する。
幅優先で見ていくとき、一つ下のノードをキューにためていくことなる。
キューの実装方法はdequeを選択する
- list: pop(0)でキューから取り出すときに、メモリ移動が発生しO(N)になるため、dequeに比べるとパフォーマンス面でマイナス 
- collections.deque: キューへの追加、取り出しをO(1)で実現できるため利用する
- queue.Queue: マルチスレッドの利用を想定されているため、今回はオーバースペック。

```Python3
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        current_depth = 1
        waiting_queue = deque()
        waiting_queue.append((root,current_depth))

        while len(waiting_queue):
            node, depth = waiting_queue.popleft()
            current_depth = max(current_depth, depth)
            if node.left is not None:
                waiting_queue.append((node.left, current_depth + 1))
            if node.right is not None:
                waiting_queue.append((node.right, current_depth + 1))
        
        return current_depth
```

時間計算量: O(N)
空間計算量: O(N)

## Step2

### 2.1 まずは自分で他の手段を実装してみる
深さ優先で実装してみた

```Python3
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        node_stack = [(root,1)]
        max_depth = 1
        while len(node_stack):
            node, depth = node_stack.pop()
            max_depth = max(max_depth, depth)
            if node.right is not None:
                node_stack.append((node.right, depth + 1))
            if node.left is not None:
                node_stack.append((node.left, depth + 1))         
        return max_depth
```
時間計算量: O(N)
空間計算量: O(N)

再帰でも実装してみる
```Python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        left_node_depth = self.maxDepth(root.left)
        right_node_depth = self.maxDepth(root.right)
        return max(left_node_depth, right_node_depth) + 1
```

### 2.2 コメント集や他の人のコードを読む

- 再帰のDFSとstackのDFSの違い
  - https://discord.com/channels/1084280443945353267/1227073733844406343/1236235351140339742
  - 再帰は下から上げてくる、stackは上から配る
  - 再帰で上から配る、stackで下から上げるも可能
- BFSは深さごとにまとめて処理する方法もある
  - https://github.com/kazizi55/coding-challenges/pull/21
- BFS: 層ごとに処理
  - https://github.com/mt2324/leetcode/pull/15/changes

再帰で上から配るver
- nolocalを使う
  - https://docs.python.org/ja/3.5/reference/simple_stmts.html?highlight=nonlocal#the-nonlocal-statement
  - 一つ外側の変数を参照

```Python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        max_depth = 0
        def depth(node: Optional[TreeNode], current_depth: int):            
            if node is None:
                return
            nonlocal max_depth
            max_depth = max(max_depth, current_depth)
            depth(node.right, current_depth + 1)
            depth(node.left, current_depth + 1)

        depth(root, 1)
        return max_depth
```

stackで下から上げるver

```Python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        node_to_check = [(root, False)] # (node, 帰りがけかどうかフラグ)
        depth = {}
        while node_to_check:
            node, isBack = node_to_check.pop()
            if isBack:
                # 自分の深さを登録する
                leftDepth = depth.get(node.left, 0)
                rightDepth = depth.get(node.right, 0)
                depth[node] = max(leftDepth, rightDepth) + 1
            else:
                if node is None:
                    continue
                node_to_check.append((node, True))
                node_to_check.append((node.right, False))
                node_to_check.append((node.left, False))
        return depth.get(root, 0)
```
## Step3


```Python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        frontier = [root]
        depth = 0
        while frontier:
            next_frontier = []
            for node in frontier:
                if node.left is not None:
                    next_frontier.append(node.left)
                if node.right is not None:
                    next_frontier.append(node.right)
            depth += 1
            frontier = next_frontier
        return depth
```