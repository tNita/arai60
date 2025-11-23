# 142. Linked List Cycle II


## 問題

Given the head of a linked list, return the node where the cycle begins. If there is no cycle, return null.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to (0-indexed). It is -1 if there is no cycle. Note that pos is not passed as a parameter.

Do not modify the linked list.

制約：

The number of the nodes in the list is in the range [0, 10^4].
-10^5 <= Node.val <= 10^5
pos is -1 or a valid index in the linked-list.

Follow up: Can you solve it using O(1) (i.e. constant) memory?

Nodeの定義
```Python3
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
```

## Step1
- 前の問題（141 Linked List Cycle）と同様でsetを使っていけそう
  - 先頭から順にNodeをみていきメモしておく（setにNodeを追加）
  - 同時に今までのメモもチェック
    - 同じノードがメモにあれば、そのNodeが循環の開始点であるためそのNodeを答えとしてreturn
  - メモに同じノードが現れずして末端（node.nextがNone）に到達した場合、連結リストに循環はないのでNoneをreturn

```Python3
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        visited_nodes = set()
        node = head
        while node:
            if node in visited_nodes:
                return node
            visited_nodes.add(node)
            node = node.next
        return None
```

- ただ、これだと空間計算量がO(n)
    - まあ、制約上問題ない気がするが、問題文をみる限り0(1)で解いた方がいいのだろう
```shell
python3 -c "import tracemalloc;tracemalloc.start();x={object() for _ in range(10000)};print(tracemalloc.get_traced_memory()[1]/1024/1024, 'MB')"
```
結果：0.7004241943359375 MB

- フロイドの循環検出法が使えるか？（前といたことがあるので使えるのは知っていたが。。。）
  - slowを1ノードずつ、fastを1ノード飛ばしでみていく
  - N回チェックした時にslowとfastが初めて出会うとするとslowはN、fastは2N進む
    - fastとSlowには差がNであり、fastは2週目であることを考えると循環の長さに等しい
    - 左端から合流点の距離がNであることを考えると（左端~循環開始点の距離)=(合流点~循環開始点の距離)
    - 左端・合流点からそれぞれ駒を一つづつ進めていけば循環開始点で合流する
```
左端    循環開始点      右端 循環開始点
|----------|------------|-|
<--  x  -->|<--    N    -->
               合流点 
|----------|-----|------|-|
<--     N     --> <-- x -->
           
```

- 左端・合流点から進める「駒」の命名迷う。。。

```Python3
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        fast = head
        slow = head

        joinPoint = None
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
            if fast is slow:
                joinPoint = fast
                break

        if not joinPoint:
            return None
        
        left = head
        right = joinPoint
        while True:
            if left is right:
                return left
            left = left.next
            right = right.next
        
        return None
```

## Step2

- https://discord.com/channels/1084280443945353267/1246383603122966570/1252209488815984710
  - この説明を見る前は証明的なことをして数式で理解しに行ったが、直感的にも理解できるようになった！
- https://github.com/mizuha0214/saito03601/pull/3/files
  - このPRのように、合流点見つけるロジックと循環の開始点見つけるロジックそれぞれをメソッドで分けてやっていることをメソッド名で表すとよりわかりやすいなと思った
  - from_xxxという命名は良さそう、循環開始点を見つけるロジックでそれぞれfrom_start, from_joinPointとすればよかったか
- 普段JavaやKotlin書くせいでついついキャメルケースで書いてしまう。。。
```Python3
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        fast = head
        slow = head

        join_point = None
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
            if fast is slow:
                join_point = fast
                break

        if not join_point:
            return None
        
        from_start = head
        from_join_point = join_point
        while True:
            if from_start is from_join_point:
                return from_start
            from_start = from_start.next
            from_join_point = from_join_point.next
        
        return None
```
- https://github.com/MasukagamiHinata/Arai60/pull/5/files#r2423335228
  - なるほど、while~elseという書き方があるのか。。。
  - > 「... 初めてのプログラマは、for/elseのelse部分は、『ループが完了しなかったらこれをしなさい』という意味だと思い込むものです。実際にはこれはまったく反対です。ループでbreak文が実行されると、実はelseブロックがスキップされます。」
  - 初見の文法見たら、妄想せずきちんとマニュアル見るのが大事そう
  - https://docs.python.org/3.13/tutorial/controlflow.html#else-clauses-on-loops
  - > In a for or while loop the break statement may be paired with an else clause. If the loop finishes without executing the break, the else clause executes.
  - 自分の好み的には使わないかな。。。
- https://github.com/Kazuryu0907/LeetCode_Arai60/pull/18/files#diff-b28236b06dc69b04a8be3de45d4b44cfe23ed4671c0fad2acf886cd1deb00fb9R24-R32
  - __hash__がオーバーライドされていないので、オブジェクトの同一性に基づいたハッシュになっていて、うまく動いただけ
  - https://docs.python.org/3/reference/datamodel.html#object.__hash__
  - > User-defined classes have __eq__() and __hash__() methods by default (inherited from the object class); with them, all objects compare unequal (except with themselves) and x.__hash__() returns an appropriate value such that x == y implies both that x is y and hash(x) == hash(y).

## Step3

```Python3
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        visited_nodes = set()
        node = head
        while node:
            if node in visited_nodes:
                return node
            visited_nodes.add(node)
            node = node.next
        return None
```
