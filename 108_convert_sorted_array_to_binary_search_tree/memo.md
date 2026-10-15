# 108. Convert Sorted Array to Binary Search Tree

Given an integer array nums where the elements are sorted in ascending order, convert it to a height-balanced binary search tree.

- 1 <= nums.length <= 10^4
- -10^4 <= nums[i] <= 10^4 
- nums is sorted in a strictly increasing order.

## Step1

- 真ん中を親。左半分を左の子を頂点とする部分木、右半分を右の子を頂点とする部分木とする形できを作っていく。
- 再帰はさける、再帰数はノード数分になるため 
- 幅優先、深さ優先どちらでもできそう、すべてのノードを見る必要あるため大きな優劣はなし→幅優先を選択

- 実行時間: 10^4 / 10^7 = 1msec程度

```Python3
class Solution:
    def sortedArrayToBST(self, nums: list[int]) -> TreeNode | None:
        if not nums:
            return None

        dummy = TreeNode()
        # 親ノード、方向、開始位置（閉区間）、終了位置（開区間）
        nodes = [(dummy, "left", 0, len(nums))]
        while len(nodes) > 0:
            next_nodes = []
            for parent_node, direction, start, end in nodes:
                middle = (start + end) // 2
                node = TreeNode(val=nums[middle])
                if direction == "left":
                    parent_node.left = node
                else:
                    parent_node.right = node
                if start < middle:
                    next_nodes.append((node, "left", start, middle))
                if middle + 1 < end:
                    next_nodes.append((node, "right", middle + 1, end))
            nodes = next_nodes
        return dummy.left
```
- 時間計算量: O(N)
- 空間計算量: O(N)


## Step2
### AIレビュー（by GPT 6）

>  「再帰数はノード数分になるため」では、再帰を避ける根拠として不十分です。スタック使用量を決めるのは、同時に積まれる呼び出しの深さです。 この構築方法では毎回区間をほぼ半分にするので、深さは O(log N) です。N = 10^4 でも木の高さは14、空区間の呼び出しまで含めて15段程度です。この問題では、再帰も十分に検討できま す。

確かに、再帰の深さ=木の高さで、二分岐なので再帰数は最大でもlog2 10^4 = 13.2..

そのため再帰も十分選択肢に入る。

再帰で実装してみる
```Python3
class Solution:
    def sortedArrayToBST(self, nums: list[int]) -> TreeNode | None:
        if len(nums) == 0:
            return None
        middle = 0 + len(nums) // 2
        left_node = self.sortedArrayToBST(nums[:middle])
        right_node = self.sortedArrayToBST(nums[middle + 1:])
        return TreeNode(nums[middle], left_node, right_node)
```

> 幅優先と深さ優先は、保持する作業量が異なります。 — memo.md:12 (108_convert_sorted_array_to_binary_search_tree/memo.md:12)
> 全ノードを見るため、どちらも時間計算量は O(N) です。ただし、この平衡な木では、幅優先は最大幅に応じた O(N)、深さ優先は O(log N) の補助空間で処理できます。出力の木自体には、 どちらも O(N) 必要です。 

深さ優先、幅優先どちらにするかの根拠は以下のような感じで述べれると良かったか。

- 深さ優先はstackに入れるのは深さ分（O(log N)）、幅優先の場合はqueueに入れるのは最下層の幅分（O(N)）となり、この点だけ見れば深さ優先の方がメモリ消費量を抑えられる
- ただ、出力する木のメモリ使用量がどちらもO(N)でこちらが支配的なので、幅優先と深さ優先の大きな優劣は無さそう

### コメント集、他の人のコード
- https://github.com/irohafternoon/LeetCode/pull/27#discussion_r2060734803 
  - メモリリークについて（C++）
  - ダミーノードを生成してからスタックに入れるため、スタックからpopしたときにノードがない場合はダミーノードが入っているメモリを解放しないといけない。という感じか？
- https://github.com/naoto-iwase/leetcode/pull/23
  - 配列自体をstackに積んでいる（好みの範囲）
  - setattrは強力だが好まれない。Javaのリフレクションも同じ類か
- https://github.com/kazuki-official/leetcode/pull/24
  - 自分は[start, end)で範囲を取っていたが、この方の実装では[first, last]で範囲を取っている（一貫していればOK、どっちを取るのかは好みの範囲か）
- https://github.com/mamo3gr/arai60/pull/23
  - `if len(nums) == 1:`の時は、再帰せずにreturnする方法
  - numsの要素が一つの時も通常の再帰に流し、left, rightに要素0個の配列を渡すという方が、再帰が終了するタイミングが一つになってシンプルで好き
- https://github.com/fuga-98/arai60/pull/24
  - 再帰の解き方
    - スライスにはO(k)（kは取得する要素分、新しいリストを作ってそこに取り出した分を詰めて返すため
    - 計算量を漸化式から算出
      - スライスなし：T(n) = 2*T(n/2) + 1なので、マスターの定理からO(n^log2(2)) = O(n)
      - スライスあり：T(n) = 2*T(n/2) + f(n) なので、マスターの定理からO(n ^ log2(2) * logn) = log(n logn)
    - > - 空間計算量は時間計算量を超えることはない
      > - 一般的な計算モデル（例えば、ティューリングマシン）では、各計算ステップでアクセスできる記憶領域が限られているため、T(n) 回の計算を行うアルゴリズムは最大で T(n) 個のセルにしかアクセスできず、空間計算量は時間計算量の上限に収まります。
- https://github.com/hayashi-ay/leetcode/pull/29
  - 親のノードをスタックに積む場合、方向（自分のStep1実装のdirection）はスタックに積まず、動的に判断という方法もある
  - middleの値が親のノードより小さければ親の左に来る、そうでなければ右に来ると判断できる
  - dummyは値をinfとして作っておけばleftにほしい二分岐が来ることが保証できるか

## Step3

```Python3
class Solution:
    def sortedArrayToBST(self, nums: list[int]) -> TreeNode | None:
        if len(nums) == 0:
            return None
        middle = len(nums) // 2
        return TreeNode(
            val=nums[middle],
            left=self.sortedArrayToBST(nums[:middle]),
            right=self.sortedArrayToBST(nums[middle + 1:])
        )
```

