import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from enum import Enum
from core.base_player import BasePlayer


class PlayerRole(Enum):
    """玩家角色枚举"""
    FARMER = "农民"
    DIZHU = "地主"


class DoudizhuPlayer(BasePlayer):
    """斗地主玩家类"""

    def __init__(self, player_id: int, name: str):
        super().__init__(player_id, name)
        self.role: PlayerRole = PlayerRole.FARMER
        self.is_current: bool = False
        self.has_passed: bool = False

    def set_role(self, role: PlayerRole) -> None:
        """设置玩家角色"""
        self.role = role

    def __repr__(self) -> str:
        return f"DoudizhuPlayer(id={self.player_id}, name={self.name}, role={self.role.value}, hand_count={len(self.hand)})"
