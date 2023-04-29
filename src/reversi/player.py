from abc import ABC, abstractmethod
import random
from copy import deepcopy
from reversi_board import ReversiBoard
import curses
from typing import Tuple, List


class ReversiPlayer(ABC):
    def __init__(self, stone_color: ReversiBoard.Stone):
        self.stone_color = stone_color

    @abstractmethod
    def play(self, reversi_board: ReversiBoard) -> None:
        pass


class ReversiHumanPlayer(ReversiPlayer):
    def __init__(self, stone_color: ReversiBoard.Stone):
        super().__init__(stone_color)

    def play(self, reversi_board: ReversiBoard) -> None:
        placeable_positions = reversi_board.get_placeable_positions(self.stone_color)
        if not placeable_positions:
            print("No placeable position. Skipping your turn.")
            return

        chosen_position = self.__choose_position_with_arrow_keys(reversi_board, placeable_positions)
        put_x, put_y = chosen_position
        reversi_board.put_stone(put_x, put_y, self.stone_color)

    def __choose_position_with_arrow_keys(self, reversi_board: ReversiBoard, placeable_positions: List[Tuple[int, int]]) -> Tuple[int, int]:
        def display_positions(stdscr, select_index):
            stdscr.clear()
            stdscr.addstr(0, 0, "Current board:\n")
            displayed_board = str(reversi_board)
            displayed_board_rows = displayed_board.split('\n')
            selected_position_x, selected_position_y = placeable_positions[select_index]
            for row, line in enumerate(displayed_board_rows):
                if row == selected_position_y:
                    modified_line = list(line)
                    modified_line[2 * selected_position_x + 1] = str(self.stone_color.value)
                    line = ''.join(modified_line)
                stdscr.addstr(row + 1, 0, line)
            stdscr.addstr(10, 0, "Valid play:")
            for i, position in enumerate(placeable_positions):
                prefix = "->" if i == select_index else "  "
                stdscr.addstr(i + 11, 0, f"{prefix}: {position}")
            stdscr.refresh()

        def main(stdscr):
            curses.curs_set(0)
            current_index = 0
            while True:
                display_positions(stdscr, current_index)
                key = stdscr.getch()

                if key == curses.KEY_UP:
                    current_index = (current_index - 1) % len(placeable_positions)
                elif key == curses.KEY_DOWN:
                    current_index = (current_index + 1) % len(placeable_positions)
                elif key == ord('\n'):
                    break

            return placeable_positions[current_index]

        return curses.wrapper(main)

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