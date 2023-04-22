from abc import ABC, abstractmethod
import random
from copy import deepcopy
from reversi_board import ReversiBoard
from typing import Tuple


class ReversiPlayer(ABC):
    def __init__(self, stone_color: ReversiBoard.Stone):
        self.stone_color = stone_color

    @abstractmethod
    def play(self, reversi_board: ReversiBoard) -> None:
        pass


class ReversiRandomPlayer(ReversiPlayer):
    def __init__(self, stone_color: ReversiBoard.Stone):
        super().__init__(stone_color)

    def play(self, reversi_board: ReversiBoard) -> None:
        placeable_positions = reversi_board.get_placeable_positions(self.stone_color)
        if placeable_positions:
            selected_position = random.choice(placeable_positions)
            put_x, put_y = selected_position
            reversi_board.put_stone(put_x, put_y, self.stone_color)


class ReversiMinimaxPlayer(ReversiPlayer):
    def __init__(self, stone_color: ReversiBoard.Stone, search_depth: int=4):
        super().__init__(stone_color)
        self.search_depth = search_depth

    def play(self, reversi_board: ReversiBoard) -> None:
        _, best_play = self.__minimax(reversi_board, self.search_depth, self.stone_color)
        if best_play:
            put_x, put_y = best_play
            reversi_board.put_stone(put_x, put_y, self.stone_color)

    def __minimax(self, reversi_board: ReversiBoard, depth: int, player_color: ReversiBoard.Stone) -> (int, Tuple[int, int]):
        if depth == 0 or reversi_board.is_game_over():
            return self.__evaluate(reversi_board, player_color), None
    
        placeable_positions = reversi_board.get_placeable_positions(player_color)
        if not placeable_positions:
            return self.__evaluate(reversi_board, player_color), None

        best_score = float("-inf") if player_color == self.stone_color else float("inf")
        best_play = None
        for placeable_position in placeable_positions:
            put_x, put_y = placeable_position
            new_board = deepcopy(reversi_board)
            new_board.put_stone(put_x, put_y, player_color)
            score, _ = self.__minimax(new_board, depth - 1, ReversiBoard.Stone.opposite(player_color))

            if player_color == self.stone_color:
                if score > best_score:
                    best_score = score
                    best_play = placeable_position
            else:
                if score < best_score:
                    best_score = score
                    best_play = placeable_position
        return best_score, best_play

    def __evaluate(self, reversi_board: ReversiBoard, player_color: ReversiBoard.Stone) -> int:
        my_stone_count = reversi_board.count_stone(player_color)
        opponent_stone_count = reversi_board.count_stone(ReversiBoard.Stone.opposite(player_color))
        return my_stone_count - opponent_stone_count