from abc import ABC
from typing import Any


class BaseCard(ABC):
    """卡牌基类"""

    def __init__(self, value: int, suit: Any = None):
        self.value = value
        self.suit = suit

    def get_weight(self) -> int:
        """获取卡牌的权重值"""
        return self.value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BaseCard):
            return False
        return self.value == other.value and self.suit == other.suit

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, BaseCard):
            return NotImplemented
        return self.get_weight() < other.get_weight()

    def __repr__(self) -> str:
        raise NotImplementedError("Subclasses must implement __repr__")
