class MyHeap:
    def __init__(self, data: list):
        self.heap = data
        self.heapify()

    def heapify(self):
        length = len(self.heap)
        # 葉はヒープの条件を満たしているので、最後の葉の親ノードから順にshift_upを行う
        for i in reversed(range(length // 2)):
            self._shift_up(i)

    def push(self, val: int):
        self.heap.append(val)
        self._shift_down(len(self.heap) - 1)

    def pop(self) -> int:
        self._swap(0, len(self.heap) - 1)
        top = self.heap.pop()
        self._shift_up(0)
        return top

    # 前提：indexは葉でありindexの要素だけがヒープの条件を満たしていない
    # 操作：その要素を正しい位置に移動させる。そうすることで結果的にindex以下の部分木がヒープになる
    def _shift_up(self, index: int):
        parent = index
        min_child_index = self._min_child_index(parent)
        while min_child_index != -1:
            if self.heap[parent] < self.heap[min_child_index]:
                break
            # ここでswapしても、親の要素がさらに小さくなるだけ
            self._swap(parent, min_child_index)
            parent = min_child_index
            min_child_index = self._min_child_index(parent)

    # 前提：indexの要素だけがヒープの条件を満たしていない、indexの親の部分木はヒープの条件を満たしている
    # 操作：その要素を正しい位置に移動させる。そうすることで結果的にindexの親の部分木がヒープになる
    def _shift_down(self, index: int):
        child = index
        parent_index = self._parent_index(child)
        while parent_index > -1:
            if self.heap[parent_index] < self.heap[child]:
                break
            self._swap(parent_index, child)
            child = parent_index
            parent_index = self._parent_index(child)
    

    def _parent_index(self, index: int) -> int:
        # pythonは負の無限大方向へ丸めるのでこの分岐は不要だが念の為
        if index == 0:
            return -1
        return (index - 1) // 2

    def _min_child_index(self, index: int) -> int:
        left = 2 * index + 1
        right = 2 * index + 2
        if right < len(self.heap):
            if self.heap[left] < self.heap[right]:
                return left
            else:
                return right
        if left < len(self.heap):
            return left
        return -1

    def _swap(self, i: int, j: int):
        tmp = self.heap[i]
        self.heap[i] = self.heap[j]
        self.heap[j] = tmp


data = [5, 4, 6, -3, 3, 10, 2, 0]

expected1 = [-3, 0, 2, 4, 3, 10, 6, 5]
expected2 = [-4, -3, 2, 0, 3, 10, 6, 5, 4]
expected3 = [-3, 0, 2, 4, 3, 10, 6, 5]

new_heap = MyHeap(data)

print("heapify:", new_heap.heap == expected1)

new_heap.push(-4)
print("after push:", new_heap.heap == expected2)

new_heap.pop()
print("after pop:", new_heap.heap == expected3)