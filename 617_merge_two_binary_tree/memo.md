# 617. Merge Two Binary Trees

You are given two binary trees root1 and root2.

Imagine that when you put one of them to cover the other, some nodes of the two trees are overlapped while the others are not. You need to merge the two trees into a new binary tree. The merge rule is that if two nodes overlap, then sum node values up as the new value of the merged node. Otherwise, the NOT null node will be used as the node of the new tree.

Return the merged tree.

Note: The merging process must start from the root nodes of both trees.

制約：
The number of nodes in both trees is in the range [0, 2000].
-10^4 <= Node.val <= 10^4


## Step1

- 幅優先でも深さ優先でも解ける 
- 二つの木のノード全てを見る必要がある
- 木の深さは最高2000→Pythonの再帰の上限のデフォルトは1000なので、再帰の利用は防ぐ
- 計算量
  - Time: O(N)
    - whileの中は12step→15 * 2000 / 10^7 = 3 msec
  - Space: O(N)
```Python3
class Solution:
    def mergeTrees(self, root1: TreeNode | None, root2: TreeNode | None) -> TreeNode | None:
        if root1 is None and root2 is None:
            return None
        
        def sum_node_val(node_1, node_2):
            sum_val = 0
            sum_val += node_1.val if node_1 else 0
            sum_val += node_2.val if node_2 else 0
            return sum_val

        merged_root = TreeNode()
        frontier = [(root1, root2, merged_root)] # 一つ目と二つ目はどっちかがnot None, 3つ目はnot Noneでleftとrightは未接続
        while frontier:
            node1, node2, merged_node = frontier.pop()
            merged_node.val = sum_node_val(node1, node2)
            node1_left = node1.left if node1 else None
            node1_right = node1.right if node1 else None
            node2_left = node2.left if node2 else None
            node2_right = node2.right if node2 else None
            if node1_right or node2_right:
                merged_node.right = TreeNode()
                frontier.append((node1_right, node2_right, merged_node.right))
            if node1_left or node2_left:
                merged_node.left = TreeNode()
                frontier.append((node1_left, node2_left, merged_node.left))
        return merged_root
```

- whileの中で、今のノードがNoneなのか子のノードがNoneなのかを区別して考える必要がある

## Step2

### 自分で

BFS
```Python3
class Solution:
    def mergeTrees(self, root1: TreeNode | None, root2: TreeNode | None) -> TreeNode | None:
        if root1 is None and root2 is None:
            return None
        
        def sum_node_val(node_1, node_2):
            sum_val = 0
            sum_val += node_1.val if node_1 else 0
            sum_val += node_2.val if node_2 else 0
            return sum_val

        merged_root = TreeNode()
        nodes = [(root1, root2, merged_root)] # 一つ目と二つ目はどっちかがnot None, 3つ目はnot Noneでleftとrightは未接続
        while nodes:
            next_nodes = []
            for node1, node2, merged_node in nodes:
                merged_node.val = sum_node_val(node1, node2)
                node1_left = node1.left if node1 else None
                node1_right = node1.right if node1 else None
                node2_left = node2.left if node2 else None
                node2_right = node2.right if node2 else None
                if node1_left or node2_left:
                    merged_node.left = TreeNode()
                    next_nodes.append((node1_left, node2_left, merged_node.left))
                if node1_right or node2_right:
                    merged_node.right = TreeNode()
                    next_nodes.append((node1_right, node2_right, merged_node.right))
            nodes = next_nodes
        return merged_root

```

一応再帰でやっている

```Python3
class Solution:
    def mergeTrees(self, root1: TreeNode | None, root2: TreeNode | None) -> TreeNode | None:
        if root1 is None and root2 is None:
            return None
        def sum_node_val(node_1, node_2):
            sum_val = 0
            sum_val += node_1.val if node_1 else 0
            sum_val += node_2.val if node_2 else 0
            return sum_val
        merged_root = TreeNode(val = sum_node_val(root1, root2))
        # 帰りがけ
        root1_left = root1.left if root1 else None
        root1_right = root1.right if root1 else None
        root2_left = root2.left if root2 else None
        root2_right = root2.right if root2 else None
        merged_root.left = self.mergeTrees(root1_left, root2_left)
        merged_root.right = self.mergeTrees(root1_right, root2_right)
        return merged_root
```

### AIからの指摘 （by GPT-6）

>  32行目以降 (617_merge_two_binary_tree/memo.md:32)は、左右の子を4つ取り出してから接続しています。右の子2つを取り出して右を接続し、その後に左を処理すると、同時に追う変数が減ります

好みの範囲だと思うが、確かに指摘のやり方のほうが良いかも。自分もこちらのほうが好き。

```Python3
node1_right = node1.right if node1 else None
node2_right = node2.right if node2 else None
if node1_right or node2_right:
  merged_node.right = TreeNode()
  frontier.append((node1_right, node2_right, merged_node.right))
node1_left = node1.left if node1 else None
node2_left = node2.left if node2 else None
if node1_left or node2_left:
  merged_node.left = TreeNode()
  frontier.append((node1_left, node2_left, merged_node.left))
```

> 入力の部分木をそのまま利用するなら、片方しか存在しない部分木は走査せず接続できます。

確かに。
- 片一方がNoneのnodeの場合、そのノード配下の部分木は重なり合わない。
- つまり片一方がNoneのnode→統合した木のその位置から下は、他方のnodeを頂点とする木と同じ
- 一方で、入力の部分木を使い回すので、入力と出力の部分木が同じになってしまうのがマイナス点（例えば、このメソッド呼び出したあとに入力の部分木に変更があると、出力の部分木も変わってしまうことがある）→deepcopyすれば解消できそう

```Python3
class Solution:
    def mergeTrees(self, root1: TreeNode | None, root2: TreeNode | None) -> TreeNode | None:
        if root1 is None and root2 is None:
            return None

        merged_root = TreeNode()
        if not root1 and root2:
            return root2
        if root1 and not root2:
            return root1
        frontier = [(root1, root2, merged_root)] # 一つ目と二つ目はどちらもnot None, 3つ目はnot Noneでleftとrightは未接続
        while frontier:
            node1, node2, merged_node = frontier.pop()
            merged_node.val = node1.val + node2.val
            # right
            if node1.right and node2.right:
                merged_node.right = TreeNode()
                frontier.append((node1.right, node2.right, merged_node.right))
            if not node1.right and node2.right:
                merged_node.right = node2.right
            if node1.right and not node2.right:
                merged_node.right = node1.right

            # left
            if node1.left and node2.left:
                merged_node.left = TreeNode()
                frontier.append((node1.left, node2.left, merged_node.left))
            if not node1.left and node2.left:
                merged_node.left = node2.left
            if node1.left and not node2.left:
                merged_node.left = node1.left
        return merged_root
```

### コメント、他の人のコード

- https://discord.com/channels/1084280443945353267/1233603535862628432/1278020133628940395
  - 入力を破壊するか、出力が変更されると（意図せず）入力が変わってしまうか。
  - 入力と出力の部分木を共有してしまう問題は後者
- https://discord.com/channels/1084280443945353267/1262688866326941718/1297934906189549599
  - ダブルポインタ（ポインタのポインタ）を使う方法（C++やGoなど）
  - ダブルポインタに無染みなかった。以下の記事を読み、図も書いてみることである程度理解
    - ashi-developer.hatenablog.jp/entry/2022/11/29/093000
    - [図](pointer_and_double_pointer.svg)
  - ダブルポインタを使うことで、書き込む場所を一旦値はnilの状態でstackに積み、後で実際にノードがあればそのノードのアドレスに値を更新→こうすることで、ノードが存在するかどうかを処理対象のノードでできる（子の2つのノドに対して、2回存在チェックをやる必要がない）
- https://discord.com/channels/1084280443945353267/1295357747545505833/1329746604114055191
  - Pythonでダブルポインタでやったことと似たようなことをやる
- https://github.com/naoto-iwase/leetcode/pull/22
  - mergedの方は「親のノード」+「どっちの子か？」でノードを表現する方法もある
  - そうすれば、スタックに入れる前に、mergedのノードがNoneになりうるかチェックする必要がない
  - ノードをセットする場所をstackに積むという点で、ダブルポインタの話とも似ている
- https://github.com/nanae772/leetcode-arai60/pull/23
  - 下から上げる場合のstackの実装（リストを使って、ノードを上へ伝搬させる）
- https://github.com/kazuki-official/leetcode/pull/23
  - それぞれ3つの木に対してstackを用意

### 実際にポインタ / ダブルポインタで比較してみる

ダブルポインタ
```Go
type Nodes struct {
    Node1 *TreeNode
    Node2 *TreeNode
    Merged **TreeNode
}

func left(node *TreeNode) *TreeNode {
    if node == nil {
        return nil
    }
    return node.Left
}

func right(node *TreeNode) *TreeNode {
    if node == nil {
        return nil
    }
    return node.Right
}

func val(node* TreeNode) int {
    if node == nil {
        return 0
    }
    return node.Val
}

func mergeTrees(root1 *TreeNode, root2 *TreeNode) *TreeNode {
    var result *TreeNode
    var stack []Nodes
    stack = append(stack, Nodes{root1, root2, &result})
    for len(stack) != 0 {
        top := stack[len(stack) - 1]
        node1, node2, merged := top.Node1, top.Node2, top.Merged
        stack = stack[:len(stack) - 1]
        if node1 == nil && node2 == nil {
            continue
        }
        *merged = &TreeNode{Val: val(node1) + val(node2)}
        stack = append(stack, Nodes{right(node1), right(node2), &(*merged).Right})
        stack = append(stack, Nodes{left(node1), left(node2), &(*merged).Left})
    }
    return result
}
```
ポインタを使う場合

```Go
type Nodes struct {
    Node1 *TreeNode
    Node2 *TreeNode
    Merged *TreeNode
}

... （略）...

func mergeTrees(root1 *TreeNode, root2 *TreeNode) *TreeNode {
    if root1 == nil && root2 == nil {
        return nil
    }
    var result = &TreeNode{Val: 0} // ダミー
    var stack []Nodes
    stack = append(stack, Nodes{root1, root2, result})
    for len(stack) > 0 {
        top := stack[len(stack)-1]
        node1, node2, merged := top.Node1, top.Node2, top.Merged
        stack = stack[:len(stack)-1]
        merged.Val = val(node1) + val(node2)
        if right(node1) != nil || right(node2) != nil {
            merged.Right = &TreeNode{Val: 0}
            stack = append(stack, Nodes{right(node1), right(node2), merged.Right})
        }
        if left(node1) != nil || left(node2) != nil {
            merged.Left = &TreeNode{Val: 0}
            stack = append(stack, Nodes{left(node1), left(node2), merged.Left})
        }
    }
    return result
}
```

観察
- ダブルポインタのほうがシンプルに感じる
  - if文が一つになっている
  - stackに実体のノードを積むか、nilを積むかの違い
  - ダブルポインタのほうが手作業でやるときの手順に近い
    - 手作業でやるときに、子ノードが存在するかどうかチェックして、もしあればValは空欄の状態で子ノードを追加しておく。。。ということはしないはず
      - 存在チェックと値の計算が「離れて」しまう
    - ノードが存在するかどうかチェックして、存在するならばValを計算してノードを追加するという流れが自然

## Step3

```Python3
class Solution:
    def mergeTrees(self, root1: TreeNode | None, root2: TreeNode | None) -> TreeNode | None:
        def left(node: TreeNode):
            return node.left if node else None
        def right(node: TreeNode):
            return node.right if node else None
        
        def val(node: TreeNode):
            return node.val if node else 0
        
        dummy = TreeNode()
        nodes = [(root1, root2, dummy, "left")]
        while nodes:
            next_nodes = []
            for node1, node2, parent_merged_node, direction in nodes:
                if not node1 and not node2:
                    continue
                merged_node = TreeNode(val(node1) + val(node2))
                if direction == "left":
                    parent_merged_node.left = merged_node
                else:
                    parent_merged_node.right = merged_node
                
                next_nodes.append((left(node1), left(node2), merged_node, "left"))
                next_nodes.append((right(node1), right(node2), merged_node, "right"))
            nodes = next_nodes
        return dummy.left
```
## TODO

Rustに入門したら、ここを確認する

https://discord.com/channels/1084280443945353267/1251052599294296114/1289055268201824356