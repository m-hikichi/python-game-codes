import pytest
from src.trump.trump import Suit


def test_Suit():
    # GIVEN
    suit_mark_list = [
        "♠",
        "♡",
        "♢",
        "♣",
    ]

    # WHEN

    # THEN
    assert len(Suit) == 4

    for suit, suit_mark in zip(Suit, suit_mark_list):
        assert suit.mark == suit_mark


@pytest.mark.parametrize(
    "input, ans",
    [
        ("♠", Suit.SPADE),
        ("♤", Suit.SPADE),
        ("♥", Suit.HEART),
        ("♡", Suit.HEART),
        ("♦", Suit.DIA),
        ("♢", Suit.DIA),
        ("♣", Suit.CLUB),
        ("♧", Suit.CLUB),
    ],
)
def test_mark2Suit(input, ans):
    # GIVEN

    # WHEN
    ret = Suit.mark2Suit(input)

    # THEN
    assert ret == ans
