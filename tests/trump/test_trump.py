import pytest
from src.trump.trump import Suit, Number, Trump


@pytest.fixture()
def trump():
    return Trump()


def test_trump(trump):
    # GIVEN
    # テストするトランプのインスタンスが渡されたことを確認する
    trump = trump

    # WHEN
    # 何もしない（トランプのインスタンスが作成されたときに52枚のカードが追加されるため）

    # THEN
    # トランプのインスタンスに含まれるカードの枚数が52枚であることを確認する
    assert len(trump) == 52


def test_shuffle(trump):
    # GIVEN
    trump = trump
    before_shuffle_card_sequence = str(trump)

    # WHEN
    # カードをシャッフルする
    trump.shuffle()
    after_shuffle_card_sequence = str(trump)

    # THEN
    # シャッフル後の残りのカード枚数が52枚であることを確認する
    assert len(trump) == 52
    # シャッフル前後でカードの順序が変化したことを確認する
    assert before_shuffle_card_sequence != after_shuffle_card_sequence


@pytest.mark.parametrize("draw_count, expected_card_count",
    [(1, 51), (52, 0), (53, 0)],
)
def test_draw(trump, draw_count, expected_card_count):
    # GIVEN
    trump = trump

    # WHEN
    # 指定された枚数のカードを引く
    for i in range(draw_count):
        trump.draw()

    # THEN
    # 残りのカード枚数が期待される数であることを確認する
    assert len(trump) == expected_card_count


@pytest.mark.parametrize(
    "suit, number, expected_search_result_count",
    [
        (Suit.SPADE, None, 13),
        (None, Number.ACE, 4),
        (Suit.SPADE, Number.ACE, 1),
        (None, None, 0),
    ],
)
def test_search(trump, suit, number, expected_search_result_count):
    # GIVEN
    trump = trump

    # WHEN
    # 指定されたスートと数字を使って検索を実行する
    search_result = trump.search(suit=suit, number=number)

    # THEN
    # 検索結果の数が期待される数であることを確認する
    assert len(search_result) == expected_search_result_count
