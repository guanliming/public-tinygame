import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import random
from typing import List, Optional, Tuple
from enum import Enum
from core.base_game import BaseGame


class PlayerColor(Enum):
    """玩家颜色枚举"""
    BLACK = 1
    WHITE = 2


class Position:
    """位置类"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Position({self.x}, {self.y})"


class Move:
    """走棋类"""

    def __init__(self, position: Position, color: PlayerColor):
        self.position = position
        self.color = color


class GomokuGame(BaseGame):
    """五子棋游戏类"""

    BOARD_SIZE = 100
    WIN_COUNT = 5

    def __init__(self):
        super().__init__("五子棋")
        self.board: List[List[Optional[PlayerColor]]] = []
        self.current_player: PlayerColor = PlayerColor.BLACK
        self.game_over: bool = False
        self.winner: Optional[PlayerColor] = None
        self.moves: List[Move] = []

    def init_game(self) -> None:
        """初始化游戏"""
        self.board = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.current_player = PlayerColor.BLACK
        self.game_over = False
        self.winner = None
        self.moves = []
        self.is_running = False

    def start(self) -> None:
        """开始游戏"""
        self.init_game()
        self.is_running = True

    def is_valid_move(self, x: int, y: int) -> bool:
        """检查是否是有效走棋"""
        if x < 0 or x >= self.BOARD_SIZE or y < 0 or y >= self.BOARD_SIZE:
            return False
        return self.board[y][x] is None

    def make_move(self, x: int, y: int) -> bool:
        """走棋"""
        if not self.is_valid_move(x, y):
            return False

        self.board[y][x] = self.current_player
        self.moves.append(Move(Position(x, y), self.current_player))

        if self._check_win(x, y, self.current_player):
            self.game_over = True
            self.winner = self.current_player
            self.is_running = False
            return True

        self.current_player = PlayerColor.WHITE if self.current_player == PlayerColor.BLACK else PlayerColor.BLACK
        return True

    def _check_win(self, x: int, y: int, color: PlayerColor) -> bool:
        """检查是否获胜（精确5颗棋子成线）"""
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1)
        ]

        for dx, dy in directions:
            count = 1
            
            i = 1
            while True:
                nx, ny = x + i * dx, y + i * dy
                if 0 <= nx < self.BOARD_SIZE and 0 <= ny < self.BOARD_SIZE and self.board[ny][nx] == color:
                    count += 1
                    i += 1
                else:
                    break
            
            i = 1
            while True:
                nx, ny = x - i * dx, y - i * dy
                if 0 <= nx < self.BOARD_SIZE and 0 <= ny < self.BOARD_SIZE and self.board[ny][nx] == color:
                    count += 1
                    i += 1
                else:
                    break

            if count == self.WIN_COUNT:
                return True

        return False

    def _evaluate_position(self, x: int, y: int, color: PlayerColor) -> int:
        """评估位置分数"""
        if not self.is_valid_move(x, y):
            return 0

        score = 0
        opponent_color = PlayerColor.WHITE if color == PlayerColor.BLACK else PlayerColor.BLACK

        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1)
        ]

        for dx, dy in directions:
            my_count = 1
            my_blocked = 0
            my_space = 0

            i = 1
            while True:
                nx, ny = x + i * dx, y + i * dy
                if 0 <= nx < self.BOARD_SIZE and 0 <= ny < self.BOARD_SIZE:
                    if self.board[ny][nx] == color:
                        my_count += 1
                    elif self.board[ny][nx] is None:
                        my_space += 1
                        break
                    else:
                        my_blocked += 1
                        break
                else:
                    my_blocked += 1
                    break
                i += 1

            i = 1
            while True:
                nx, ny = x - i * dx, y - i * dy
                if 0 <= nx < self.BOARD_SIZE and 0 <= ny < self.BOARD_SIZE:
                    if self.board[ny][nx] == color:
                        my_count += 1
                    elif self.board[ny][nx] is None:
                        my_space += 1
                        break
                    else:
                        my_blocked += 1
                        break
                else:
                    my_blocked += 1
                    break
                i += 1

            if my_count >= 5:
                score += 100000
            elif my_count == 4:
                if my_blocked == 0:
                    score += 10000
                elif my_blocked == 1:
                    score += 1000
            elif my_count == 3:
                if my_blocked == 0:
                    score += 1000
                elif my_blocked == 1:
                    score += 100
            elif my_count == 2:
                if my_blocked == 0:
                    score += 100
                elif my_blocked == 1:
                    score += 10

        for dx, dy in directions:
            opp_count = 1
            opp_blocked = 0

            i = 1
            while True:
                nx, ny = x + i * dx, y + i * dy
                if 0 <= nx < self.BOARD_SIZE and 0 <= ny < self.BOARD_SIZE:
                    if self.board[ny][nx] == opponent_color:
                        opp_count += 1
                    elif self.board[ny][nx] is None:
                        break
                    else:
                        opp_blocked += 1
                        break
                else:
                    opp_blocked += 1
                    break
                i += 1

            i = 1
            while True:
                nx, ny = x - i * dx, y - i * dy
                if 0 <= nx < self.BOARD_SIZE and 0 <= ny < self.BOARD_SIZE:
                    if self.board[ny][nx] == opponent_color:
                        opp_count += 1
                    elif self.board[ny][nx] is None:
                        break
                    else:
                        opp_blocked += 1
                        break
                else:
                    opp_blocked += 1
                    break
                i += 1

            if opp_count >= 5:
                score += 80000
            elif opp_count == 4:
                if opp_blocked == 0:
                    score += 8000
                elif opp_blocked == 1:
                    score += 800
            elif opp_count == 3:
                if opp_blocked == 0:
                    score += 800
                elif opp_blocked == 1:
                    score += 80
            elif opp_count == 2:
                if opp_blocked == 0:
                    score += 80
                elif opp_blocked == 1:
                    score += 8

        center_x = self.BOARD_SIZE // 2
        center_y = self.BOARD_SIZE // 2
        distance = abs(x - center_x) + abs(y - center_y)
        score += max(0, 20 - distance // 5)

        return score

    def get_ai_move(self) -> Optional[Tuple[int, int]]:
        """获取AI走棋"""
        if self.game_over:
            return None

        best_score = -1
        best_moves = []

        search_radius = 2
        occupied_positions = set()

        for move in self.moves:
            for dx in range(-search_radius, search_radius + 1):
                for dy in range(-search_radius, search_radius + 1):
                    x = move.position.x + dx
                    y = move.position.y + dy
                    if 0 <= x < self.BOARD_SIZE and 0 <= y < self.BOARD_SIZE:
                        occupied_positions.add((x, y))

        if not self.moves:
            center = self.BOARD_SIZE // 2
            return (center, center)

        for x, y in occupied_positions:
            if self.is_valid_move(x, y):
                score = self._evaluate_position(x, y, self.current_player)
                if score > best_score:
                    best_score = score
                    best_moves = [(x, y)]
                elif score == best_score:
                    best_moves.append((x, y))

        if best_moves:
            return random.choice(best_moves)

        return None

    def next_turn(self):
        """进入下一回合，返回当前玩家"""
        return self.current_player

    def is_game_over(self) -> bool:
        """判断游戏是否结束"""
        return self.game_over

    def get_winner(self):
        """获取获胜者"""
        return self.winner

    def get_state(self) -> dict:
        """获取游戏状态"""
        state = super().get_state()
        state.update({
            "board_size": self.BOARD_SIZE,
            "current_player": self.current_player.name if self.current_player else None,
            "game_over": self.game_over,
            "winner": self.winner.name if self.winner else None,
            "moves_count": len(self.moves)
        })
        return state
