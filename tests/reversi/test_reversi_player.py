import pytest
from src.reversi.player import *


@pytest.mark.parametrize(
    "class_name, stone_color",
    [
        (ReversiRandomPlayer, ReversiBoard.Stone.BLACK),
        (ReversiRandomPlayer, ReversiBoard.Stone.WHITE),
        (ReversiMinimaxPlayer, ReversiBoard.Stone.BLACK),
        (ReversiMinimaxPlayer, ReversiBoard.Stone.WHITE),
        (ReversiHumanPlayer, ReversiBoard.Stone.BLACK),
        (ReversiHumanPlayer, ReversiBoard.Stone.WHITE),
    ]
)
def test_init_reversi_player(class_name, stone_color):
    # GIVEN

    # WHEN
    player = class_name(stone_color)

    # THEN
    assert player.get_stone_color() == stone_color


@pytest.mark.parametrize(
    "class_name, stone_color",
    [
        (ReversiRandomPlayer, ReversiBoard.Stone.EMPTY),
        (ReversiRandomPlayer, 0),
        (ReversiRandomPlayer, "ABC"),
        (ReversiMinimaxPlayer, ReversiBoard.Stone.EMPTY),
        (ReversiMinimaxPlayer, 0),
        (ReversiMinimaxPlayer, "ABC"),
        (ReversiHumanPlayer, ReversiBoard.Stone.EMPTY),
        (ReversiHumanPlayer, 0),
        (ReversiHumanPlayer, "ABC"),
    ]
)
def test_init_reversi_player_error(class_name, stone_color):
    # GIVEN

    # WHEN
    with pytest.raises(ValueError) as e:
        player = class_name(stone_color)

    # THEN
    assert str(e.value) == "Invalid stone color. Must be either ReversiBoard.Stone.BLACK or ReversiBoard.Stone.WHITE"