from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseGame(ABC):
    """游戏基类，所有游戏都需要继承这个类"""

    def __init__(self, game_name: str):
        self.game_name = game_name
        self.players: List[Any] = []
        self.is_running = False

    @abstractmethod
    def init_game(self) -> None:
        """初始化游戏"""
        pass

    @abstractmethod
    def start(self) -> None:
        """开始游戏"""
        pass

    @abstractmethod
    def next_turn(self) -> Any:
        """进入下一回合，返回当前玩家"""
        pass

    @abstractmethod
    def is_game_over(self) -> bool:
        """判断游戏是否结束"""
        pass

    @abstractmethod
    def get_winner(self) -> Any:
        """获取获胜者"""
        pass

    def add_player(self, player: Any) -> None:
        """添加玩家"""
        self.players.append(player)

    def get_state(self) -> Dict[str, Any]:
        """获取游戏状态"""
        return {
            "game_name": self.game_name,
            "players_count": len(self.players),
            "is_running": self.is_running
        }
