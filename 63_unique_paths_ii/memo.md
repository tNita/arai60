## 63. Unique Paths II

You are given an m x n integer array grid. There is a robot initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.

An obstacle and space are marked as 1 or 0 respectively in grid. A path that the robot takes cannot include any square that is an obstacle.

Return the number of possible unique paths that the robot can take to reach the bottom-right corner.

The testcases are generated so that the answer will be less than or equal to 2 * 109.

Constraints

- m == obstacleGrid.length
- n == obstacleGrid[i].length
- 1 <= m, n <= 100
- obstacleGrid[i][j] is 0 or 1.

## Step1
- grid[i][j]の経路数はgrid[i-1][j] + grid[i][j - 1]
- マス目ごとに経路数を記録する
- 障害がある箇所は経路数を0にする
- 一次元のDPと2次元のDPでできそう

```Python3
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:
        row = len(obstacleGrid)
        column = len(obstacleGrid[0])
        paths = [[0] * column for _ in range(row)]
        for i in range(row):
            for j in range(column):
                if obstacleGrid[i][j] == 1:
                    paths[i][j] = 0
                    continue
                if i == 0 and j == 0:
                    paths[i][j] = 1
                    continue
                paths[i][j] = paths[i - 1][j] + paths[i][j - 1]
        return paths[row - 1][column - 1]
```

```Python3
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:
        row = len(obstacleGrid)
        column = len(obstacleGrid[0])
        paths = [0] * column
        for j in range(column):
            if obstacleGrid[0][j] == 1:
                break
            paths[j] = 1
        for i in range(1, row):
            for j in range(0, column):
                if obstacleGrid[i][j] == 1:
                    paths[j] = 0
                    continue
                # j == 0は何もしない。paths[j]をそのまま引き継げばよいので。
                if j > 0:
                    paths[j] = paths[j] + paths[j - 1]
        return paths[-1]
```

## Step2
- https://github.com/olsen-blue/Arai60/pull/34#discussion_r1968666138
  - > コードを書くというのはすべて地雷の埋設(使われなくなるまでに爆発しなければ勝ち)くらいに思っておくといいでしょう。作る時にだいたいどれくらいで爆発するか見積もります。また、壊れるにしても安全に壊れて欲しいです。ユーザーに届く前に事前に気がつくとか不完全ながらも結果は返るとか止まって異常があったことが分かるとか何がいいかは状況次第です。
- https://github.com/Fuminiton/LeetCode/pull/34#discussion_r2052772608
  - > [0][0]にアクセスする前に一応チェックしてもいいかもしれませんね。問題文に制約があるにせよ。
  - 空のgridを考慮できていなかった。。。
  - 制約があるとしても今後のその制約は破られていく可能性がある
- https://github.com/fuga-98/arai60/pull/34
  - マジックナンバー使うの避ける
  - dead_endを用意して障害物のせいで先に進めないことがわかった段階で処理を終了する
- https://github.com/kazuki-official/leetcode/pull/34
  - 1次元のDPで２つリストを用意するパターン
  - 再帰でやるパターン
- https://github.com/mamo3gr/arai60/pull/32
  - itertools.productでインデント一つ下げれる
  - 上の経路数、左の経路数を命名していて、わかりやすい

## Step3
一次元配列でやる。

一つ前の列の配列と対象の列の配列２つを使ってやるパターンが直感的で良いと思った。

```Python3
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:
        OBSTACLE = 1
        grid_rows = len(obstacleGrid)
        grid_columns = len(obstacleGrid[0])
        if grid_rows == 0:
            raise ValueError("行数は1以上にしてください")
        if grid_columns == 0:
            raise ValueError("列数は1以上にしてください")
        
        previous_unique_paths = [0] * grid_columns
        for column in range(grid_columns):
            if obstacleGrid[0][column] == OBSTACLE:
                previous_unique_paths[column] = 0
                continue
            if column == 0:
                previous_unique_paths[column] = 1
                continue
            previous_unique_paths[column] = previous_unique_paths[column - 1]

        for row in range(1, grid_rows):
            unique_paths = [0] * grid_columns
            for column in range(grid_columns):
                if obstacleGrid[row][column] == OBSTACLE:
                    unique_paths[column] = 0
                    continue
                if column == 0:
                    unique_paths[column] = previous_unique_paths[column]
                    continue
                unique_paths[column] = previous_unique_paths[column] + unique_paths[column - 1]
            previous_unique_paths = unique_paths
        return previous_unique_paths[-1]
```