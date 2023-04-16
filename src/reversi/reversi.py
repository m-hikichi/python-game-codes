from enum import Enum, unique
from typing import Tuple


class Reversi:
    WIDTH = 8
    HEIGHT = 8

    @unique
    class Stone(Enum):
        EMPTY = " "
        BLACK = "○"
        WHITE = "●"

        @classmethod
        def opposite(cls, stone_color: 'Reversi.Stone') -> 'Reversi.Stone':
            if stone_color == cls.BLACK:
                return cls.WHITE
            elif stone_color == cls.WHITE:
                return cls.BLACK
            else:
                return None

    def __init__(self):
        self.__board = [
            [Reversi.Stone.EMPTY for w in range(Reversi.WIDTH)] for h in range(Reversi.HEIGHT)
        ]
        self.__board[3][3] = Reversi.Stone.BLACK
        self.__board[4][4] = Reversi.Stone.BLACK
        self.__board[3][4] = Reversi.Stone.WHITE
        self.__board[4][3] = Reversi.Stone.WHITE

    def __str__(self) -> str:
        """
        ボードを文字列として返す

        Retruns:
            str: ボードの文字列表現
        """
        output = ""
        for rows in self.__board:
            for stone in rows:
                output += stone.value
            output += "\n"
        return output

    def put_stone(self, x: int, y: int, stone_color: Stone) -> None:
        """
        与えられた位置に石を置き，ボードを更新する

        Args:
            x (int): 位置を置く位置の x 座標
            y (int): 位置を置く位置の y 座標
            stone_color (Stone): 置く石の色（BLACKまたはWHITE）
        """
        opposite_stone_color = Reversi.Stone.opposite(stone_color)
        for x_vec, y_vec in Reversi.__get_directions():
            # 確認方向に反対色の石がない場合は，処理を飛ばす
            if self.__board[y + y_vec][x + x_vec] != opposite_stone_color:
                continue
            self.__flip_stones_in_direction(x, y, x_vec, y_vec, stone_color)

    def __flip_stones_in_direction(self, x: int, y: int, x_vec: int, y_vec: int, stone_color: Stone) -> None:
        """
        可能であれば，指定された位置・方向で石をひっくり返す

        Args:
            x (int): 開始位置の x 座標
            y (int): 開始位置の y 座標
            x_vec (int): 方向の x オフセット
            y_vec (int): 方向の y オフセット
            stone_color (Reversi.Stone): 置く石の色（BLACKまたはWHITE）
        """
        for step in range(1, 8):
            x_pos = x + x_vec * step
            y_pos = y + y_vec * step

            # 盤面外の場合は処理をスキップ
            if not Reversi.__is_valid_position(x_pos, y_pos):
                break

            # 指定した色の石が見つかる前に，空きがある場合は置き換えることができないので，処理を飛ばす
            if self.__board[y_pos][x_pos] == Reversi.Stone.EMPTY:
                break

            # 指定した色の石が見つかった場合，あいだの石を置き換える
            if self.__board[y_pos][x_pos] == stone_color:
                for s in range(step):
                    self.__board[y + y_vec * s][x + x_vec * s] = stone_color
                break

    def count_stone(self, stone_color: Stone) -> int:
        """
        指定された石の色の数をカウントする

        Args:
            stone_color (Reversi.Stone): カウントする石の色

        Returns:
            int: 指定された石の色の数
        """
        count = 0
        for rows in self.__board:
            for stone in rows:
                if stone_color == stone:
                    count += 1
        return count

    def get_stone(self, x: int, y: int) -> Stone:
        """
        指定された座標の石を取得する

        Args:
            x (int): 取得する石の x 座標
            y (int): 取得する石の y 座標

        Returns:
            Reversi.Stone: 指定された座標の石
        """
        return self.__board[y][x]

    @classmethod
    def __get_directions(cls) -> Tuple[int, int]:
        """
        周囲の石を確認するためのすべての可能な方向（8方向）を生成する

        Returns:
            x 方向 と y 方向 のオフセットのタプル
        """
        for x_vec in [-1, 0, 1]:
            for y_vec in [-1, 0, 1]:
                if x_vec == 0 and y_vec == 0:
                    continue
                yield x_vec, y_vec

    @classmethod
    def __is_valid_position(cls, x: int, y: int) -> bool:
        """
        与えられた位置がボード内にあるかどうかを確認する

        Args:
            x (int): 確認する位置の x 座標
            y (int): 確認する位置の y 座標

        Returns:
            bool: 位置がボード内にある場合は True, ボード外の場合は False
        """
        return 0 <= x < cls.WIDTH and 0 <= y < cls.HEIGHT
