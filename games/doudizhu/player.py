from enum import Enum
from typing import Optional
from public_tinygame.core.base_card import BaseCard


class Suit(Enum):
    """花色枚举"""
    SPADE = "♠"
    HEART = "♥"
    CLUB = "♣"
    DIAMOND = "♦"
    JOKER = "🃏"


class CardType(Enum):
    """牌型枚举"""
    INVALID = 0
    SINGLE = 1
    PAIR = 2
    TRIPLE = 3
    TRIPLE_ONE = 4
    TRIPLE_TWO = 5
    STRAIGHT = 6
    BOMB = 7
    ROCKET = 8
    PLANE = 9
    PLANE_SINGLE = 10
    PLANE_PAIR = 11


CARD_VALUES = {
    3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
    8: "8", 9: "9", 10: "10", 11: "J", 12: "Q",
    13: "K", 14: "A", 15: "2", 16: "小王", 17: "大王"
}


class DoudizhuCard(BaseCard):
    """斗地主卡牌类"""

    def __init__(self, value: int, suit: Optional[Suit] = None):
        super().__init__(value, suit)
        self._validate()

    def _validate(self) -> None:
        """验证卡牌有效性"""
        if not (3 <= self.value <= 17):
            raise ValueError(f"Card value must be between 3 and 17, got {self.value}")
        
        if self.value in (16, 17):
            if self.suit and self.suit != Suit.JOKER:
                raise ValueError(f"Joker must have Suit.JOKER, got {self.suit}")
            self.suit = Suit.JOKER
        else:
            if self.suit not in (Suit.SPADE, Suit.HEART, Suit.CLUB, Suit.DIAMOND):
                raise ValueError(f"Invalid suit {self.suit} for card value {self.value}")

    def get_weight(self) -> int:
        """获取卡牌权重（3-17）"""
        return self.value

    def is_joker(self) -> bool:
        """判断是否为大小王"""
        return self.value in (16, 17)

    def __repr__(self) -> str:
        name = CARD_VALUES.get(self.value, str(self.value))
        if self.is_joker():
            return f"[{name}]"
        return f"{self.suit.value}{name}"

    def __hash__(self) -> int:
        return hash((self.value, self.suit))


def create_deck() -> list[DoudizhuCard]:
    """创建一副完整的54张牌"""
    deck = []
    
    for value in range(3, 16):
        for suit in (Suit.SPADE, Suit.HEART, Suit.CLUB, Suit.DIAMOND):
            deck.append(DoudizhuCard(value, suit))
    
    deck.append(DoudizhuCard(16, Suit.JOKER))
    deck.append(DoudizhuCard(17, Suit.JOKER))
    
    return deck
