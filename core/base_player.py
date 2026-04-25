from abc import ABC
from typing import Any, List


class BasePlayer(ABC):
    """玩家基类"""

    def __init__(self, player_id: int, name: str):
        self.player_id = player_id
        self.name = name
        self.hand: List[Any] = []

    def add_card(self, card: Any) -> None:
        """添加一张牌到手牌"""
        self.hand.append(card)

    def add_cards(self, cards: List[Any]) -> None:
        """添加多张牌到手牌"""
        self.hand.extend(cards)

    def remove_cards(self, cards: List[Any]) -> None:
        """从手牌中移除指定的牌"""
        for card in cards:
            if card in self.hand:
                self.hand.remove(card)

    def get_hand_count(self) -> int:
        """获取手牌数量"""
        return len(self.hand)

    def clear_hand(self) -> None:
        """清空手牌"""
        self.hand = []

    def sort_hand(self, key_func=None) -> None:
        """对手牌排序"""
        if key_func:
            self.hand.sort(key=key_func)
        else:
            self.hand.sort()

    def __repr__(self) -> str:
        return f"Player(id={self.player_id}, name={self.name}, hand_count={len(self.hand)})"
