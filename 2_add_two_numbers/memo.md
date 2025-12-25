# 

## 問題

You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.



## 制約
The number of nodes in each linked list is in the range [1, 100].
0 <= Node.val <= 9
It is guaranteed that the list represents a number that does not have leading zeros.


```Python3
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

```

## Step1
- 先頭から順にループで見ていき、足していく
    -  繰り上がりをどこかに持っておけば
    -  全加算器のようなものを作れば良さそう
```Python3
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        # 番兵を使わない場合、ループ中に次の桁のノードをダミー（値が0のノード）で追加していくことになる
        # そうするとループ終了時には必ずダミーのノードが残る
        # 末端から一つ前に戻ってそのダミーノードへの連結を切断する必要があり、大変。
        # 連結リストは進むのは簡単だが戻るのは大変なので
        dummy_head_sum = ListNode()
        added = dummy_head_sum
        carry = 0
        # ループの契約はl1, l2は今の桁、carryは前の桁からの繰り上がり、addedは前の桁
        while l1 or l2 or carry > 0:
            l1_digit = l1.val if l1 else 0
            l2_digit = l2.val if l2 else 0
            sum_digit = l1_digit + l2_digit + carry
            added.next = ListNode(sum_digit % 10)
            carry = sum_digit // 10
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
            added = added.next
        # l1、l2ともに先頭の桁（連結リストの末端）が0であることはないので、和の先頭の桁も必ず0以上になる
        return dummy_head_sum.next
```

- 計算量
    - 時間計算量: O(N)
    - 空間計算量: O(N)

## Step2

- 自分のコードの整形
    - 変数名の変更
    - 次のNodeを取得する、今のNodeの値を取得するのは関数に切り出した方が良さそう
```Python3
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        sum_dummy_head = ListNode()
        sum_node = sum_dummy_head
        carry = 0
        while l1 or l2 or carry > 0:
            l1_val = self._get_val_or_zero(l1)
            l2_val = self._get_val_or_zero(l2)
            sum_val = l1_val + l2_val + carry
            sum_node.next = ListNode(sum_val % 10)
            carry = sum_val // 10
            l1 = self._get_next(l1)
            l2 = self._get_next(l2)
            sum_node = sum_node.next
        # l1、l2ともに先頭の桁（連結リストの末端）が0であることはないので、和の先頭の桁も必ず0以上になる
        return sum_dummy_head.next

    def _get_val_or_zero(self, node: Optional[ListNode]) -> int:
        return node.val if node else 0
    
    def _get_next(self, node: Optional[ListNode]) -> Optional[ListNode]:
        return node.next if node else None
```

- https://discord.com/channels/1084280443945353267/1196472827457589338/1197166381146329208
    - 再帰で書く方法もあり
```Python3
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        return self.add_two_numbers(l1, l2, 0)

    def add_two_numbers(self, l1: Optional[ListNode], l2: Optional[ListNode], carry: int) -> Optional[ListNode]:
        if l1 is None and l2 is None and carry == 0:
            return None
        l1_val = self._get_val_or_zero(l1)
        l2_val = self._get_val_or_zero(l2)
        total = l1_val + l2_val + carry
        carry = total // 10
        remainder = total % 10
        node = ListNode(remainder)
        l1 = self._get_next(l1)
        l2 = self._get_next(l2)
        node.next = self.add_two_numbers(l1, l2, carry)
        return node

    def _get_val_or_zero(self, node: Optional[ListNode]) -> int:
        return node.val if node else 0
    
    def _get_next(self, node: Optional[ListNode]) -> Optional[ListNode]:
        return node.next if node else None
```
- https://discord.com/channels/1084280443945353267/1235829049511903273/1238087350995779674
    - ダミーを使った再帰
    - 帰りがけの処理が不要になるメリットがある
```Python3
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        # 中で組み立て
        self.add_two_numbers(l1, l2, 0, dummy)
        return dummy.next

    def add_two_numbers(self, l1: Optional[ListNode], l2: Optional[ListNode], carry: int, curr: ListNode) -> None:
        if l1 is None and l2 is None and carry == 0:
            return
        l1_val = self._get_val_or_zero(l1)
        l2_val = self._get_val_or_zero(l2)
        total = l1_val + l2_val + carry
        carry = total // 10
        remainder = total % 10
        curr.next = ListNode(remainder)
        l1 = self._get_next(l1)
        l2 = self._get_next(l2)
        self.add_two_numbers(l1, l2, carry, curr.next)

    def _get_val_or_zero(self, node: Optional[ListNode]) -> int:
        return node.val if node else 0
    
    def _get_next(self, node: Optional[ListNode]) -> Optional[ListNode]:
        return node.next if node else None

```
- stack-loopに書き直してみる
```Python3
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        ENTER = 0
        EXIT = 1
        # stackに行きかけ、帰りがけに必要なネタをまとめるのは歪な気がする
        stack = [(ENTER, l1, l2, 0, 0)]
        head = None

        while stack:
            state, n1, n2, carry, reminder = stack.pop()
            if state == ENTER:
                if n1 is None and n2 is None:
                    if carry > 0:
                        # 最上位の繰り上がりは帰りがけだけ
                        stack.append((EXIT, None, None, 0, carry))
                    continue

                n1_val = self._get_val_or_zero(n1)
                n2_val = self._get_val_or_zero(n2)
                total = n1_val + n2_val + carry
                new_carry = total // 10
                reminder = total % 10

                stack.append((EXIT, None, None, 0, reminder))
                stack.append((ENTER, self._get_next(n1), self._get_next(n2), new_carry, 0))
            else:
                head = ListNode(reminder, head)

        return head

    def _get_val_or_zero(self, node: Optional[ListNode]) -> int:
        return node.val if node else 0
    
    def _get_next(self, node: Optional[ListNode]) -> Optional[ListNode]:
        return node.next if node else None
```

- https://discord.com/channels/1084280443945353267/1247673286503039020/1249777338057752616
    - dummy_headを使わないパターン。Pythonで書き直す
    - > 末端から一つ前に戻ってそのダミーノードへの連結を切断する必要があり、大変。
    - 上記のように考えていたが、先頭（一の位）を特別扱いすれば、ダミーノードを連結する必要はなさそう

```Python3
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        sum_head = ListNode() # まだ和が計算される前ということもあり0としておく
        sum_node = sum_head
        carry = 0
        is_bottom = True
        # 契約：l1, l2は今の桁、sum_nodeは最初だけ今の桁、次から（十の位から）は前の桁
        #  is_bottom: 一番下の桁（一の位）であるか？
        while l1 or l2 or carry > 0:
            l1_val = self._get_val_or_zero(l1)
            l2_val = self._get_val_or_zero(l2)
            sum_val = l1_val + l2_val + carry
            carry = sum_val // 10
            remainder = sum_val % 10
            l1 = self._get_next(l1)
            l2 = self._get_next(l2)
            if is_bottom:
                sum_node.val = remainder
                is_bottom = False
                continue
            sum_node.next = ListNode(remainder)
            sum_node = sum_node.next
        return sum_head

    def _get_val_or_zero(self, node: Optional[ListNode]) -> int:
        return node.val if node else 0
    
    def _get_next(self, node: Optional[ListNode]) -> Optional[ListNode]:
        return node.next if node else None
```

- https://github.com/seal-azarashi/leetcode/pull/5#discussion_r1639556137
    - sum_head, sum_nodeを作る部分はis_bottomの条件分岐の中に移す
    - こうするとそもそもis_bottom自体不要そう、sum_headがNoneかどうかで先頭かどうか確認できる
    - こっちの方がフラグ不要でシンプルに書けそう
```Python3
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        sum_head = None
        sum_node = None
        carry = 0
        while l1 or l2 or carry > 0:
            l1_val = self._get_val_or_zero(l1)
            l2_val = self._get_val_or_zero(l2)
            sum_val = l1_val + l2_val + carry
            carry = sum_val // 10
            remainder = sum_val % 10
            l1 = self._get_next(l1)
            l2 = self._get_next(l2)
            if sum_head is None:
                sum_head = ListNode(remainder)
                sum_node = sum_head
                continue
            sum_node.next = ListNode(remainder)
            sum_node = sum_node.next
        return sum_head

    def _get_val_or_zero(self, node: Optional[ListNode]) -> int:
        return node.val if node else 0
    
    def _get_next(self, node: Optional[ListNode]) -> Optional[ListNode]:
        return node.next if node else None
```

- https://github.com/Yoshiki-Iwasa/Arai60/pull/4#discussion_r1643076346
    - carryをintにするかboolにするか
    - > 整数が入るが、結果として0,1しか入らないと理解します
    - > 素数を列挙する返す関数で素数型作らないですよね。
    - 取りうる値（仕様）を型で表現することで表現力やその仕様をコンパイラに保証させることができるが、その分「今の仕様」を型で縛るような形なので、拡張性が失われるというトレードオフがあるということなのかな
    - この問題の場合は3つ以上の足し算である場合はcarry>1
- https://github.com/yus-yus/leetcode/pull/5/files/91f344d110d2dc8ce7982065314a25afec963cc9#r1944795971
    - `%`や`//`をしているところはdivmodでシンプルに表現できる
    - よりシンプルにできそうと感じた
- https://discord.com/channels/1084280443945353267/1366423240624439378/1372611463872516096
    - Generatorを使った解法もあり
    - https://github.com/mamo3gr/arai60/pull/5/files#r2635725096
    - > 一般に Generator は遅いので、遊びくらいの気持ちでいいと思います。
    - https://www.datacamp.com/tutorial/python-generators#:~:text=POWERED%20BY-,Memory%20and%20Speed%20Benchmarks,-Because%20of%20how
    - 実行を一時停止して再開するオーバーヘッドがあるため？
    - データ量的に今回は使わなくても良さげ

```shell
# リスト
python3 -m timeit "sum([x**2 for x in range(1_000_000)])"
2 loops, best of 5: 112 msec per loop

# Generator
python3 -m timeit "sum(x**2 for x in range(10_000_000))" 
1 loop, best of 5: 1.14 sec per loop
```

- https://github.com/aki235/Arai60/pull/5
    - https://github.com/aki235/Arai60/pull/5/files#r2642695415
    - `while l1 or l2 or carry >0` は `while l1 is None or l2 is None or carry > 0`

- https://github.com/appseed246/arai60/pull/6/files#r2596444559
- https://discord.com/channels/1084280443945353267/1084283898617417748/1199292102161481778
- https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex
    - 負の割り算の丸め方は言語によって異なる
    - 危ないので言語仕様を確認しようと思う気持ちが大事（知っているかどうかよりも）
        - Python: https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex
        - > The result is always rounded towards minus infinity: 1//2 is 0, (-1)//2 is -1, 1//(-2) is -1, and (-1)//(-2) is 0.

## Step3

```Python3
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        node = dummy
        carry = 0
        while l1 is not None or l2 is not None or carry > 0:
            l1_val = self._get_val_or_zero(l1)
            l2_val = self._get_val_or_zero(l2)
            total = l1_val + l2_val + carry
            carry, reminder = divmod(total, 10)
            node.next = ListNode(reminder)
            node = node.next
            l1 = self._get_next(l1)
            l2 = self._get_next(l2)
        return dummy.next

    def _get_val_or_zero(self, node: Optional[ListNode]) -> int:
        return node.val if node is not None else 0

    def _get_next(self, node: Optional[ListNode]) -> Optional[ListNode]:
        return node.next if node is not None else None

```