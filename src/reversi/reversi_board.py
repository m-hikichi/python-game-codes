from enum import Enum, unique
from typing import Tuple, List


class ReversiBoard:
    WIDTH = 8
    HEIGHT = 8

    @unique
    class Stone(Enum):
        EMPTY = " "
        BLACK = "○"
        WHITE = "●"

        @classmethod
        def opposite(cls, stone_color: 'ReversiBoard.Stone') -> 'ReversiBoard.Stone':
            if stone_color == cls.BLACK:
                return cls.WHITE
            elif stone_color == cls.WHITE:
                return cls.BLACK
            else:
                return None

    def __init__(self):
        self.__board = [
            [ReversiBoard.Stone.EMPTY for w in range(ReversiBoard.WIDTH)] for h in range(ReversiBoard.HEIGHT)
        ]
        self.__board[3][3] = ReversiBoard.Stone.BLACK
        self.__board[4][4] = ReversiBoard.Stone.BLACK
        self.__board[3][4] = ReversiBoard.Stone.WHITE
        self.__board[4][3] = ReversiBoard.Stone.WHITE

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

    def get_placeable_positions(self, stone_color: Stone) -> List[Tuple[int, int]]:
        """
        指定された石の色に対して，盤面上で置くことができる全ての座標のリストを返す

        Args:
            stone_color (Stone): 石の色

        Returns:
            List[Tuple[int, int]]: 石を置くことができる座標のリスト，各座標は(x, y)の形式
        """
        placeable_position = []
        for y in range(ReversiBoard.HEIGHT):
            for x in range(ReversiBoard.WIDTH):
                # 対象の座標に石を置けるかを確認
                if self.__is_placeable_position(x, y, stone_color):
                    placeable_position.append((x, y))
        return placeable_position

    def __is_placeable_position(self, x: int, y: int, stone_color: Stone) -> bool:
        """
        指定された座標に指定された石の色を置くことができるかどうか判定する

        Args:
            x (int): 確認する位置の x 座標
            y (int): 確認する位置の y 座標
            stone_color (Stone): 置く石の色

        Returns:
            bool: 指定された座標に指定された石の色を置くことができる場合はTrue, できない場合はFalse
        """
        # 指定された座標にすでに石がある場合，Falseを返す
        if self.__board[y][x] != ReversiBoard.Stone.EMPTY:
            return False
        
        opposite_stone_color = ReversiBoard.Stone.opposite(stone_color)
        for x_vec, y_vec in self.__get_directions():
            # 盤面外，または確認方向に反対色の石がない場合は，次の方向をチェック
            if not self.__is_valid_position(x + x_vec, y + y_vec) or self.__board[y + y_vec][x + x_vec] != opposite_stone_color:
                continue

            for step in range(1, 8):
                x_pos = x + x_vec * step
                y_pos = y + y_vec * step

                # 盤面外の場合は処理をスキップ
                if not self.__is_valid_position(x_pos, y_pos):
                    break

                # 指定した色の石が見つかる前に，空きがある場合は置き換えることができないので，処理を飛ばす
                if self.__board[y_pos][x_pos] == ReversiBoard.Stone.EMPTY:
                    break
                
                # 反対色の石を挟むことができる場合，Trueを返す
                if self.__board[y_pos][x_pos] == stone_color:
                    return True
        return False

    def put_stone(self, x: int, y: int, stone_color: Stone) -> None:
        """
        与えられた位置に石を置き，ボードを更新する

        Args:
            x (int): 位置を置く位置の x 座標
            y (int): 位置を置く位置の y 座標
            stone_color (Stone): 置く石の色（BLACKまたはWHITE）
        """
        opposite_stone_color = ReversiBoard.Stone.opposite(stone_color)
        for x_vec, y_vec in ReversiBoard.__get_directions():
            # 盤面外，または確認方向に反対色の石がない場合は，次の方向をチェック
            if not self.__is_valid_position(x + x_vec, y + y_vec) or self.__board[y + y_vec][x + x_vec] != opposite_stone_color:
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
            stone_color (ReversiBoard.Stone): 置く石の色（BLACKまたはWHITE）
        """
        for step in range(1, 8):
            x_pos = x + x_vec * step
            y_pos = y + y_vec * step

            # 盤面外の場合は処理をスキップ
            if not self.__is_valid_position(x_pos, y_pos):
                break

            # 指定した色の石が見つかる前に，空きがある場合は置き換えることができないので，処理を飛ばす
            if self.__board[y_pos][x_pos] == ReversiBoard.Stone.EMPTY:
                break

            # 指定した色の石が見つかった場合，あいだの石を置き換える
            if self.__board[y_pos][x_pos] == stone_color:
                for s in range(step):
                    self.__board[y + y_vec * s][x + x_vec * s] = stone_color
                break

    def is_game_over(self) -> bool:
        """
        ゲームを続行できないかどうかを確認する，つまり黒も白も石を置けない状態になったかを確認する

        Returns:
            bool: ゲームが終了ならTrue, ゲームを続行できる場合はFalse
        """
        black_placeable_postions = self.get_placeable_positions(ReversiBoard.Stone.BLACK)
        white_placeable_postions = self.get_placeable_positions(ReversiBoard.Stone.WHITE)
        return not (black_placeable_postions or white_placeable_postions)


    def count_stone(self, stone_color: Stone) -> int:
        """
        指定された石の色の数をカウントする

        Args:
            stone_color (ReversiBoard.Stone): カウントする石の色

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
            ReversiBoard.Stone: 指定された座標の石
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
