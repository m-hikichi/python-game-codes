import pytest
from src.reversi.reversi_board import ReversiBoard


@pytest.mark.parametrize(
    "input, ans",
    [
        (ReversiBoard.Stone.BLACK, ReversiBoard.Stone.WHITE),
        (ReversiBoard.Stone.WHITE, ReversiBoard.Stone.BLACK),
        (ReversiBoard.Stone.EMPTY, None),
    ],
)
def test_opposite_stone(input, ans):
    # GIVEN

    # WHEN
    ret = ReversiBoard.Stone.opposite(input)

    # THEN
    assert ret == ans


@pytest.fixture()
def init_reversi():
    return ReversiBoard()


def test_init_reversi(init_reversi):
    # GIVEN

    # WHEN
    reversi = init_reversi

    # THEN
    assert reversi.count_stone(ReversiBoard.Stone.BLACK) == 2
    assert reversi.count_stone(ReversiBoard.Stone.WHITE) == 2
    assert reversi.get_stone(3, 3) == ReversiBoard.Stone.BLACK
    assert reversi.get_stone(4, 4) == ReversiBoard.Stone.BLACK
    assert reversi.get_stone(3, 4) == ReversiBoard.Stone.WHITE
    assert reversi.get_stone(4, 3) == ReversiBoard.Stone.WHITE


def test_get_placeable_positions(init_reversi):
    # GIVEN

    # WHEN
    reversi = init_reversi

    # THEN
    assert set([(4, 2), (5, 3), (2, 4), (3, 5)]) == set(reversi.get_placeable_positions(ReversiBoard.Stone.BLACK))
    assert set([(3, 2), (2, 3), (5, 4), (4, 5)]) == set(reversi.get_placeable_positions(ReversiBoard.Stone.WHITE))


def test_put_stone(init_reversi):
    # GIVEN
    reversi = init_reversi

    # WHEN
    reversi.put_stone(2, 4, ReversiBoard.Stone.BLACK)

    # THEN
    assert reversi.count_stone(ReversiBoard.Stone.BLACK) == 4
    assert reversi.count_stone(ReversiBoard.Stone.WHITE) == 1
    assert reversi.get_stone(3, 3) == ReversiBoard.Stone.BLACK
    assert reversi.get_stone(4, 4) == ReversiBoard.Stone.BLACK
    assert reversi.get_stone(3, 4) == ReversiBoard.Stone.BLACK
    assert reversi.get_stone(2, 4) == ReversiBoard.Stone.BLACK
    assert reversi.get_stone(4, 3) == ReversiBoard.Stone.WHITE
