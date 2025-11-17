## 141. Linked List Cycle

問題：

Given head, the head of a linked list, determine if the linked list has a cycle in it.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to. Note that pos is not passed as a parameter.

Return true if there is a cycle in the linked list. Otherwise, return false.

制約:

The number of the nodes in the list is in the range [0, 10^4].
-10^5 <= Node.val <= 10^5
pos is -1 or a valid index in the linked-list.

Nodeの定義：

```Python3
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
```
 
https://leetcode.com/problems/linked-list-cycle/


## Step1

最初に思いついたこと

- 昔同じ問題やったことがあり、ウサギとカメのアルゴリズムはなんとくなく知っていたがきちんと一から考えてみる
- headから順番にチェックしていき、通ったnodeを到達ずみとしてメモ
- チェックしていくうちにメモしたnodeと一致するnodeがあればサイクルあり、一致するものなく末端に到達すればサイクルなし
- nodeをそのまま到達ずみメモの配列に追加する
- nodeの実態はオブジェクトのポインタであり、リストのnodeの数の上限からもメモリ使用量も問題なさそう
  - 実測値からも問題なし
```
% python3 -c "import tracemalloc;tracemalloc.start();x=[object() for _ in range(10000)];print(tracemalloc.get_traced_memory()[1]/1024/1024,'MB')" 

0.23400115966796875 MB
```

```Python3
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        visited_node = []
        node = head
        while node:
            for m in visited_node:
                if m is node:
                    return True
            visited_node.append(node)
            node = node.next
        return False
```

- 毎回到達ずみのnodeチェックをしているが無駄な気もする
- 一人でチェックする場合はどうしても記憶（=メモ）を使わないといけない
- 二人以上でチェックする場合はどうか？
  - サイクルがある時は無限ループするので、二人が異なるスピードでnodeをチェックしていけばいずれは追い越しが発生する
  - 追い越しを検知さえすればサイクルを検知できる
  - 早い人(fast)=一つ飛ばし、遅い人(slow)=一つづつでチェックしていけば、追い越し時は以下の通りで必ず同じnodeにいる時が存在する
    1. fastがslowの1つまえのnode
    2. fastとslowが同じnode
    3. fastがslowの一つ先のnode
  - サイクルなしのチェックはfastが末端に到達したかどうかでチェックすればいい
    - fastは一つ飛ばしなので末端 or 末端一つ前に到達した時点でサイクルなしと判断できる

```Python3
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        fast = head
        slow = head
        # 必ずfastの方がslowより先に末端に到達するためslowのチェックは不要
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
            if fast is slow:
                return True
        return False
```

## Step2


他の方の解き方や過去のコメントなどを見てみる
- https://discord.com/channels/1084280443945353267/1195700948786491403/1195868438858571977
  - リストじゃなくてSetを使えば、すでに到達した点のチェックはO(1)でできた
    - Setは内部的にはハッシュテーブル（https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset）
  - リストの3倍メモリを使用しているがメモリ使用量自体は問題なさそう
    - Setはメモリを過剰に割り当てるらしい（https://medium.com/data-science/memory-efficiency-of-common-python-data-structures-88f0f720421）
```
% python3 -c "import tracemalloc;tracemalloc.start();x={object() for _ in range(10000)};print(tracemalloc.get_traced_memory()[1]/1024/1024, 'MB')"
0.7004241943359375 MB
```
  - 今回、メモリ使用量の方を気にしすぎていた
    - > 毎回到達ずみのnodeチェックをしているが無駄な気もする
    - ここからチェックをO(n)→O(1)に下げる方法はないかと考えられたはず。。。
- https://github.com/tk-hirom/Arai60/pull/1#discussion_r1641231416
  - > Tortoise and Hare を知っていた場合、知っていたところでどうでもいいです。これは科学手品みたいに子供の興味を引くときに使うものです。 
    > Tortoise and Hare を知らなかった場合、特に何もありません。 
    > 上の set を使ったコードが書けた場合、普通はできます。 
    > 上の set を使ったコードが書けなかった場合、一緒に働くことが困難です
    - なるほど、独学でLeetCodeかじっていた時はこういうエレガントなアルゴリズムをたくさん知っていないといけないのかと思っていたが、そういうわけではないのか
    - それよりも、基本的なアルゴリズムをきちんと使いこなせるかが大事なのかなと思った
    - (キャンベルの法則)[https://discord.com/channels/1084280443945353267/1195700948786491403/1196021630103724134]
- https://github.com/TakayaShirai/leetcode_practice/pull/1#discussion_r2514344453
  - 変数名はシンプルにvisitedにするのがいいのか？
  - 多分上記の例はSwiftでオブジェクトの識別子をvisitedに追加しているから
    - ```Swift
      let nodeId = ObjectIdentifier(node)
      ...
      visitedNodes.insert(nodeId)
      ```
  - Pythonでもid関数を使った場合はvisitedを使った方がいい
    - https://docs.python.org/3/library/functions.html#id
    - ただ、マニュアルに↓と書いてあるのでvisited_nodeにnode自体を追加し、isを使って同一性チェックをするのが素直
    - https://docs.python.org/3/reference/datamodel.html#objects-values-and-types
    - >  The is operator compares the identity of two objects; the id() function returns an integer representing its identity.
- https://github.com/MasukagamiHinata/Arai60/pull/4/files#diff-357653c1cb415a59b70c0ee0b3aba61410e2b967c6cb0312e034d6ba5c90169fR33
  - 時間の見積もり
  - なるほど、C言語で見積もった後に大体100倍するという方法があるのか（Pythonだと1行百機械語の場合もある）
    - 一旦のC言語でどのくらいの命令があるかをざっくり見積もり（定数倍の見積もり)、C言語でどのくらい実行時間がかかるかを算出
    - ネイティブコードを呼び出す場合はずれそうではある。
    - 参考になりそうなコメント
      - https://discord.com/channels/1084280443945353267/1218823752243089408/1244470338562293882
      - https://discord.com/channels/1084280443945353267/1200089668901937312/1235490680592273410

## Step3

```Python3
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        visited_node = set()
        node = head
        while node:
            if node in visited_node:
                return True
            visited_node.add(node)
            node = node.next
        return False
```


