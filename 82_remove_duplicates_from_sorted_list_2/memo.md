# 82. Remove Duplicates from Sorted List II 

## 問題

Given the head of a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list. Return the linked list sorted as well.

## 制約
The number of nodes in the list is in the range [0, 300].
-100 <= Node.val <= 100
The list is guaranteed to be sorted in ascending order.

## Step1

- 重複を全部削除する→重複している要素の直前の要素を基準とする必要がありそう
- 重複している直前の要素を特定してから、重複している要素の直後の要素を特定できればそれらを繋げることで目的を達成できそう
- その重複している要素の直前の要素、直後の要素はどう特定するのか？
  - 二つのポインタ直前の要素left、直後の要素rightを持ってそれを動かしていけば良さそう→rightを主役にループを回す
    - 初回はleftを先頭、rightを先頭の次の要素として進める
    - rightが重複要素だったらrightを次に進める、leftはそのまま
    - rightが重複要素でなかったらleftをrightに連結させた上で、leftはrightまで移動、rightは次の要素へ移動
    - rightがNoneになったらループを終了し、leftは末端になるようにしておく
  - rightが重複要素であることの判定
    - 直前の要素の値 ==　今の要素の値 or （直後の要素がNoneか今の要素の値 == 直後の要素の値）
  - 解いている中で境界条件が甘く、先頭をきちんと考慮できていないことに気づく
（アクセプトされなかったコード）
```Python3
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None:
            return head
        left = head
        prev_right_val = head.val
        right = head.next
        while right:
            isDuplicate = self.isDuplicate(prev_right_val, right)
            if isDuplicate:
                prev_right_val = right.val
                right = right.next
            else:
                left.next = right
                left = right
                prev_right_val = right.val
                right = right.next
        left.next = None
        return head    
    

    def isDuplicate(self, prev_node_val: int, node: ListNode) -> bool:
        if node.next:    
            return prev_node_val == node.val or node.val == node.next.val
        else:
            return prev_node_val == node.val
```

- 先頭を特別に扱わなくていいようにheadの先頭にdummyのヘッドを作って対応
    - ループのはじめはleftをdummyのヘッド、rightをヘッド（dummyの次の要素）
```
class Solution:
    # ダミーヘッドの値は -100 <= Node.val <= 100 の外の適当な値
    #  仕様が変更になるかもしれないので大きめに取っておく
    DUMMY_HEAD_VAL = 10000

    # WARN: headを破壊的に変更します
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None:
            return head
        dummyHead = ListNode(self.DUMMY_HEAD_VAL, head)
        left = dummyHead
        prev_right_val = left.val
        right = dummyHead.next
        while right:
            isDuplicate = self.isDuplicate(prev_right_val, right)
            if isDuplicate:
                prev_right_val = right.val
                right = right.next
            else:
                left.next = right
                left = right
                prev_right_val = right.val
                right = right.next
        left.next = None
        return dummyHead.next

    def isDuplicate(self, prev_node_val: int, node: ListNode) -> bool:
        if node.next:    
            return prev_node_val == node.val or node.val == node.next.val
        else:
            return prev_node_val == node.val
```

- 一旦アクセプトされたのでstep1は終了


## Step2

まずは自分のコードを整える

- dummyheadを用意しているのでheadがNoneかどうかはチェック不要
- Javaの癖でどうしても意識していないとキャメルケースで書いてしまう（Pythonの「常識」に意識的に合わせていく）
- DUMMY_HEAD_VALに依存するとどうしても変更に弱くなる...
    - Noneでやってみる
- is_duplicateをprev == curr or curr == nextという形でリファクタ
```
class Solution:
    # WARN: headを破壊的に変更します
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy_head = ListNode(0, head)
        left = dummy_head
        prev_right_val: Optional[int] = None
        right = dummy_head.next
        while right:
            if self.is_duplicate(prev_right_val, right):
                prev_right_val = right.val
                right = right.next
            else:
                left.next = right
                left = right
                prev_right_val = right.val
                right = right.next
        left.next = None
        return dummy_head.next

    def is_duplicate(self, prev_node_val: Optional[int], node: ListNode) -> bool:
        return (prev_node_val is not None and prev_node_val == node.val) or (node.next is not None and node.val == node.next.val)
```

他の人のコードを見る

- 

