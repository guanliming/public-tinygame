import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import random
from enum import Enum
from typing import List, Set, Tuple
from core.base_game import BaseGame


class CellState(Enum):
    """格子状态枚举"""
    HIDDEN = 0
    REVEALED = 1
    QUESTIONED = 2


class MinesweeperGame(BaseGame):
    """扫雷游戏类"""

    GRID_WIDTH = 50
    GRID_HEIGHT = 50
    MINE_COUNT = 250

    def __init__(self):
        super().__init__("扫雷")
        self.grid: List[List[bool]] = []
        self.cell_states: List[List[CellState]] = []
        self.revealed_count: int = 0
        self.total_cells: int = self.GRID_WIDTH * self.GRID_HEIGHT
        self.game_over: bool = False
        self.won: bool = False
        self.first_click: bool = True

    def init_game(self) -> None:
        """初始化游戏"""
        self.grid = [[False for _ in range(self.GRID_HEIGHT)] for _ in range(self.GRID_WIDTH)]
        self.cell_states = [[CellState.HIDDEN for _ in range(self.GRID_HEIGHT)] for _ in range(self.GRID_WIDTH)]
        self.revealed_count = 0
        self.game_over = False
        self.won = False
        self.first_click = True
        self.is_running = False

    def _place_mines(self, exclude_x: int, exclude_y: int) -> None:
        """放置地雷，排除第一次点击的位置及其周围"""
        exclude_positions: Set[Tuple[int, int]] = set()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx = exclude_x + dx
                ny = exclude_y + dy
                if 0 <= nx < self.GRID_WIDTH and 0 <= ny < self.GRID_HEIGHT:
                    exclude_positions.add((nx, ny))

        available_positions: List[Tuple[int, int]] = []
        for x in range(self.GRID_WIDTH):
            for y in range(self.GRID_HEIGHT):
                if (x, y) not in exclude_positions:
                    available_positions.append((x, y))

        mines_to_place = min(self.MINE_COUNT, len(available_positions))
        mine_positions = random.sample(available_positions, mines_to_place)

        for x, y in mine_positions:
            self.grid[x][y] = True

    def start(self) -> None:
        """开始游戏"""
        self.init_game()
        self.is_running = True

    def get_adjacent_mine_count(self, x: int, y: int) -> int:
        """获取指定格子周围的地雷数量"""
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = x + dx
                ny = y + dy
                if 0 <= nx < self.GRID_WIDTH and 0 <= ny < self.GRID_HEIGHT:
                    if self.grid[nx][ny]:
                        count += 1
        return count

    def _reveal_cell(self, x: int, y: int) -> None:
        """递归翻开格子"""
        if x < 0 or x >= self.GRID_WIDTH or y < 0 or y >= self.GRID_HEIGHT:
            return
        if self.cell_states[x][y] != CellState.HIDDEN:
            return

        self.cell_states[x][y] = CellState.REVEALED
        self.revealed_count += 1

        mine_count = self.get_adjacent_mine_count(x, y)
        if mine_count == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    self._reveal_cell(x + dx, y + dy)

    def left_click(self, x: int, y: int) -> bool:
        """左击翻开格子
        
        Returns:
            bool: True表示游戏继续，False表示游戏结束
        """
        if self.game_over or self.won:
            return False

        if x < 0 or x >= self.GRID_WIDTH or y < 0 or y >= self.GRID_HEIGHT:
            return True

        if self.first_click:
            self.first_click = False
            self._place_mines(x, y)

        if self.cell_states[x][y] == CellState.REVEALED:
            return True

        if self.grid[x][y]:
            self.game_over = True
            self.is_running = False
            return False

        self._reveal_cell(x, y)

        if self.revealed_count >= self.total_cells - self.MINE_COUNT:
            self.won = True
            self.is_running = False
            return False

        return True

    def right_click(self, x: int, y: int) -> None:
        """右击标记/取消标记问号"""
        if self.game_over or self.won:
            return

        if x < 0 or x >= self.GRID_WIDTH or y < 0 or y >= self.GRID_HEIGHT:
            return

        if self.cell_states[x][y] == CellState.HIDDEN:
            self.cell_states[x][y] = CellState.QUESTIONED
        elif self.cell_states[x][y] == CellState.QUESTIONED:
            self.cell_states[x][y] = CellState.HIDDEN

    def next_turn(self):
        """进入下一回合（扫雷游戏不需要）"""
        pass

    def is_game_over(self) -> bool:
        """判断游戏是否结束"""
        return self.game_over or self.won

    def get_winner(self):
        """获取获胜者"""
        if self.won:
            return "You Win!"
        return None

    def get_state(self) -> dict:
        """获取游戏状态"""
        state = super().get_state()
        grid_state = []
        for x in range(self.GRID_WIDTH):
            row = []
            for y in range(self.GRID_HEIGHT):
                cell_info = {
                    "x": x,
                    "y": y,
                    "state": self.cell_states[x][y].name,
                    "is_mine": self.grid[x][y] if self.game_over or self.won else False
                }
                if self.cell_states[x][y] == CellState.REVEALED:
                    cell_info["adjacent_mines"] = self.get_adjacent_mine_count(x, y)
                row.append(cell_info)
            grid_state.append(row)

        state.update({
            "grid_width": self.GRID_WIDTH,
            "grid_height": self.GRID_HEIGHT,
            "mine_count": self.MINE_COUNT,
            "revealed_count": self.revealed_count,
            "game_over": self.game_over,
            "won": self.won,
            "first_click": self.first_click,
            "grid": grid_state
        })
        return state
