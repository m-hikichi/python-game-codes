from enum import Enum, unique
import random


# 迷路クラス
class Maze:
    """
    Mazeクラスは, 指定された大きさの迷路を生成するためのクラスです
    迷路は, フィールド・壁・スタート・ゴールの4種類のセルから構成されます
    迷路の生成には, 深さ優先探索を用いたバックトラッキング法を採用しています

    Attributes:
        width (int): 迷路の幅（セル数）. 奇数で指定する必要があります
        height (int): 迷路の高さ（セル数）. 奇数で指定する必要があります

    Raises:
        MazeError: 迷路の幅や高さが小さすぎる, もしくは偶数である場合に発生します

    Example:
        maze = Maze(21, 21)  # 幅21、高さ21の迷路を生成する
        print(maze)  # 生成された迷路を表示する
        (21, 21) = maze.get_size()  # 迷路のサイズを取得する
        cell = maze.get_cell(5, 7)  # 座標(5, 7)のセルの種類を取得する
    """

    @unique
    class Cell(Enum):
        FIELD = " "
        WALL = "■"
        START = "S"
        GOAL = "G"

    def __init__(self, width: int, height: int, start_x: int = 1, start_y: int = 1):
        """
        迷路クラスのコンストラクタ

        Args:
            width (int): 迷路の横幅
            height (int): 迷路の高さ
            start_x (int, optional): スタート地点のX座標. 既定値は1
            start_y (int, optional): スタート地点のY座標. 既定値は1

        Raises:
            MazeError: 迷路の幅または高さが小さすぎる場合, または偶数である場合に発生します

        """
        if width < 5 or height < 5:
            raise MazeError("Maze size is too small.")

        if width % 2 == 0 or height % 2 == 0:
            raise MazeError("Maze size must be specified in odd numbers.")

        self.width = width
        self.height = height
        self.__generate_maze(start_x, start_y)

    def __str__(self) -> str:
        """
        迷路を文字列として返す

        Returns:
            str: 迷路の文字列表現
        """
        output = ""
        for cells in self.__maze:
            for cell in cells:
                output += cell.value
            output += "\n"
        return output

    def __generate_maze(self, start_x: int, start_y: int):
        """
        迷路を生成する

        Args:
            start_x (int): スタート地点のX座標
            start_y (int): スタート地点のY座標
        """
        self.__maze = [[Maze.Cell.WALL] * self.width for h in range(self.height)]
        # スタートの設定
        self.__maze[start_y][start_x] = Maze.Cell.START
        # 迷路の作成
        self.__dig(start_x, start_y)
        # ゴールの設定
        self.__maze[self.height - 2][self.width - 2] = Maze.Cell.GOAL

    def __dig(self, x: int, y: int):
        """
        迷路を掘り進める

        Args:
            x (int): 現在のX座標
            y (int): 現在のY座標
        """
        @unique
        class Direction(Enum):
            UP = "u"
            RIGHT = "r"
            DOWN = "d"
            LEFT = "l"

        while True:
            directions = []
            # 掘り進められる方向の検索
            if y - 2 > 0 and self.__maze[y - 2][x] == Maze.Cell.WALL:
                directions.append(Direction.UP)
            if x - 2 > 0 and self.__maze[y][x - 2] == Maze.Cell.WALL:
                directions.append(Direction.RIGHT)
            if y + 2 < self.height and self.__maze[y + 2][x] == Maze.Cell.WALL:
                directions.append(Direction.DOWN)
            if x + 2 < self.width and self.__maze[y][x + 2] == Maze.Cell.WALL:
                directions.append(Direction.LEFT)

            # 掘り進める方向が存在しない場合は飛ばす
            if len(directions) == 0:
                break

            direction = random.choice(directions)
            if direction == Direction.UP:
                self.__maze[y - 1][x] = Maze.Cell.FIELD
                self.__maze[y - 2][x] = Maze.Cell.FIELD
                self.__dig(x, y - 2)
            if direction == Direction.RIGHT:
                self.__maze[y][x - 1] = Maze.Cell.FIELD
                self.__maze[y][x - 2] = Maze.Cell.FIELD
                self.__dig(x - 2, y)
            if direction == Direction.DOWN:
                self.__maze[y + 1][x] = Maze.Cell.FIELD
                self.__maze[y + 2][x] = Maze.Cell.FIELD
                self.__dig(x, y + 2)
            if direction == Direction.LEFT:
                self.__maze[y][x + 1] = Maze.Cell.FIELD
                self.__maze[y][x + 2] = Maze.Cell.FIELD
                self.__dig(x + 2, y)

    def get_size(self) -> (int, int):
        """
        迷路のサイズを取得する

        Returns
            tuple: 迷路の横幅と高さを格納したタプル
        """
        return (self.width, self.height)

    def get_cell(self, x: int, y: int) -> 'Cell':
        """
        指定された位置のセルの種類を取得する

        Args: 
        x (int): 取得するセルのX座標
        y (int): 取得するセルのY座標

        Returns
            Cell: 指定された位置の Cell オブジェクト
        """
        return self.__maze[y][x]


class MazeError(Exception):
    pass
