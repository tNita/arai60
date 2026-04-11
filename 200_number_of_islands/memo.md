# 200. Number of Islands

Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.


Constraints:

m == grid.length
n == grid[i].length
1 <= m, n <= 300
grid[i][j] is '0' or '1'.

## Step1

- 左上から順番に見ていく
- 訪問済みかどうかを管理するm x nの配列を用意する
- 訪問済みであればスキップ
- 未訪問であれば、
  - (i,j)がlandであったら、islandの個数をインクリメントして、四方をlandが続く限り訪問済みにしていく
  - (i,j)がwaterであったら訪問済みにしてスキップ
- 深さ優先

```Python3
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        island_count = 0
        rows = len(grid)
        columns = len(grid[0])
        visited = [ [False] * columns for _ in range(rows) ]

        def visit_island(current_i: int, current_j: int) -> None:
            if visited[current_i][current_j]:
                return
            visited[current_i][current_j] = True
            if grid[current_i][current_j] == "0":
                return
            next_visit_points = []
            if current_i > 0:
                next_visit_points.append((current_i - 1, current_j))
            if current_i < rows - 1:
                next_visit_points.append((current_i + 1, current_j))
            if current_j > 0:
                next_visit_points.append((current_i, current_j - 1))
            if current_j < columns - 1:
                next_visit_points.append((current_i, current_j + 1))
            for next_i, next_j in next_visit_points:
                visit_island(next_i, next_j)
        i = 0
        j = 0
        while i < rows:
            if not visited[i][j] and grid[i][j] == "1":
                island_count += 1
                visit_island(i, j)
            if j == columns - 1:
                i += 1
                j = 0
                continue
            j += 1
        return island_count
```


- 再帰をループに書き換え
  - 幅優先
```Python3
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        island_count = 0
        rows = len(grid)
        columns = len(grid[0])
        visited = [ [False] * columns for _ in range(rows) ]

        def visit_island(current_i: int, current_j: int) -> None:
            visiting_points = deque([(current_i, current_j)])
            while visiting_points:
                current_i, current_j = visiting_points.popleft()
                if visited[current_i][current_j]:
                    continue
                visited[current_i][current_j] = True
                if grid[current_i][current_j] == "0":
                    continue
                if current_i > 0:
                    visiting_points.append((current_i - 1, current_j))
                if current_i < rows - 1:
                    visiting_points.append((current_i + 1, current_j))
                if current_j > 0:
                    visiting_points.append((current_i, current_j - 1))
                if current_j < columns - 1:
                    visiting_points.append((current_i, current_j + 1))

        i = 0
        j = 0
        while i < rows:
            if not visited[i][j] and grid[i][j] == "1":
                island_count += 1
                visit_island(i, j)
            if j == columns - 1:
                i += 1
                j = 0
                continue
            j += 1
        return island_count

```

- 深さ優先
```Python3
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        island_count = 0
        rows = len(grid)
        columns = len(grid[0])
        visited = [ [False] * columns for _ in range(rows) ]

        def visit_island(current_i: int, current_j: int) -> None:
            visiting_points = deque([(current_i, current_j)])
            while visiting_points:
                current_i, current_j = visiting_points.pop()
                if visited[current_i][current_j]:
                    continue
                visited[current_i][current_j] = True
                if grid[current_i][current_j] == "0":
                    continue
                if current_i > 0:
                    visiting_points.append((current_i - 1, current_j))
                if current_i < rows - 1:
                    visiting_points.append((current_i + 1, current_j))
                if current_j > 0:
                    visiting_points.append((current_i, current_j - 1))
                if current_j < columns - 1:
                    visiting_points.append((current_i, current_j + 1))

        i = 0
        j = 0
        while i < rows:
            if not visited[i][j] and grid[i][j] == "1":
                island_count += 1
                visit_island(i, j)
            if j == columns - 1:
                i += 1
                j = 0
                continue
            j += 1
        return island_count
```
- 時間計算量
  - visit_islandの計算量を出すのが難しい
  - visit_islandの計算量を Kとした場合は
  - O(rows * columns * K)
- 空間計算量
  - O(rows * columns)

### Step1の計算量について怪しいのでAIを元に理解を深める
- 結論、空間計算量は正しい、時間計算量はKは不要
- DFS, BFSともに時間計算量はO(V + E)、空間計算量はO(V)。Vは頂点の数、Eは辺の総数
  - https://en.wikipedia.org/wiki/Breadth-first_search
  - https://en.wikipedia.org/wiki/Depth-first_search
- 時間計算量
  - 辺の総数はE = rows * (columns - 1) + (rows - 1) * columns = 2 * rows * columns - rows - columns → O(rows * column)
  - よって  O(rows × columns + rows * column) → O(rows × columns)

## Step2

### 他の人のコード
- https://github.com/hayashi-ay/leetcode/pull/33
  - https://github.com/hayashi-ay/leetcode/pull/33/changes#r1648958531
    - 陸を見つけては海に沈める方法
    - gridを破壊的に変更してしまうので注意が必要か
  - LAND、WATERを定数で定義
  - 四方の地点を訪れる方法
    - 自分の実装ではその地点が存在するか確認してから再帰で関数を呼び出す、hayashi-ayさんは関数を呼び出したあとに呼び出した関数の中でその土地があるかどうかを確認
    - 全実装通して一貫性を取れていたら問題なし→いや関数を呼び出してその関数内部でチェックする方が良いかも
      - > しかし、visit_island は、メソッド内のとはいえメソッドなので、雑に扱っても構わないものにしておきたい気持ちがあるんです。
      - https://github.com/sakupan102/arai60-practice/pull/18/changes#r1582062824
      - 使う人の立場に立って考える
  - https://github.com/hayashi-ay/leetcode/pull/33/changes#diff-225d97de8f43ab6e115258cc7d483e5a343d8556774b2dde47c392b38b49e89bR1
    - 確かに訪問済みの点を管理するのはsetやdictでも良いか。
    - (i,j)のtupleをキーにすれば良さそう
- https://github.com/fuga-98/arai60/pull/18
  - Union Find
    - https://github.com/fuga-98/arai60/pull/18/changes#diff-185178acbbe0f95b5d4592a56376ee4515fe16b8222f5310d8df82af478e666bR69
    - なんとなくわかった程度なので、コメント集読むタイミングでUnion Findについて調べたり実装したりする
- https://github.com/naoto-iwase/leetcode/pull/17
  - BFS, DFSの選択方法
    - 今回はどちら使っても良さそうだが、根拠を持ってそう判断したい
    - https://github.com/naoto-iwase/leetcode/pull/17/changes#diff-5c15b5a457745340b0829a41cc85d0ec21654a482447ccb1facec02bdcd5e432R11-R16
    - > - 1 <= m, n <= 300の長方形であり、グラフの幅が極端に広いわけでも、深いわけでもない（と思う）。
    - > - もし極端に幅が広いならOut of Memoryを考慮しDFSにする、など？
  - BFSでTTLと言っているが、自分はそうならなかった→違いを考える
    - popleftしたあとに取り出した地点がvisitedにあるかどうかチェックしているかどうかの違いがある
      - BFSでland_queueに加えたときにはvisitedになかったが取り出したときにはvisitedになっているものがある程度あると思われる
    - TTLを解消する方法
      - > 対策は「push 時に visited に入れる」か「push 時に grid を '0' などで潰す」ことです。
    - TTLを解消するのは以下でも可能
    - naoto-iwaseさんの実装を、popleftの直後にvisitedを確認するように書き直させていただいたところ、TTL解消できた
```Python3
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        def bfs_in_island(start: Tuple[int, int], visited: set): 
            land_queue = deque() 
            land_queue.append(start)
            while land_queue:
                land = land_queue.popleft()
                # これを加える
                if land in visited:
                    continue
                visited.add(land)
                for direction in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                    neighbor = (land[0] + direction[0], land[1] + direction[1])
                    if neighbor not in visited \
                        and 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) \
                        and grid[neighbor[0]][neighbor[1]] == "1":
                        land_queue.append(neighbor)
            return visited

        visited = set()
        count = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if (i, j) not in visited and grid[i][j] == "1":
                    count += 1
                    visited = bfs_in_island((i, j), visited)
        return count
```

- ここまで3人のPRを読んで
  - (0,0) から順に地点を見ていくのはwhileじゃなくてforの二重ループの方が一般的でわかりやすいかもな。やってること同じだし

- https://github.com/komdoroid/arai60/pull/14
  - 計算量の整理がわかりやすい
    > - 外側の2重ループについてO(num_rows * num_colums)
    > - while内で各マスが登場する回数は高々１回なので、O(num_rows * num_colums)
    > - directionsのループは定数
    > - 時間計算量:O(num_rows * num_columns)
    > - visitedとstackが最大全マス
    > - 空間計算量:O(num_rows * num_columns)
- https://github.com/tom4649/Coding/pull/16
  - DFS、BFSの比較
    - https://github.com/tom4649/Coding/pull/16/changes#diff-825ecb3e6129caf0d7bd9b568835a8864cdf20de9b12ac8863f17eb2fc4d8d04R7-R19
    > - 深さ優先探索と幅優先探索の比較
    >   - BFSは最短経路を見つけやすい
    >   - DFSは強連結成分、トポロジカルソート、サイクル検出、に応用できる
    >     - 強連結成分: DFSを行い帰りがけ順に番号を振る→辺を逆順にし番号が大きいものから再度DFS
    >     - トポロジカルソート: DFSで帰りがけ順に番号を振ればトポロジカルソートの逆順が得られる
    >     - サイクル検出: DFSで後退辺（探索中の頂点を訪れるか）を見る（この場合はvisitedを未訪問/探索中/探索完了で管理する）
- https://github.com/dorxyxki/arai60/pull/17
  - https://github.com/dorxyxki/arai60/pull/17/changes#diff-8f4b552352a653109e67c53b16609739ce9ebc36e1c5663fda5ba1c7f8365ed1R10
    - Pythonのrecursion limitは1,000
      - 公式Docには書いていなかったが、cpythonの実装では定義していあるか？
      ```cpp
      #  define Py_DEFAULT_RECURSION_LIMIT 1000
      ```
      - https://github.com/python/cpython/blob/main/Include/internal/pycore_ceval.h#L43
    - 再帰を書くときは再帰の上限をチェック。
    - recursion limitを取得できるメソッドもあるらしい
      - getrecursionlimit
      - https://docs.python.org/3/library/sys.html#sys.getrecursionlimit
  - gridが空の時は早期return
    - https://github.com/dorxyxki/arai60/pull/17/changes#diff-8f4b552352a653109e67c53b16609739ce9ebc36e1c5663fda5ba1c7f8365ed1R22-R23
  - 島を隅々までおとづれる関数名が良さげ: `explore_island`
    - https://github.com/dorxyxki/arai60/pull/17/changes#diff-09fdd9f2cb0a86ba6b7296e3f7b9d231b97045a5e2bffb2237d3f1b92c445c7bR28
  - `[(-1,0),(1,0),(0,-1),(0,1)]` のように隣接する点を今の場所からの差分で定義
    - https://github.com/dorxyxki/arai60/pull/17/changes#diff-09fdd9f2cb0a86ba6b7296e3f7b9d231b97045a5e2bffb2237d3f1b92c445c7bR12
  - https://github.com/dorxyxki/arai60/pull/17/changes#diff-09fdd9f2cb0a86ba6b7296e3f7b9d231b97045a5e2bffb2237d3f1b92c445c7bR37
    - `if inside_grid(next_row, next_col) and is_unvisited_land(next_row, next_col):` grid内部・未訪問の土地かを一つの関数にまとめるとわかりやすい
- https://github.com/kitano-kazuki/leetcode/pull/17
  - gridをdeepcopyした上で破壊的に変更するのは良さそう
    - deepcopyについて
      - https://docs.python.org/3/library/copy.html
      - deepcopyならば、再帰的に内部のオブジェクトもコピーされる
      - > A deep copy constructs a new compound object and then, recursively, inserts copies into it of the objects found in the original.
        
### コメント集
- https://discord.com/channels/1084280443945353267/1206101582861697046/1316539211779801148
  - > ここの部分は先にチェックするか一回 queue に入れて、後からチェックするかでしょう。
    繰り返しっぽいので範囲チェックを lambda にする手もあります
  - 地点が場面に収まっているかチェックする方法の幅
- https://discord.com/channels/1084280443945353267/1201211204547383386/1213387878734766080
  - swapで統一する
  - 処理のシンプルさは説明のシンプルさにつながる
- https://discord.com/channels/1084280443945353267/1295357747545505833/1306124175173222471
- https://discord.com/channels/1084280443945353267/1337642831824814192/1347398290030985279
  - > 上、下、右、左の順序で再帰していくので、確かにこれは場面全部を蛇腹状に埋める形で再帰が深くなっていきますね。
  - > これ島自体が蛇のようになっていなくても、左右を優先して探索して、その後上下を探索するので、蛇腹状に埋まっていきます。
  - 再帰の伸び方をイメージできた
- https://discord.com/channels/1084280443945353267/1227073733844406343/1234185601993932891
  - > メソッド内のとはいえメソッドなので、雑に扱っても構わないものにしておきたい気持ち
  - メソッドは他の人から引き受けて仕事を代行してあげる、引き受けた仕事には責任を持つイメージか
  - > そういうところも含めて読みやすいものにしたいので、上に条件を移したらという気持ちです。そうすると、読む方からすると、こういう条件を満たしている引数で呼んで欲しいのか、と分かるようになりますね。
- Union Find
  - [『問題解決力を鍛える！アルゴリズムとデータ構造』](https://www.kspub.co.jp/book/detail/5128442.html) にUnionFindの解説あり
    - union by sizeと経路圧縮をすることで統合する時の（ならし）計算量がO(α(N))となる
      - αはアッカーマンの逆関数でN<= 10^80でα(N)<=4なので、O(1)とみなせる
  - コメント集にも解説あり
    - https://discord.com/channels/1084280443945353267/1183683738635346001/1197738650998415500
    - 経路圧縮を現実世界に当てはめて
    - > 集団全員に対して、新しい全体の代表者の電話番号を通知することもできるのだが、それをしていると更新の時間が集団のサイズだけかかるので、それはしない。一方で、集団の代表者を探すときに、ボスのボスのボスと辿っていくので、「その電話リレーに巻き込まれた人だけ、代表者の電話番号を聞いておく(path compression)」ことで、次回たどる時間が短縮される。
  - 自分で実装してみる
```Python3
class UnionFind:
    def __init__(self, points: List[tuple[int, int]]) -> None:
        self.parents = {}
        # 根のサイズ（じゃなくなっても放置
        self.sizes = {}
        for point in points:
            self.parents[point] = point
            self.sizes[point] = 1
    
    def root(self, point: tuple[int, int]) -> tuple[int, int]:
        if self.parents[point] == point:
            return point
        
        # 経路圧縮
        self.parents[point] = self.root(self.parents[point])
        return self.parents[point]

    def unite(self, point1: tuple[int, int], point2: tuple[int, int]) -> None:
        # union by size
        bigger_root = self.root(point1)
        smaller_root = self.root(point2)
        if bigger_root == smaller_root:
            return

        if self.sizes[bigger_root] < self.sizes[smaller_root]:
            bigger_root, smaller_root = smaller_root, bigger_root

        self.parents[smaller_root] = bigger_root
        self.sizes[bigger_root] += self.sizes[smaller_root]
    
    def get_root_count(self) -> int:
        root_count = 0
        for parent, parent_of_parent in self.parents.items():
            if parent == parent_of_parent:
                root_count += 1
        return root_count

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        lands = []
        height = len(grid)
        width = len(grid[0])
        for i in range(height):
            for j in range(width):
                if grid[i][j] == "1":
                    lands.append((i, j))
        unionFind = UnionFind(lands)
        
        for land in lands:
            i, j = land
            if  i < height - 1 and grid[i+1][j] == "1":
                unionFind.unite(land, (i+1, j))
            if j < width -1 and grid[i][j+1] == "1":
                unionFind.unite(land, (i, j+1))

        return unionFind.get_root_count()
```

## Step3
- Step1でvisit_island関数でwaterだとしても`visited[i][j]`をTrueにしていたのはメソッド名とやっていることが一貫しておらずよくなかった。。。
- `visited = [[False] * width] * height`と `visited = [[False] * width for _ in range(height)]` は同じだと思っており少しハマった
  - オブジェクトはコピーされない旨、公式Docに書いてあった。。。（ちゃんと仕様を確認して使うべき）
  - > Note that items in the sequence s are not copied; they are referenced multiple times.
  - https://docs.python.org/3/library/stdtypes.html#typesseq-common

```Python3
class Solution:
    WATER = "0"
    LAND = "1"
    def numIslands(self, grid: List[List[str]]) -> int:
        height = len(grid)
        width = len(grid[0])
        visited = [[False] * width for _ in range(height)]

        def is_inside_grid(i: int, j: int) -> bool:
            return 0 <= i < height and 0 <= j < width

        def visit_island(start: tuple[int, int]) -> None:
            stack = deque()
            stack.append(start)
            while stack:
                i, j = stack.pop()
                if not is_inside_grid(i, j) or grid[i][j] == self.WATER or visited[i][j]:
                    continue
                visited[i][j] = True
                stack.append((i - 1, j))
                stack.append((i + 1, j))
                stack.append((i, j - 1))
                stack.append((i, j + 1))
        
        island_count = 0
        for i in range(height):
            for j in range(width):
                if not visited[i][j] and grid[i][j] == self.LAND:
                    island_count += 1
                    visit_island((i, j))
        return island_count

```

