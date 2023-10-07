from pathlib import Path
from enum import Enum, unique
import random
from typing import List


@unique
class Suit(Enum):
    """
    トランプのマークを表す列挙型

    Attributes:
        SPADE (Suit): スペード
        HEART (Suit): ハート
        DIA (Suit): ダイヤ
        CLUB (Suit): クラブ
        JOKER (Suit): ジョーカー
    """
    SPADE = "♠"
    HEART = "♡"
    DIA = "♢"
    CLUB = "♣"
    JOKER = "JOKER"

    def __init__(self, mark):
        self.mark = mark

    @staticmethod
    def mark2Suit(mark: str) -> 'Suit':
        """
        マークを表す記号を Suit に変換する静的メソッド

        Args:
            mark (str): マークを表す記号

        Returns:
            Suit or None: マークに対応する Suit オブジェクト
                          マークが不正な場合は None を返す
        """
        if mark == "♤":
            mark = "♠"
        if mark == "♥":
            mark = "♡"
        if mark == "♦":
            mark = "♢"
        if mark == "♧":
            mark = "♣"

        for s in Suit:
            if s.mark == mark:
                return s


@unique
class Number(Enum):
    """
    トランプの数字を表す列挙型です

    Attributes
    ----------
    ACE : Number
        エースを表します
    TWO : Number
        2を表します
    THREE : Number
        3を表します
    FOUR : Number
        4を表します
    FIVE : Number
        5を表します
    SIX : Number
        6を表します
    SEVEN : Number
        7を表します
    EIGHT : Number
        8を表します
    NINE : Number
        9を表します
    TEN : Number
        10を表します
    JACK : Number
        ジャックを表します
    QUEEN : Number
        クイーンを表します
    KING : Number
        キングを表します
    """
    ACE = (1, "A")
    TWO = (2, "2")
    THREE = (3, "3")
    FOUR = (4, "4")
    FIVE = (5, "5")
    SIX = (6, "6")
    SEVEN = (7, "7")
    EIGHT = (8, "8")
    NINE = (9, "9")
    TEN = (10, "10")
    JACK = (11, "J")
    QUEEN = (12, "Q")
    KING = (13, "K")

    def __init__(self, num, mark):
        self.num = num
        self.mark = mark

    @staticmethod
    def int2Number(num: int) -> 'Number':
        """
        整数を Number に変換する静的メソッド

        Args:
            num (int): 変換したい整数

        Returns:
            Number or None: 引数で指定された整数に対応する Number オブジェクト
                            引数が1から13までの整数でない場合は, None を返す
        """
        for n in Number:
            if n.num == num:
                return n

    @staticmethod
    def mark2Number(mark: str) -> 'Number':
        """
        文字列を Number に変換する静的メソッド

        Args:
            mark (str): 変換したい文字列. A, 2, 3, ..., 10, J, Q, Kのいずれか

        Returns:
            Number or None: 引数で指定された文字列に対応する Number オブジェクト
                            引数が正しい文字列でない場合は, None を返す
        """
        for n in Number:
            if n.mark == mark:
                return n


class Card:
    """
    トランプのカードを表すクラス

    Attributes:
        suit (Suit): スート
        number (Number): 数字
    """

    def __init__(self, suit: Suit, number: Number):
        """
        コンストラクタ

        Args:
            suit (Suit): スート
            number (Number): 数字
        """
        self.suit = suit
        self.number = number

    def __del__(self):
        """
        デコンストラクタ. 何もしない
        """
        # print("delete : " + self.suit.mark + "-" + self.number.mark)
        pass

    def __str__(self) -> str:
        """
        カードのスートと数字を表示する

        Returns:
            str: カードのスートと数字. 例: "♠︎-A", "♠︎-2", "♡-K", "JOKER"
        """
        if self.suit == Suit.JOKER:
            return self.suit.mark
        else:
            return self.suit.mark + "-" + self.number.mark


class Trump:
    """
    トランプの一組を表すクラス
    
    Attributes:
        card_list (list): トランプのカードを表すCardオブジェクトのリスト
    
    Methods:
        __init__(): トランプ一組を初期化する（JOKERを含む場合:54枚, JOKERを含まない場合:52枚）
        __str__(): カードリストの文字列表現を返す
        __len__(): 残りのカード枚数を返す
        shuffle(): カードをシャッフルする
        draw(): カードを引く. カードが残っていない場合にはFalseを返す
        search(suit=None, number=None): カードを検索する. suitやnumberに指定がある場合, 条件に一致するカードを返す
    """

    def __init__(self, include_jokers: bool=False):
        """
        トランプ一組を初期化する（JOKERを含む場合:54枚, JOKERを含まない場合:52枚）
        """
        self.card_list = []
        for s in Suit:
            if s == Suit.JOKER:
                continue
            for n in Number:
                self.card_list.append(Card(suit=s, number=n))
        if include_jokers:
            self.card_list.append(Card(suit=Suit.JOKER, number=None))
            self.card_list.append(Card(suit=Suit.JOKER, number=None))

    def __str__(self) -> str:
        """
        カードリストの文字列表現を返す
        
        Returns:
            str: カードリストの文字列表現
        """
        return "\n".join(str(card) for card in self.card_list)

    def __len__(self) -> int:
        """
        残りのカード枚数を返す

        Returns:
            int: 残りのカード枚数
        """
        return len(self.card_list)

    def shuffle(self):
        """
        カードをシャッフルする
        """
        random.shuffle(self.card_list)

    def draw(self) -> 'Card':
        """
        カードを引く. カードが残っていない場合にはFalseを返す
        
        Returns:
            Card or False: 引かれたカードの Card オブジェクト, もしくはFalse
        """
        if len(self.card_list) == 0:
            print("There are only 0 cards left in the deck.")
            return False
        else:
            draw_card = self.card_list.pop(0)
            return draw_card

    def search(self, suit: Suit = None, number: Number = None) -> List[Card]:
        """
        カードを検索する. suitやnumberに指定がある場合, 条件に一致するカードを返す
        
        Args:
            suit (Suit): 検索するカードの Suit オブジェクト
            number (Number): 検索するカードの Number オブジェクト
        
        Returns:
            list: 条件に一致するカードの Card オブジェクトのリスト
        """
        search_list = []

        if (suit is None) and (number is None):
            return search_list

        for card in self.card_list:
            if (suit is None or card.suit == suit) and (number is None or card.number == number):
                search_list.append(card)
        return search_list
