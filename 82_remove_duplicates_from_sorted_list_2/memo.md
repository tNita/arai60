# 82. Remove Duplicates from Sorted List II 

## 問題

Given the head of a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list. Return the linked list sorted as well.

## 制約
The number of nodes in the list is in the range [0, 300].
-100 <= Node.val <= 100
The list is guaranteed to be sorted in ascending order.

## Step1

- `83. Remove Duplicates from Sorted Value` の問題と同様にconcat-filter-groupで行けるかなと思ったが、うまく書く方法が思いつかなかった（混乱してきたので、一旦concat-filter-groupからは離れて考える）
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
                left.next = right # ここがまずい。元の連結リストが壊れる
                left = right
                prev_right_val = right.val
                right = right.next
        left.next = None
        return dummy_head.next

    def is_duplicate(self, prev_node_val: Optional[int], node: ListNode) -> bool:
        return (prev_node_val is not None and prev_node_val == node.val) or (node.next is not None and node.val == node.next.val)
```

コメント集や他の人のコードを見ていく
- https://github.com/goto-untrapped/Arai60/pull/43#discussion_r1695372547
    - 命名、nextとか、prevとか割と実装よりの命名を自分もしがち
    - より意味がわかる命名をするのがよさそう（checking、saved）
    - コードを書くときは自分の中でも理解をきちんと深め、本来何をしたいものなのかをはっきりさせておくことが必要
- https://discord.com/channels/1084280443945353267/1195700948786491403/1197102971977211966
- https://discord.com/channels/1084280443945353267/1196472827457589338/1196473202193481728
    - concat . filter . group で行けたのか。。。
        - group-filter-concatを理解したつもりになってたが、ちゃんと理解していなかったんだな。
        - 「重複している要素の直前」=「最後の一意なノード」を素直に変数で定義しておき、重複部分を特定して（group）、重複部分をスキップして最後の一意のノードを重複部分の次のノードに繋ぐ（filter-concat）
        - 判断（group-filter）と連結（concat）というふうに分けることでわかりやすくはなりそう？（理解が甘くてうまく言語化できない。。。）
        - > 「重複を発見したら帰るな」です。
        - 重複時は帰らない（group化）することで、前の要素との比較が不要になり考えることが減ってシンプルになるので好み
    - 列車のの
        - ループを描くときは他の人に引き継ぐために何が必要か明確に定義しておく
- https://github.com/nittoco/leetcode/pull/9#discussion_r1634077440
    - イテレータを作ると、pythonのgroupbyを使える
- https://github.com/seal-azarashi/leetcode/pull/4#discussion_r1633577704
    -   whileには本当に注目しているものを入れる
- https://discord.com/channels/1084280443945353267/1227073733844406343/1228673329284513843
    - 繋いでおいて切断する、切断しておいて繋ぐの2パターン
        - 個人的には初期化の時、ループ中と毎回切断の処理を書くのがめんどくさいので繋いでおいて切断するが好み

（繋いでおいて切断）

```Python3
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy_head = ListNode()
        dummy_head.next = head # 重複要素かわからない要素を繋いでおく
        tail = dummy_head
        node = head
        # 繋いでおいて切断
        # 引き継ぎの契約
        #  同じ値にグループ化
        #　nodeはグループの先頭
        #  tailは重複しない要素の最後、 重複かどうかわからない要素が後ろに繋がっている
        while node:
            if node.next is None or node.val != node.next.val:
                # nodeは重複しないことが確定
                tail.next = node # ここで重複しない要素を繋ぐ
                tail = tail.next # 重複要素かどうか不明な要素node.nextがtailに繋がっている
                node = node.next
                continue
            # nodeは重複確定
            while node.next and node.val == node.next.val:
                node = node.next
            node = node.next
        tail.next = None # 重複要素が繋がっている可能性があるので切断
        return dummy_head.next
```

（切断しておいて繋ぐ）
```Python3
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy_head = ListNode()
        tail = dummy_head
        node = head
        # 切断しておいて繋ぐ
        # 引き継ぎの契約
        #  同じ値にグループ化
        #  nodeはグループの先頭
        #  tailは重複しない要素の最後、後ろには何も繋がっていない
        while node:
            if node.next is None or node.val != node.next.val:
                tail.next = node
                tail = tail.next
                node = node.next
                tail.next = None
                continue
            while node.next and node.val == node.next.val:
                node = node.next
            node = node.next
        return dummy_head.next
```


- https://hackage.haskell.org/package/base-4.19.0.0/docs/Data-List.html#v:group
    - Pythonのgroup→filter→concatの順に見えるので、なんでconcat. filter. groupなのかが疑問だった
    - おそらくHaskellの書き方をもとにしてそうとわかり納得
（動くか不明、GPTに書かせただけ）
```Haskell
import Data.List (group)

-- 例: data ListNode = ListNode Int (Maybe ListNode)
-- deleteDuplicates :: Maybe ListNode -> Maybe ListNode

deleteDuplicates :: Maybe ListNode -> Maybe ListNode
deleteDuplicates =
  fromList
  . concat
  . filter ((== 1) . length)
  . group
  . toList

toList :: Maybe ListNode -> [Int]
toList Nothing = []
toList (Just (ListNode x next)) = x : toList next

fromList :: [Int] -> Maybe ListNode
fromList [] = Nothing
fromList (x:xs) = Just (ListNode x (fromList xs))
```

- https://discord.com/channels/1084280443945353267/1334041281902547036/1335906471111688212
    - dummy_headを使わずにもとける
    - step1で先頭が重複していた場合を分岐するのがめんどくさく諦めてしまったが、もう一度dummy headを使わない方法をトライして見る
```Python3
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        node = head        
        # 重複しない連結リストの先頭を決めるため、重複しない要素までnodeを進める
        while node and node.next and node.val == node.next.val: # nodeはグループの先頭
            while node.next and node.val == node.next.val: 
                node = node.next
            node = node.next

        # 末尾まで来てしまった場合
        if node is None:
            return None

        unique_head = ListNode(node.val)
        unique_tail = unique_head
        node = node.next
        while node:
            if node.next is None or node.val != node.next.val:
                unique_tail.next = node
                unique_tail = unique_tail.next
                node = node.next
                continue
            while node.next and node.val == node.next.val:
                node = node.next
            node = node.next
        unique_tail.next = None
        return unique_head
```
- https://github.com/komdoroid/arai60/pull/11/files#diff-78f7b056e03d7cd1c9c430caf9558d329cf2e40a6d7b5ab47313ff817fe44cf9R105
    - 再帰でもかける

- 色々みたあとで：元のリストを変更しない方がわかりやすそうと感じた
    - この場合、「切断」自体不要で、headも壊れない
    - nodeの数も高々300であるため、メモリ使用量も問題ない

## Step 3 

```Python3
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy
        node = head
        while node:
            if node.next is None or node.val != node.next.val:
                tail.next = ListNode(node.val)
                tail = tail.next
                node = node.next
                continue
            while node.next and node.val == node.next.val:
                node = node.next
            node = node.next
        return dummy.next
```