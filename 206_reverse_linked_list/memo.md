# 206. Reverse Linked List

Given the head of a singly linked list, reverse the list, and return the reversed list.

Constraints:

The number of nodes in the list is the range [0, 5000].
-5000 <= Node.val <= 5000

```Python3
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

## Step1

- ノードの数からstackに先頭から積んでいって
- 積み終わったらスタックから取り出していて連結リストを作る

```Python3
from collections import deque
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Noneのチェックしなくても通りはする（好みの範囲？）
        if not head:
            return None

        node = head
        stack = deque()
        while node is not None:
            stack.append(node.val)
            node = node.next

        # 分岐を減らすために番兵を利用
        reverse_dummy = ListNode()
        reverse_node = reverse_dummy
        while stack:
            val = stack.pop()
            reverse_node.next = ListNode(val)
            reverse_node = reverse_node.next
        return reverse_dummy.next
```
- ネストしてはいないものの、ループが二つあるのが気になる。。。もっといいやり方ないかな。。。

- 時間計算量: O(n)
- 空間計算量: O(n)

## Step2

- 手作業でやると考えた時に、一度stackに積むのは非効率
- 手作業でやるならば：元の連結リストの先頭要素と同じ値の要素を作りそこを基準に、元の連結リストの要素に相当する要素を作って新しい反転させるリストの先頭に持っていく
    - 新しいリストを作らず元のリストをそのままいじるやり方もありそう
```Python3
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        original_node = head
        # 前のループでの反転させたリストの先頭
        reverse_head = None
        while original_node is not None:
            reverse_head = ListNode(original_node.val, reverse_head)
            original_node = original_node.next
        return reverse_head
```

- https://github.com/t0hsumi/leetcode/pull/7#discussion_r1875385145
    - 渡されたリストを直接いじって繋ぎかえるパターン
    - ひっくり返したリストの先頭、ひっくり返す前の先頭を持っておけばよし
        - 手作業:
            - 0. ひっくり返す前の先頭を保存（「元の要素」とする）
            - 1. ひっくり返す前の先頭を次の要素に移動
            - 2. 「元の要素」をひっくり返す前の先頭に繋ぎ変え
            - 3. ひっくり返す前の先頭を「元の要素」に更新
    - メモリ使用量は新しいリストを作らない分こっちの方が抑えられる
    - ノード数の制約と引数で渡された連結リストを破壊的に変更するかどうかを考えると個人的には新しい反転リストを作る方法の方が好み
```Python3
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        original_head = head
        reverse_head = None
        while original_head is not None:
            original_node = original_head
            original_head = original_head.next
            original_node.next = reverse_head
            reverse_head = original_node
        return reverse_head
```

- https://github.com/irohafternoon/LeetCode/pull/7#discussion_r2019076979
    - リンクを中心に見る
```Python3
class Solution:
    def reverseList(self, head):
        # reverse_head, head, original_nextのリンクの繋ぎ変え
        reverse_head = None
        while head:
            original_next = head.next
            head.next = reverse_head
            reverse_head = head
            head = original_next
        return reevrse_head
```

- https://discord.com/channels/1084280443945353267/1231966485610758196/1239417493211320382
    - > 自分よりも下流を逆順にして、頭と尻尾の輪っかを渡してください
    - お尻は下流に渡したノードになっているので省略可能

- https://github.com/goto-untrapped/Arai60/pull/27#discussion_r1638693522
    - 下流に渡す時の選択肢
        - 1. 反転した上流と残りを下流に渡して全て反転してもらう（行きがけ）
        - 2. 残りを渡してそこだけ反転したものを返してもらい（先頭と末尾があればよい）、それを利用して上流も反転（帰りがけ）

1）
```Python3
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        def reverse_helper(reversed_node: Optional[ListNode], rest_node: Optional[ListNode]) -> Optional[ListNode]:
            if rest_node is None:
                return reversed_node
            next_rest = rest_node.next
            rest_node.next = reversed_node
            return reverse_helper(rest_node, next_rest)
        return reverse_helper(None, head)
```

2）
```Python3
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        def reverse_helper(node: Optional[ListNode]) -> Tuple[Optional[ListNode], Optional[ListNode]]:
            if node is None:
                return None, None
            if node.next is None:
                return node, node
            tail = node.next
            node.next = None # reverseListを呼ぶ前にやっても後にやっても変わらなさそう（どういう違いがあるのかが言語化できなかった）
            reversed_head, reversed_tail = reverse_helper(tail)
            reversed_tail.next = node
            return reversed_head, node
        return reverse_helper(head)[0]
```

2-1） 実はtailは不要（上でnode.next is Noneの時にnode, nodeと二つ同じものを返しているところに違和感を感じて気づく？）
```Python3
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None:
            return None
        if head.next is None:
            return head
        next_head = head.next
        head.next = None
        reversed_head = self.reverseList(next_head)
        next_head.next = head
        return reversed_head
```
- https://github.com/resumit30minutes/leetcode-arai60-practice/pull/8/files#diff-56cce9af784f5c572f0706e03269e28af28f8aabbface21c32e6199d6400c657
- https://github.com/quinn-sasha/leetcode/pull/7#discussion_r1948355100
    - stackを利用する場合でもNodeのまま次へのつながりを切ってstackに積むやり方もあり
    - 値をstackに積んでからstackからひとつつづ取り出して新しくNodeを作るよりメモリ使用量は少なくなりそうだが、ノード数の制約から値をstackに積む方が好み

- https://github.com/nanae772/leetcode-arai60/pull/8/files#r2324800451
    - 再帰の上限を上げるのは好ましくないかも

# Step3

```Python3
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        reversed_head = None
        while head is not None:
            reversed_head = ListNode(head.val, reversed_head)
            head = head.next
        return reversed_head
```