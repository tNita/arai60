# 695. Max Area of Island
You are given an m x n binary matrix grid. An island is a group of 1's (representing land) connected 4-directionally (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water.

The area of an island is the number of cells with a value 1 in the island.

Return the maximum area of an island in grid. If there is no island, return 0.

m == grid.length
n == grid[i].length
1 <= m, n <= 50
grid[i][j] is either 0 or 1.

## Step1

- 前の問題（200. Numbers of Islands）と同様に行けそう
  - visit_islandする時に、重複なく訪問しているのでついでに広さも計測していけば良い
    - 深さ優先、幅優先二つの解法があると思うが、特に目立った優劣はなさそう
    - 再帰の深さは最大50 * 50 = 2,500 > [recursion limit(1000)](https://docs.python.org/3/library/sys.html#sys.getrecursionlimit)なので再帰はやめておく
- 他の案は？
  - Union Findを使ってもいけそう
    - union by sizeのために各グループのサイズをrootに持たせているのでこれを利用すれば

- 深さ優先でvisit_islandするついでに広さも計測
```Python
class Solution:
    WATER = 0
    LAND = 1
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        height = len(grid)
        width = len(grid[0])
        visited = [[False] * width for _ in range(height)]

        def is_inside_grid(i: int, j: int) -> bool:
            return 0 <= i < height and 0 <= j < width

        def visit_and_measure_island(start: tuple[int, int]) -> int:
            stack = deque()
            stack.append(start)
            island_size = 0
            while stack:
                i, j = stack.pop()
                if not is_inside_grid(i, j) or grid[i][j] == self.WATER or visited[i][j]:
                    continue
                visited[i][j] = True
                island_size += 1
                stack.append((i - 1, j))
                stack.append((i + 1, j))
                stack.append((i, j - 1))
                stack.append((i, j + 1))
            return island_size

        max_island_size = 0
        for i in range(height):
            for j in range(width):
                if not visited[i][j] and grid[i][j] == self.LAND:
                    island_size = visit_and_measure_island((i, j))
                    max_island_size = max(max_island_size, island_size)
        return max_island_size

```

- Union Find

```Python3
class IsLandUnionFind:
    def __init__(self, lands: List[tuple[int, int]]) -> None:
        self.parents = {}
        # rootにサイズを持たせる。
        self.sizes_by_root = {}
        for land in lands:
            self.parents[land] = land
            self.sizes_by_root[land] = 1
    
    def get_root(self, land: tuple[int, int]) -> tuple[int, int]:
        if self.parents[land] == land:
            return land
        self.parents[land] = self.get_root(self.parents[land])
        return self.parents[land]

    def unite(self, land1: tuple[int, int], land2: tuple[int, int]) -> None:
        land1_root = self.get_root(land1)
        land2_root = self.get_root(land2)
        if land1_root == land2_root:
            return

        big_root = land1_root
        small_root = land2_root
        if self.sizes_by_root[big_root] < self.sizes_by_root[small_root]:
            big_root, small_root = small_root, big_root
        
        self.parents[small_root] = big_root
        self.sizes_by_root[big_root] += self.sizes_by_root[small_root]
        del self.sizes_by_root[small_root]

    def get_largest_union_size(self) -> int:
        union_size = 0
        for size in self.sizes_by_root.values():
            union_size = max(union_size, size)
        return union_size

class Solution:
    WATER = 0
    LAND = 1
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        height = len(grid)
        width = len(grid[0])
        lands = []
        for i in range(height):
            for j in range(width):
                if grid[i][j] == self.LAND:
                    lands.append((i, j))

        land_union_find = IsLandUnionFind(lands)
        for land in lands:
            i, j = land
            if j < width - 1 and grid[i][j + 1] == self.LAND:
                land_union_find.unite(land, (i, j + 1))
            if i < height - 1 and grid[i + 1][j] == self.LAND:
                land_union_find.unite(land, (i + 1, j))
        return land_union_find.get_largest_union_size()
```


## Step2

### 他の人のコード
- https://github.com/hayashi-ay/leetcode/pull/34
  - Union Findで一通りuniteしたあとにルートごとに広さを集計していくやり方
- https://github.com/fuga-98/arai60/pull/19
  - Union Findで、union by rank
  - rankが等しいものを結合する時にrankを+1する、等しくない場合はrankはそのまま
- https://github.com/naoto-iwase/leetcode/pull/18
  - コマンド・クエリ分離
- https://github.com/Manato110/LeetCode-arai60/pull/18/changes
  - 上下左右の点の面積をそれぞれ再帰的に計算して合算する方法で面積求めている
- https://github.com/rimokem/arai60/pull/18
  - stackに一気に詰める方法もあり。
```mermaid
stack.extend(
    [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
)
```

### コメント集

- https://discord.com/channels/1084280443945353267/1307605446538039337/1334350726683693086
  - > 同じ意味のものが繰り返しているときには [] のほうが多い気がします。Tuple も immutable という点ではいいかもしれません。
  - ちょっと好みではないが一貫性があればまあ良いって感じの類か


## Step3

```Python3
class Solution:
    WATER = 0
    LAND = 1
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        height = len(grid)
        width = len(grid[0])
        visited = [[False] * width for _ in range(height)]

        def is_inside_island(i: int, j: int):
            return 0 <= i < height and 0 <= j < width

        def explorer_and_get_size_island(start: tuple[int]) -> int:
            stack = deque()
            stack.append(start)
            area_size = 0
            while stack:
                i, j = stack.pop()
                if not is_inside_island(i, j) or grid[i][j] == self.WATER or visited[i][j]:
                    continue
                visited[i][j] = True
                area_size += 1
                stack.append((i - 1, j))
                stack.append((i + 1, j))
                stack.append((i, j - 1))
                stack.append((i, j + 1))
            return area_size
        
        max_are_size = 0
        for i in range(height):
            for j in range(width):
                if not visited[i][j] and grid[i][j] == self.LAND:
                    area_size = explorer_and_get_size_island((i, j))
                    max_are_size = max(max_are_size, area_size)
        return max_are_size
```
