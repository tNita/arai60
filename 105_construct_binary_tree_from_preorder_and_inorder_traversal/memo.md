# 105. Construct Binary Tree from Preorder and Inorder Traversal

Given two integer arrays preorder and inorder where preorder is the preorder traversal of a binary tree and inorder is the inorder traversal of the same tree, construct and return the binary tree.

Constraints:

- 1 <= preorder.length <= 3000
- inorder.length == preorder.length
- -3000 <= preorder[i], inorder[i] <= 3000
- preorder and inorder consist of unique values.
- Each value of inorder also appears in preorder.
- preorder is guaranteed to be the preorder traversal of the tree.
- inorder is guaranteed to be the inorder traversal of the tree.

## Step1

- preorder、inorderの２つの配列から木の形状を特定せよという問題
- preorderとinorderの性質を利用する
  - preorder: 根、左部分木のpreorder、右部分木のpreorder
  - inorder: 左部分木のinorder、根、右部分木のinorder
  - 今回はノードの値がぶつからないのでinorderの根の位置を位置位に特定できる
- 再帰的に処理できそう
  - 左部分木（右部分木）のpreorder, inorderを渡して左部分木（右部分木）を構築させる
  - 根のノードを作って、上で作った左、右部分木につなげる
- 木が偏っていた場合は再帰の深さが最大3000（ノード数）> 1000になるので、DFSのスタックで実装する
  - 元々の案は下から上げてくるタイプだが、上から配る形に読み替えて実装する
- ノードの値が被らないので、木を一意に特定できるが、被る場合は複数の木を構築できる
  - その場合は候補の木を複数リストで持っておくのが良いか（後で実装してみる）
  
- 一旦ノードの値の重複がないとして実装

- Acceptしない。。。何かの想定が間違っているはずだが、わからない。。。
```Python3
class Solution:
    def buildTree(self, preorder: list[int], inorder: list[int]) -> TreeNode | None:
        if len(preorder) != len(inorder):
            raise ValueError("preorderとinorderは同じ要素数である必要があります。")
        if not preorder:
            raise ValueError("preorderとinorderは要素数が一つ以上である必要があります。")
        dummy = TreeNode()
        # 親、左の子かどうか、preorder、inorder
        nodes = [(dummy, True, preorder, inorder)]
        while nodes:
            parent, is_left, preorder, inorder = nodes.pop()
            node = TreeNode(preorder[0])
            if is_left:
                parent.left = node
            else:
                parent.right = node
            node_inorder_index = inorder.index(node.val)

            right_preorder_start = 1
            # 左があるとき
            if node_inorder_index > 0:
                # inorderの左部分木の最後の要素はpreorderの左部分期の最後の要素と同じになる（どちらも右端のノード）
                right_preorder_start = preorder.index(inorder[node_inorder_index - 1]) + 1
                nodes.append((node, True, preorder[1: right_preorder_start], inorder[: node_inorder_index]))
            # 右があるとき
            if node_inorder_index < len(inorder) - 1:
                nodes.append((node, False, preorder[right_preorder_start:], inorder[node_inorder_index + 1:]))
        return dummy.left
```
- 仕方がないのでleetcodeのテストケースを使ってデバッグしてみる
> inorderの左部分木の最後の要素はpreorderの左部分期の最後の要素と同じになる（どちらも右端のノード）
- これが間違っていることに気づいた
- 例えば以下のケースでは成り立たない
```text
    1
   /  \
  2    4
 /
3
```
- preorder = [1, 2, **3**, 4]
- inorder = [3, **2**, 1, 4]

- inorderは即座に左と右に分けれるので、左のinorderを使ってpreorderの左部分を特定する
  - ただし、すべての要素が異なることを前提にした実装。要素の重複があるとして実装するやり方は思いつかなかった
```Python3
class Solution:
    def buildTree(self, preorder: list[int], inorder: list[int]) -> TreeNode | None:
        if len(preorder) != len(inorder):
            raise ValueError("preorderとinorderは同じ要素数である必要があります。")
        if not preorder:
            raise ValueError("preorderとinorderは要素数が一つ以上である必要があります。")

        dummy = TreeNode()
        # 親、左の子かどうか、preorder、inorder
        nodes = [(dummy, True, preorder, inorder)]
        while nodes:
            parent, is_left, preorder, inorder = nodes.pop()
            node = TreeNode(preorder[0])
            if is_left:
                parent.left = node
            else:
                parent.right = node
            node_inorder_index = inorder.index(node.val)
            left_inorder = inorder[:node_inorder_index]
            right_inorder = inorder[node_inorder_index + 1:]

            left_preorder_end = 1
            if left_inorder:
                while left_preorder_end < len(preorder):
                    if preorder[left_preorder_end] not in left_inorder:
                        break
                    left_preorder_end += 1
                nodes.append((node, True, preorder[1:left_preorder_end], left_inorder))
            if right_inorder:
                nodes.append((node, False, preorder[left_preorder_end:], right_inorder))      
        return dummy.left
```
- 時間計算量: O(N^3)
  - ノード数分処理をする：O(N)
  - ノード一つの処理に対して、左のpreorderの範囲特定のためにpreorderの左端から一つづつ見ていく必要がある: O(N^2)
- 空間計算量: O(N^2)
  - 木の高さ分とpreorder, inorderのリスト分

- 一部Time Limited Exceeded

## Step2
### AIレビュー

> 左部分木の境界は、要素の探索ではなく個数で決まります
- 言われてみればそれはそう

> 最初の誤りは、走査の末尾の意味を小さい例で確かめたいです

> 時間計算量 O(N^3) は妥当ですが、入力の形まで説明しましょう
> 最後の実装では、サイズ m の部分木について、最大 O(m) 回のループの各回でリストへの所属確認に O(m) かかります。左一列の木なら、サイズ N, N−1, …, 1 の部分木でこの処理を繰り返すため、合計は O(N^3) です。
- N^2 + (N-1)^2 + ....+ 1なので、O(N^3)ということか。

> 現在のスタック実装のピーク空間は O(N) です
> 「木の高さ分 × 配列の長さ」で O(N^2) とするのは、このコードには当てはまりません。スタックに同時に入っている仕事は互いに重ならない部分木なので、それらが持つ preorder / inorder の要素数の合計は O(N) です。処理中の配列や一時的なスライスを含めても O(N) に収まります。出力の木も O(N) です。
- なるほど。
- スタックに何が入るのかイメージしきれていなかった。

### コメント集や他の人のコード
- https://discord.com/channels/1084280443945353267/1233603535862628432/1289056088334925888
  - まずは小さい例から始める
  - 順序付き根付き木の総数はカタラン数
  - > 異なる2つの木で Preorder と Inorder が同じになっちゃうような場合って本当にないの。
    - ノード数3, 4の場合を試したが、どの木もinorderが異なる
    - inorderではどのノードにおいても左部分木→ノード→右部分木の順という性質
    - 木が異なるとどこかノードの左部分木または右部分木のノード数が異なるので、inorderの配列の並びも異なる
- preorderを先頭から順に見ていく
  - https://github.com/kazukiii/leetcode/pull/30/changes/BASE..ab2dbb435e41621f4b7e17de01e8afcf984af434#r1821506570
  - https://github.com/nittoco/leetcode/pull/37#discussion_r1821720967
  - stackに親の候補とその親の左右の子のmax（inorderでの位置のmax）を積む
  - preorderを一つづつみて木を構築。そのときにstackから親の候補を取り出して親になりうるか調査
    - 各ノード対する手作業の手順
      1. スタックからpeekして得れる親候補に対して左の子になりうるかチェック
        - YESの場合は左の子に設定してスタックに積んで終了 
      2. スタックからpeekして得れる親候補に対して右の子になりうるかチェック
        - YESの場合は右の子に設定してスタックに積んで終了
        - NOの場合はスタックからpopして、再度2をやる
          - ノードの処理を始める前のstackの一番上しか左の子になりうることはない
          - 親、左の子はpreorder上では隣り合っているため
- inorderを先頭から順に見ていく
  - https://github.com/kazukiii/leetcode/pull/30/changes/BASE..ab2dbb435e41621f4b7e17de01e8afcf984af434#r1821628634
  - https://github.com/fuga-98/arai60/pull/29#discussion_r2020242408
  - https://github.com/tarinaihitori/leetcode/pull/29#discussion_r2044913447
  - 手作業でやると
    - スタックには親が決まっていないノードを積んでおく（inorderの性質上、右の子も設定されていない）
    - ノードの左部分木はすでにstack上にあるので、ノードの左の子を設定してスタックに積んでおく
      - 右側もつなげて左部分木を完成形にしてから左部分木の根をノードの左の子として設定する
    - inorderは左部分木→根→右部分木の順
      - 特定のノード nodeから見ると
        - preorderにおいてnodeより前にあるノード: nodeより上のノード全体とそれらのノードの各左部分木。
        - preorderにおいてnodeより後ろにあるノード: nodeの左右部分木と上のノードの各右部分木。
          - nodeの左部分木のみ、inorder上でnodeよりも前にある
- Cartesian Tree構成法
  - Cartesian Tree : 配列が与えられたとき、その配列の最小要素を根とし、配列上の根より左部分を左部分木、右部分を右部分木として再帰的に構築される木
    - https://en.wikipedia.org/wiki/Cartesian_tree
  - 今回の例での対応関係
    - 配列: inorder
    - 配列の要素の値の大小関係: preorderでの出現順
  - https://discord.com/channels/1084280443945353267/1478763507963924522/1492871022511390843
  - ノード3つの例で以下の実装が正しそうなことはわかったがイマイチ腑に落ちない（一つ一つの操作（「点」）は理解できるが、「点」と「点」が「線」として繋がらない感覚。。。この実装で絶対大丈夫って言い切れない）
```Python3
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        priority = {val: i for i, val in enumerate(preorder)}
        # [1, 2, 3...] で、1.right = 2, 2.right = 3, ...となっている（つまり、N-1番目のルートの右の子にはN番目のルートが設定されている）
        stack = []
        for val in inorder:
            # stackの各ノード見てこのノードは右下or右上方面にある
            node = TreeNode(val)
            # nodeからみて下のものを取り出す。
            # stackから左部分木を探してnode.leftに設定する
            while stack and priority[stack[-1].val] > priority[val]:
                # 左側の親→stackから取り出す
                node.left = stack.pop()
            # ここまで来たらstackにあるものはnodeより上
            # stackに入っている右端の右部分木にあるので、一旦右端のrightにつなげておく。（stack[-1]の右の子が直接nodeである場合もあれば、間に他のノードが挟まっていることもある。後者の場合は次のイテレーションでstackから取り除かれる）
            if stack:
                stack[-1].right = node
            stack.append(node)
        return stack[0]
```
- https://github.com/Yoshiki-Iwasa/Arai60/pull/33#discussion_r1688357607
  - numpyのarray.arrayを使うと、コピーじゃないスライスができる
- https://github.com/olsen-blue/Arai60/pull/29#discussion_r1948256437
  - 内包表記も可能
- https://github.com/naoto-iwase/leetcode/pull/34
  - preorderの順でみていくやり方、inorderも前から進める
    - 右に行くときにinorderを進めるイメージか？（理解度怪しい）
      - 右上に行く：stackから取り出す
      - 右下に行く：右の子にノードを設定
  - 根を元にinorderを左右の子に二分できることを利用する
    - subtreesに深さ優先に積むので、取り出したときにpreorderと同じ順番で取り出される

## Step3

- preorder
```Python3
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        inorder_value_to_index = {value: i for i, value in enumerate(inorder)}
        dummy = TreeNode()
        stack = [(dummy, len(inorder))]
        for value in preorder:
            node = TreeNode(value)
            node_inorder_index = inorder_value_to_index[value]
            prev_node, prev_inorder_index = stack[-1]
            if node_inorder_index < prev_inorder_index:
                prev_node.left = node
                stack.append((node, node_inorder_index))
                continue
            stack.pop()
            while node_inorder_index > stack[-1][1]:
                prev_node, _ = stack.pop()
            prev_node.right = node
            stack.append((node, node_inorder_index))
        return dummy.left
```

- inorder
```Python3
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        preorder_value_to_index = {value: i for i, value in enumerate(preorder)}
        stack = []
        def gather(parent_preorder_index):
            child = None
            while stack:
                node, node_preorder_index = stack[-1]
                if node_preorder_index < parent_preorder_index:
                    break
                node.right = child
                child = node
                stack.pop()
            return child
        for value in inorder:
            node = TreeNode(value)
            node_preorder_index = preorder_value_to_index[node.val]
            node.left = gather(node_preorder_index)
            stack.append((node, node_preorder_index))
        return gather(-1)
```

- inorderの実装は少ししっくりこない（どんな構造でもちゃんと動くか？）

