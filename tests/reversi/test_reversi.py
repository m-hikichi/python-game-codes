import pytest
from src.reversi.reversi import Reversi


@pytest.mark.parametrize(
    "input, ans",
    [
        (Reversi.Stone.BLACK, Reversi.Stone.WHITE),
        (Reversi.Stone.WHITE, Reversi.Stone.BLACK),
        (Reversi.Stone.EMPTY, None),
    ],
)
def test_opposite_stone(input, ans):
    # GIVEN

    # WHEN
    ret = Reversi.Stone.opposite(input)

    # THEN
    assert ret == ans


@pytest.fixture()
def init_reversi():
    return Reversi()


def test_init_reverisi(init_reversi):
    # GIVEN

    # WHEN
    reversi = init_reversi

    # THEN
    assert reversi.count_stone(Reversi.Stone.BLACK) == 2
    assert reversi.count_stone(Reversi.Stone.WHITE) == 2
    assert reversi.get_stone(3, 3) == Reversi.Stone.BLACK
    assert reversi.get_stone(4, 4) == Reversi.Stone.BLACK
    assert reversi.get_stone(3, 4) == Reversi.Stone.WHITE
    assert reversi.get_stone(4, 3) == Reversi.Stone.WHITE


def test_get_placeable_position(init_reversi):
    # GIVEN

    # WHEN
    reversi = init_reversi

    # THEN
    assert set([(4, 2), (5, 3), (2, 4), (3, 5)]) == set(reversi.get_placeable_position(Reversi.Stone.BLACK))
    assert set([(3, 2), (2, 3), (5, 4), (4, 5)]) == set(reversi.get_placeable_position(Reversi.Stone.WHITE))


def test_put_stone(init_reversi):
    # GIVEN
    reversi = init_reversi

    # WHEN
    reversi.put_stone(2, 4, Reversi.Stone.BLACK)

    # THEN
    assert reversi.count_stone(Reversi.Stone.BLACK) == 4
    assert reversi.count_stone(Reversi.Stone.WHITE) == 1
    assert reversi.get_stone(3, 3) == Reversi.Stone.BLACK
    assert reversi.get_stone(4, 4) == Reversi.Stone.BLACK
    assert reversi.get_stone(3, 4) == Reversi.Stone.BLACK
    assert reversi.get_stone(2, 4) == Reversi.Stone.BLACK
    assert reversi.get_stone(4, 3) == Reversi.Stone.WHITE
