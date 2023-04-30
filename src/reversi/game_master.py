from reversi_board import ReversiBoard
from player import *
from typing import Optional


class ReversiGameMaster():
    def __init__(self, black_player: ReversiPlayer, white_player: ReversiPlayer):
        self.__reversi_board = ReversiBoard()

        if black_player.get_stone_color() != ReversiBoard.Stone.BLACK:
            raise InvalidStoneColorError("Black player must have BLACK stone color.")
        if white_player.get_stone_color() != ReversiBoard.Stone.WHITE:
            raise InvalidStoneColorError("White player must have WHITE stone color")
        self.__players = {
            ReversiBoard.Stone.BLACK: black_player,
            ReversiBoard.Stone.WHITE: white_player
        }
        self.__current_player_color = ReversiBoard.Stone.BLACK

    def play_game(self) -> None:
        while not self.__reversi_board.is_game_over():
            current_player = self.__players[self.__current_player_color]
            current_player.play(self.__reversi_board)
            print(self.__reversi_board)
            self.__current_player_color = ReversiBoard.Stone.opposite(self.__current_player_color)

    def get_winner(self) -> Optional[ReversiBoard.Stone]:
        black_count = self.__reversi_board.count_stone(ReversiBoard.Stone.BLACK)
        white_count = self.__reversi_board.count_stone(ReversiBoard.Stone.WHITE)
        if black_count > white_count:
            return ReversiBoard.Stone.BLACK
        elif black_count < white_count:
            return ReversiBoard.Stone.WHITE
        else:
            return None


class InvalidStoneColorError(Exception):
    pass


if __name__=="__main__":
    black_player = ReversiRandomPlayer(ReversiBoard.Stone.BLACK)
    white_player = ReversiHumanPlayer(ReversiBoard.Stone.WHITE)
    game_master = ReversiGameMaster(black_player, white_player)
    game_master.play_game()
    if game_master.get_winner() is not None:
        print(f"Winner : {game_master.get_winner().value}")
    else:
        print("Draw")