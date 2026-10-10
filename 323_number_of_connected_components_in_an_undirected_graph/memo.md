# 323. Number of Connected Components in an Undirected Graph

## 問題

You have an undirected graph of n nodes labeled from 0 to n - 1. You are given an integer n and an array edges where edges[i] = [aᵢ, bᵢ] indicates that there is an edge between aᵢ and bᵢ in the graph.

Return the number of connected components in the graph.

> - 1 <= n <= 2000
> - 1 <= edges.length <= 5000
> - edges[i].length == 2
> - 0 <= aᵢ < n
> - 0 <= bᵢ < n
> - aᵢ != bᵢ
> - There are no repeated edges.

## Step1

- 各edgeの表記をai < biとした上で考える
- 案1
  - コンポーネントの代表をコンポーネントの中の最小ノードとする
  - 代表ノード: edgeのbiには現れない
  - そうでないノード: edgeのbiに現れる（別のノードを代表ノードとするコンポーネントに所属）
  - つまり、edgeのbiに現れないノード数をカウントすれば良い
- 案2
  - 代表ノードを最小ノードとする
  - ノード数分配列を用意し、1が代表ノード、0が代表ノードでないとする
  - エッジを順に見ていき、エッジのbi番目の要素を0に更新
  - エッジを一通り見終わった後、配列の要素を全て足し合わす
- edgeはいじらない方法は思いつかなかった

案1で実装してみる

```Python
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        ordered_edges = []
        for edge in edges:
            # 制約上あり得ないが念の為
            if edge[0] == edge[1]:
                continue
            ordered_edges.append(sorted(edge, ))

        unrepresentative_nodes = set()
        for edge in ordered_edges:
            unrepresentative_nodes.add(edge[1])
        return n - len(unrepresentative_nodes)
```

Acceptしなかった。
ちょっと単純化し過ぎてしまった。。。
1-2-0 （edgeは1-2、0-2）のとき、コンポーネントを2つと判断してしまう。

手作業でどうやるかを考える。
- バラバラの島をedgeに応じて合体させていくイメージ
一旦これを愚直に実装してみる。時間計算量がO(N^2*M)になってしまったが（Nはノード数、Mはエッジ数）、ノード数、エッジ数は数千個程度なので許容はされそう→いや、そうでもない（Pythonの処理能力を 10^7 steps/secとすると、2000^2*5000/10^7 = 5.42sec）
- 他に案が思いつかず一旦終了

```Python
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        components = [[i] for i in range(n)]
        def find_component_index_of_node(node: int):
            for i, component in enumerate(components):
                if node in component:
                    return i
            # 全てのノードを含めているはずなので見つからないはずはない
            raise RuntimeError("unreachable")
        
        for edge in edges:
            first_node_component_index = find_component_index_of_node(edge[0])
            second_node_component_index = find_component_index_of_node(edge[1])
            # 別コンポーネントであれば、一方が他方を吸収し、吸収された方を削除
            if first_node_component_index != second_node_component_index:
                components[first_node_component_index].extend(components[second_node_component_index])
                components.pop(second_node_component_index)
        return len(components)
```

## Step2

### 自分のコードに対して
- 最初の解き方に対して
  - biに現れているのは代表ノードでないノードの一部であり全てでないため、ロジックが不適切
  - エッジが代表ノード-そうでないノードであればロジックは成り立つ、そうでなければ成り立たない

### コメント集や他の人のコード

- https://github.com/kazuki-official/leetcode/pull/20
  - 計算量の記法、ノード数N、エッジ数Eとするのが一般的
  - DFS、BFSで、全てのノードを見る。あるノードに対してつながっているノードを辿り切ったら次のノードに対し同様のことを行う
  - Union Find（by rank）
- https://github.com/mamo3gr/arai60/pull/56
  - > 28 bytes/int * 2000 = 56KB のオーダーを予想する。
  - 28という数字がどこからきたのかがわからなかった
  - 親を管理する配列を用意。また処理中で、親は必ず直接繋がる様に担保している
    - 最初のエッジを見た時は親-子直接繋がる状態になる
    - 親（A）-子（B、C、...）直接つながっている状態で
      - ある要素XをB（やC...）を親とする様に繋ごうとしても、Xは直接Aに繋がれる
      - AをXを親として繋げようとしても、B、C、...はXを親とする様になる
      - XをAを親として繋げる場合はそのままXの親がAとなる
    - Union Findをrankでなくsizeで
- https://github.com/naoto-iwase/leetcode/pull/28
  - Union Findについて
  - 親を繋ぎかえる処理はPath Splitting, Path Halvingもある
    - 親を親の親にする
    - ループごとに自身は以前の親に行くのか、更新後の親（以前の祖父）に行くのかが違い。Path Splittingは前者、Path Halvingは後者か。

Path Splitting
```Python3
def find(x):
  while parent[x] != x:
    parent[x], x = parent[parent[x]], parent[x]
  return x
```

Path Halving
```Python3
def find(x):
  while parent[x] != x:
    parent[x] = parent[parent[x]]
    x = parent[x]
  return x
```

DFS

```Python3
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        adjacent = defaultdict(list)
        for edge in edges:
            node1, node2 = edge
            adjacent[node1].append(node2)
            adjacent[node2].append(node1)
        
        seen = set()

        def visit_connected_node(start_node):
            frontier = [start_node]
            while frontier:
                node = frontier.pop()
                seen.add(node)
                for next_node in adjacent[node]:
                    if next_node in seen:
                        continue
                    frontier.append(next_node)

        connected_component_number = 0
        for i in range(n):
            if i in seen:
                continue
            connected_component_number += 1
            visit_connected_node(i)
        return connected_component_number
```
BFS
```Python3
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        adjacent = defaultdict(list)
        for edge in edges:
            node1, node2 = edge
            adjacent[node1].append(node2)
            adjacent[node2].append(node1)
        
        seen = set()

        def visit_connected_node(start_node):
            frontier = [start_node]
            while frontier:
                next_frontier = []
                for node in frontier:
                    seen.add(node)
                    for next_node in adjacent[node]:
                        if next_node in seen:
                            continue
                        next_frontier.append(next_node)
                frontier = next_frontier

        connected_component_number = 0
        for i in range(n):
            if i in seen:
                continue
            connected_component_number += 1
            visit_connected_node(i)
        return connected_component_number
```

## Step3
Union Findで実装

- V, Eはそれぞれ頂点、エッジとして。αは逆アッカーマン関数でほぼO(1)
- rootの取得にはO(α(V))
- 計算量
  - Time: UnionNodeのコンストラクタでO(V)、uniteがE回で、uniteの中はO(α(V))→O(V + E * α(V))
  - Space: O(V)

```Python3
class UnionNode:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.rank = [0] * n
        self.group_number = n
    
    def _root(self, x):
        if x == self.parent[x]:
            return x
        self.parent[x] = self._root(self.parent[x])
        return self.parent[x]
    
    def unite(self, x, y):
        x_root = self._root(x)
        y_root = self._root(y)
        if x_root == y_root:
            return
        if self.rank[x_root] < self.rank[y_root]:
            x_root, y_root = y_root, x_root
        self.rank[x_root] += 1
        self.parent[y_root] = x_root
        self.group_number -= 1

class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        union_node = UnionNode(n)
        for edge in edges:
            union_node.unite(edge[0], edge[1])
        return union_node.group_number
```

