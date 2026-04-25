import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import random
from typing import Optional
from core.base_game import BaseGame
from games.doudizhu.card import DoudizhuCard, create_deck
from games.doudizhu.player import DoudizhuPlayer, PlayerRole
from games.doudizhu.rules import get_card_type, compare_cards, CardType


class DoudizhuGame(BaseGame):
    """斗地主游戏类"""

    def __init__(self):
        super().__init__("斗地主")
        self.deck: list[DoudizhuCard] = []
        self.bottom_cards: list[DoudizhuCard] = []
        self.players: list[DoudizhuPlayer] = []
        self.current_player_index: int = 0
        self.last_played_cards: list[DoudizhuCard] = []
        self.last_played_player: Optional[DoudizhuPlayer] = None
        self.pass_count: int = 0

    def init_game(self) -> None:
        """初始化游戏：创建牌堆"""
        self.deck = create_deck()
        self.bottom_cards = []
        self.last_played_cards = []
        self.last_played_player = None
        self.pass_count = 0
        
        for player in self.players:
            player.clear_hand()
            player.role = PlayerRole.FARMER
            player.is_current = False
            player.has_passed = False
        
        self.is_running = False

    def shuffle(self) -> None:
        """洗牌"""
        random.shuffle(self.deck)

    def deal(self) -> None:
        """
        发牌：
        - 每人17张牌
        - 留3张底牌
        """
        if len(self.players) != 3:
            raise ValueError("斗地主需要3个玩家")
        
        if len(self.deck) != 54:
            raise ValueError("牌堆不完整")
        
        for i in range(17):
            for player in self.players:
                player.add_card(self.deck.pop())
        
        self.bottom_cards = self.deck.copy()
        
        for player in self.players:
            player.sort_hand(key_func=lambda c: -c.get_weight())

    def set_dizhu(self, player_index: int) -> None:
        """
        设置地主
        :param player_index: 玩家索引（0, 1, 2）
        """
        if not (0 <= player_index < 3):
            raise ValueError(f"无效的玩家索引: {player_index}")
        
        for i, player in enumerate(self.players):
            if i == player_index:
                player.role = PlayerRole.DIZHU
                player.add_cards(self.bottom_cards)
                player.sort_hand(key_func=lambda c: -c.get_weight())
            else:
                player.role = PlayerRole.FARMER
        
        self.current_player_index = player_index

    def start(self) -> None:
        """开始游戏"""
        if not self.players:
            self.players = [
                DoudizhuPlayer(0, "玩家1"),
                DoudizhuPlayer(1, "玩家2"),
                DoudizhuPlayer(2, "玩家3")
            ]
        
        self.init_game()
        self.shuffle()
        self.deal()
        self.is_running = True

    def next_turn(self) -> DoudizhuPlayer:
        """进入下一回合，返回当前玩家"""
        for player in self.players:
            player.is_current = False
        
        self.current_player_index = (self.current_player_index + 1) % 3
        current_player = self.players[self.current_player_index]
        current_player.is_current = True
        
        return current_player

    def get_current_player(self) -> DoudizhuPlayer:
        """获取当前玩家"""
        return self.players[self.current_player_index]

    def play_cards(self, player: DoudizhuPlayer, cards: list[DoudizhuCard]) -> tuple[bool, str]:
        """
        玩家出牌
        :param player: 出牌的玩家
        :param cards: 出的牌
        :return: (是否成功, 消息)
        """
        if player != self.get_current_player():
            return False, "不是当前玩家的回合"
        
        card_type, _ = get_card_type(cards)
        if card_type == CardType.INVALID:
            return False, "无效的牌型"
        
        if self.last_played_cards and self.last_played_player != player:
            if not compare_cards(cards, self.last_played_cards):
                return False, "出的牌打不过上家"
        
        for card in cards:
            if card not in player.hand:
                return False, f"手牌中没有 {card}"
        
        player.remove_cards(cards)
        
        self.last_played_cards = cards.copy()
        self.last_played_player = player
        self.pass_count = 0
        
        player.has_passed = False
        
        return True, f"出牌成功: {cards}"

    def pass_turn(self, player: DoudizhuPlayer) -> tuple[bool, str]:
        """
        玩家过牌
        :param player: 过牌的玩家
        :return: (是否成功, 消息)
        """
        if player != self.get_current_player():
            return False, "不是当前玩家的回合"
        
        if not self.last_played_cards:
            return False, "首家不能过牌"
        
        self.pass_count += 1
        player.has_passed = True
        
        if self.pass_count >= 2:
            self.last_played_cards = []
            self.last_played_player = None
            self.pass_count = 0
        
        return True, "过牌"

    def is_game_over(self) -> bool:
        """判断游戏是否结束"""
        for player in self.players:
            if player.get_hand_count() == 0:
                return True
        return False

    def get_winner(self) -> Optional[DoudizhuPlayer]:
        """获取获胜者"""
        for player in self.players:
            if player.get_hand_count() == 0:
                return player
        return None

    def get_state(self) -> dict:
        """获取游戏状态"""
        state = super().get_state()
        state.update({
            "current_player": self.players[self.current_player_index].name if self.players else None,
            "last_played_cards": [str(c) for c in self.last_played_cards],
            "bottom_cards": [str(c) for c in self.bottom_cards],
            "players": [
                {
                    "id": p.player_id,
                    "name": p.name,
                    "role": p.role.value,
                    "hand_count": p.get_hand_count(),
                    "is_current": p.is_current
                }
                for p in self.players
            ]
        })
        return state
