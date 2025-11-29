# 83. Remove Duplicates from Sorted List

## 問題

Given the head of a sorted linked list, delete all duplicates such that each element appears only once. Return the linked list sorted as well.


### 制約

Constraints:

The number of nodes in the list is in the range [0, 300].
-100 <= Node.val <= 100
The list is guaranteed to be sorted in ascending order.


```Python3
Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```


## Step1

- ソートされているのでそのまま前から順番に見ていく
- 副作用を避けるため、重複なし連結リストは新しく1から作る
  - たかだか元の連結リストと同じものがもうひとつできるだけで要素数を見ても新しく作っても問題なさそう
- 重複なし連結リストの先頭はheadの値のノード
- 前から順番に見て行く時に、重複なしリストの末尾のnodeの値と比較
  - 末尾のnodeの値と今見ているnodeが同じ値の時
  - 末尾のnodeの値と今見ているnodeが違う値の時
    - 今見ているnodeと同じ値を持つnodeを末尾のノードに繋ぐ
    - 末尾のノードをそのノードに更新

```Python3
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return None
        remove_duplicate_head = ListNode(head.val)
        remove_duplicate_tail = remove_duplicate_head
        node = head
        while node:
            if node.val != remove_duplicate_tail.val:
                remove_duplicate_tail.next = ListNode(node.val)
                remove_duplicate_tail = remove_duplicate_tail.next
            node = node.next
        return remove_duplicate_head
```


## Step2

- https://github.com/potrue/leetcode/pull/3
  - 副作用を避けた方がいいのかなと思ったがそうでもないのか。
  - まあ、関数のコメントに`# WARN: この関数は第一引数で渡されたheadを破壊的に変更します`と書いておけば良いか
  - nextとvalが同じ時にひとつ先のnode（next.next）に繋ぎ直すという発想か
  - ループするごとにnodeが進む場合もあれば変わらない場合もあり
  - パッと見ループが終了した時にきちんと重複要素を除外しきれているか直感的にわからない（末尾が不安）
    - 以下の終了パターンをみるに大丈夫そう
      - 末尾ふたつが重複要素である：末尾ひとつ前の要素をNone（node.next.next）に繋いで終了
      - 末尾ふたつが重複要素でない：末尾にnodeを進めて終了（要素の除外なし）

```Python3
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        node = head
        while node and node.next:
            if node.val == node.next.val:
                node.next = node.next.next
            else:
                node = node.next
        return head
```

- https://discord.com/channels/1084280443945353267/1195700948786491403/1196388760275910747
  - 確かにvalが同じをひとまとまりにして考えるのが素直
  - これだとループが終了した時に正しく重複要素を除外できていることが直感的にわかるので好み
  - group: valが同じもののまとまり
  - filter: 重複を除外
  - concat: 重複しない要素に繋ぎ直し

```Python3
while node:
    # ↓のループを1group
    while node.next and node.val == node.next.val:
        node.next = node.next.next # filter→concat
    # ↑のループを1group
    node = node.next
```

- https://github.com/TrsmYsk/leetcode/pull/3
  - valはintだろと決めつけていたが、型付けされているわけではないのでそうとは限らない
- https://github.com/docto-rin/leetcode/pull/3
  - 自分と似たような実装している方を参考に
  - remove_duplicate→deduplicateが良さそう
- https://github.com/docto-rin/leetcode/pull/3/files#r2393927727
  - 確かに再帰も可能か
  - 再帰についてコメント
    - https://discord.com/channels/1084280443945353267/1261259843671687188/1262997002891821056
    - > 前の人から数字を教えてもらうか、後ろの人から数字を教えてもらうか、なんらかの情報がないと仕事ができないですね。
    - この場合は後ろから教えてもらうのが良さそう

```Python3
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        next_head = deleteDuplicates(head.next)
        if head.val == next_head.val:
            head.next = next_head.next
        else:
            head.next = next_head
        return head 
```

（追記）上記のコード動かないので修正
```Python3
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        next_head = self.deleteDuplicates(head.next)
        if head.val == next_head.val:
            head.next = next_head.next
            return head
        head.next = next_head
        return head 
```

## Step3

```Python3
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        node = head
        while node:
            while node.next is not None and node.val == node.next.val:
                node.next = node.next.next
            node = node.next
        return head
```

