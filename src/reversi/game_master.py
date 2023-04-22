from reversi_board import ReversiBoard
from player import ReversiPlayer, ReversiRandomPlayer, ReversiMinimaxPlayer
from typing import Optional


class ReversiGameMaster():
    def __init__(self, black_player: ReversiPlayer, white_player: ReversiPlayer):
        self.reversi_board = ReversiBoard()
        self.players = {
            ReversiBoard.Stone.BLACK: black_player,
            ReversiBoard.Stone.WHITE: white_player
        }
        self.current_player_color = ReversiBoard.Stone.BLACK

    def play_game(self) -> None:
        while not self.reversi_board.is_game_over():
            current_player = self.players[self.current_player_color]
            current_player.play(self.reversi_board)
            print(self.reversi_board)
            self.current_player_color = ReversiBoard.Stone.opposite(self.current_player_color)

    def get_winner(self) -> Optional[ReversiBoard.Stone]:
        black_count = self.reversi_board.count_stone(ReversiBoard.Stone.BLACK)
        white_count = self.reversi_board.count_stone(ReversiBoard.Stone.WHITE)
        if black_count > white_count:
            return ReversiBoard.Stone.BLACK
        elif black_count < white_count:
            return ReversiBoard.Stone.WHITE
        else:
            return None


if __name__=="__main__":
    black_player = ReversiRandomPlayer(ReversiBoard.Stone.BLACK)
    white_player = ReversiMinimaxPlayer(ReversiBoard.Stone.WHITE)
    game_master = ReversiGameMaster(black_player, white_player)
    game_master.play_game()
    if game_master.get_winner() is not None:
        print(f"Winner : {game_master.get_winner().value}")
    else:
        print("Draw")