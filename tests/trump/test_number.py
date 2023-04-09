import pytest
from src.trump.trump import Number


def test_Number():
    # GIVEN

    # WHEN

    # THEN
    assert len(Number) == 13

    for i, number in enumerate(Number, start=1):
        assert number.num == i


@pytest.mark.parametrize(
    "input, ans",
    [
        (0, None),
        (1, Number.ACE),
        (2, Number.TWO),
        (3, Number.THREE),
        (4, Number.FOUR),
        (5, Number.FIVE),
        (6, Number.SIX),
        (7, Number.SEVEN),
        (8, Number.EIGHT),
        (9, Number.NINE),
        (10, Number.TEN),
        (11, Number.JACK),
        (12, Number.QUEEN),
        (13, Number.KING),
        (14, None),
    ],
)
def test_int2Number(input, ans):
    # GIVEN

    # WHEN
    ret = Number.int2Number(input)

    # THEN
    assert ret == ans


@pytest.mark.parametrize(
    "input, ans",
    [
        ("A", Number.ACE),
        ("2", Number.TWO),
        ("3", Number.THREE),
        ("4", Number.FOUR),
        ("5", Number.FIVE),
        ("6", Number.SIX),
        ("7", Number.SEVEN),
        ("8", Number.EIGHT),
        ("9", Number.NINE),
        ("10", Number.TEN),
        ("J", Number.JACK),
        ("Q", Number.QUEEN),
        ("K", Number.KING),
        ("", None),
        (None, None),
    ],
)
def test_mark2Number(input, ans):
    # GIVEN

    # WHEN
    ret = Number.mark2Number(input)

    # THEN
    assert ret == ans
