# 141. Linked List Cycle（レビュー後）

- 命名をキチンと意識してStep1をやり直す

```Python3
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        visited_nodes = []
        node = head
        while node:
            for visited_node in visited_nodes:
                if node is visited_node:
                    return True
            visited_nodes.append(node)
            node = node.next
        return False
```