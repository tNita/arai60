# 112. Path Sum

Given the root of a binary tree and an integer targetSum, return true if the tree has a root-to-leaf path such that adding up all the values along the path equals targetSum.

A leaf is a node with no children.

The number of nodes in the tree is in the range [0, 5000].
-1000 <= Node.val <= 1000
-1000 <= targetSum <= 1000

## Step1
- 根から葉までの最短時間を求める感じ
- 深さ優先で良いか
  - ノードと、そのノードの親までのpathの和の二つをスタックに積む。 
  - 幅優先でも解けるが、葉の一つ前の層までは全ノードを見ないといけず、
- 深さ優先と比べると無駄が多い。
- 再帰はやめておく。再帰数がmax5000

```Python3
class Solution:
    def hasPathSum(self, root: TreeNode | None, targetSum: int) -> bool:
        def is_leaf(node: TreeNode) -> bool:
            return node.left is None and node.right is None

        if root is None:
            return False

        frontier = [(root, 0)]
        while len(frontier) > 0:
            node, parent_sum = frontier.pop()
            node_sum = parent_sum + node.val
            if is_leaf(node) and node_sum == targetSum:
                return True
            if node.right is not None:
                frontier.append((node.right, node_sum))
            if node.left is not None:
                frontier.append((node.left, node_sum))
        return False
```
- 時間計算量: ノード数に比例するのでO(N)
- 空間計算量: stackが木の高さに比例する、偏りがある木の可能性もあるのでO(N)


## Step2
### 自分の回答について

再帰でも書く。

```Python3
class Solution:
    def hasPathSum(self, root: TreeNode | None, targetSum: int) -> bool:
        def is_leaf(node: TreeNode) -> bool:
            return node.left is None and node.right is None
        
        def has_leaf_val(node: TreeNode | None, target_val: int) -> bool:
            if node is None:
                return False
            if is_leaf(node):
                return node.val == target_val
            child_target_val = target_val - node.val
            return has_leaf_val(node.left, child_target_val) or has_leaf_val(node.right, child_target_val)
        
        return has_leaf_val(root, targetSum)
```

- 時間計算量: T(N) = 2*T(N/2) +1→O(N)
- 空間計算量: 同時に使われるメモリは最大木の高さ分→O(logN)

AIレビュー（by GPT-6）

再帰の計算量について
>`T(N) = 2*T(N/2) + 1` について 
> 左右の部分木が、それぞれ半分の大きさになる前提が入っていますね。問題に、その保証はあるでしょうか。子が一つしかない木を描いてみると、この式にはなりません。
>「木の高さ分 → O(logN)」について 
> 木の高さを H とすると O(H) まではよいです。しかし、H が O(logN) になるのは平衡な場合ですね。今回は一本道の木も入力されるので、最悪 H = N、補助空間は O(N) です。Step1 で「偏りがある木の可能性」を考えられているので、その同じ木を Step2 にも当てはめてみてください。

- 平衡木と勘違いしていた
  - 時間計算量は最大でノードすべて見ないといけないのでO(N)
  - 空間計算量も木が偏っていた場合はO(N)

> 「BFS は DFS より無駄が多い」とは限りません。この実装は左を先に探索します。根の左に長い一本道、右に条件を満たす葉を置くと、BFS のほうが早く見つかります。答えがなければ、どちらも全ノードを調べますね。

- 平衡木ではないので、DFSが良いとは言い切れない


### コメント集・他の人のコード
- https://github.com/SuperHotDogCat/coding-interview/pull/37#discussion_r1665891252
  - stackに引いた結果を積む
- https://github.com/kazuki-official/leetcode/pull/25
  - targetSumから自分の値を引く方式で処理する
```Python3
class Solution:
    def hasPathSum(self, root: TreeNode | None, targetSum: int) -> bool:
        if root is None:
            return False
        if root.left is None and root.right is None:
            return root.val == targetSum
        rest = targetSum -root.val
        return self.hasPathSum(root.left, rest) or self.hasPathSum(root.right, rest) 
```

- https://github.com/fuga-98/arai60/pull/25
  - f() or g()でfがtrueならばgは評価されない。短絡評価
  - https://docs.python.org/ja/3.6/library/stdtypes.html?highlight=set
- https://github.com/naoto-iwase/leetcode/pull/29
  - https://github.com/naoto-iwase/leetcode/pull/29/changes#r2455081026
  - True/Falseではなく実際の経路を返却する形だったら？
    - 和とそこまでのpathを記録しておくのが素直か？
    - データ構造的に子から親へは行けないので、対象の葉
  - 下に行くにつれて和が単調増加するならば枝刈りできる

## Step3
```Python3
class Solution:
    def hasPathSum(self, root: TreeNode | None, targetSum: int) -> bool:
        if root is None:
            return False
        frontier = [(root, 0)]
        while len(frontier) > 0:
            node, parent_sum = frontier.pop()
            leaf = node.left is None and node.right is None
            node_sum = parent_sum + node.val
            if leaf and node_sum == targetSum:
                return True
            if node.right is not None:
                frontier.append((node.right, node_sum))
            if node.left is not None:
                frontier.append((node.left, node_sum))
        return False
```