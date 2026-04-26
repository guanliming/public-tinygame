import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import random
import time
from enum import Enum
from typing import List, Optional, Tuple
from core.base_game import BaseGame


class CellState(Enum):
    """格子状态枚举"""
    FIXED = 0
    EMPTY = 1
    FILLED_CORRECT = 2
    FILLED_WRONG = 3


class SudokuGame(BaseGame):
    """数独游戏类"""

    GRID_SIZE = 9
    BOX_SIZE = 3
    INITIAL_REVEALED_COUNT = 35
    MAX_FAILURES = 8

    def __init__(self):
        super().__init__("数独")
        self.solution: List[List[int]] = []
        self.puzzle: List[List[int]] = []
        self.cell_states: List[List[CellState]] = []
        self.failure_count: int = 0
        self.start_time: Optional[float] = None
        self.elapsed_seconds: int = 0
        self.game_over: bool = False
        self.won: bool = False

    def init_game(self) -> None:
        """初始化游戏"""
        self.solution = self._generate_solution()
        self.puzzle = self._create_puzzle(self.solution)
        self.cell_states = [[CellState.FIXED if self.puzzle[i][j] != 0 else CellState.EMPTY 
                            for j in range(self.GRID_SIZE)] 
                            for i in range(self.GRID_SIZE)]
        self.failure_count = 0
        self.start_time = None
        self.elapsed_seconds = 0
        self.game_over = False
        self.won = False
        self.is_running = False

    def start(self) -> None:
        """开始游戏"""
        self.init_game()
        self.is_running = True
        self.start_time = time.time()

    def _generate_solution(self) -> List[List[int]]:
        """生成完整的数独解"""
        grid = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self._fill_grid(grid)
        return grid

    def _fill_grid(self, grid: List[List[int]]) -> bool:
        """使用回溯法填充数独网格"""
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                if grid[i][j] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for num in numbers:
                        if self._is_valid_placement(grid, i, j, num):
                            grid[i][j] = num
                            if self._fill_grid(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True

    def _is_valid_placement(self, grid: List[List[int]], row: int, col: int, num: int) -> bool:
        """检查数字放置是否有效"""
        for j in range(self.GRID_SIZE):
            if grid[row][j] == num:
                return False
        
        for i in range(self.GRID_SIZE):
            if grid[i][col] == num:
                return False
        
        box_row = (row // self.BOX_SIZE) * self.BOX_SIZE
        box_col = (col // self.BOX_SIZE) * self.BOX_SIZE
        for i in range(self.BOX_SIZE):
            for j in range(self.BOX_SIZE):
                if grid[box_row + i][box_col + j] == num:
                    return False
        
        return True

    def _create_puzzle(self, solution: List[List[int]]) -> List[List[int]]:
        """根据解决方案创建谜题，随机隐藏部分数字"""
        puzzle = [row.copy() for row in solution]
        
        cells_to_hide = self.GRID_SIZE * self.GRID_SIZE - self.INITIAL_REVEALED_COUNT
        positions = [(i, j) for i in range(self.GRID_SIZE) for j in range(self.GRID_SIZE)]
        random.shuffle(positions)
        
        for i, j in positions[:cells_to_hide]:
            puzzle[i][j] = 0
        
        return puzzle

    def make_move(self, row: int, col: int, num: int) -> bool:
        """
        在指定位置放置数字
        
        Args:
            row: 行号 (0-8)
            col: 列号 (0-8)
            num: 数字 (1-9)
        
        Returns:
            bool: True表示游戏继续，False表示游戏结束
        """
        if self.game_over or self.won:
            return False
        
        if not (0 <= row < self.GRID_SIZE and 0 <= col < self.GRID_SIZE):
            return True
        
        if self.cell_states[row][col] == CellState.FIXED:
            return True
        
        if self.puzzle[row][col] != 0 and self.cell_states[row][col] == CellState.FILLED_CORRECT:
            return True
        
        if num == self.solution[row][col]:
            self.puzzle[row][col] = num
            self.cell_states[row][col] = CellState.FILLED_CORRECT
            
            if self._check_win():
                self.won = True
                self.is_running = False
                return False
        else:
            self.failure_count += 1
            self.cell_states[row][col] = CellState.FILLED_WRONG
            
            if self.failure_count >= self.MAX_FAILURES:
                self.game_over = True
                self.is_running = False
                return False
        
        return True

    def clear_cell(self, row: int, col: int) -> bool:
        """
        清除指定位置的数字（只允许清除用户填写的数字）
        
        Args:
            row: 行号 (0-8)
            col: 列号 (0-8)
        
        Returns:
            bool: 是否成功清除
        """
        if self.game_over or self.won:
            return False
        
        if not (0 <= row < self.GRID_SIZE and 0 <= col < self.GRID_SIZE):
            return False
        
        state = self.cell_states[row][col]
        if state == CellState.FIXED:
            return False
        
        if state in (CellState.FILLED_CORRECT, CellState.FILLED_WRONG):
            self.puzzle[row][col] = 0
            self.cell_states[row][col] = CellState.EMPTY
            return True
        
        return False

    def _check_win(self) -> bool:
        """检查是否获胜（所有格子都填对）"""
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                if self.puzzle[i][j] == 0:
                    return False
        return True

    def is_valid_move(self, row: int, col: int) -> bool:
        """检查是否可以在指定位置填写数字"""
        if not (0 <= row < self.GRID_SIZE and 0 <= col < self.GRID_SIZE):
            return False
        return self.cell_states[row][col] != CellState.FIXED

    def update_time(self) -> int:
        """更新已用时间，返回秒数"""
        if self.start_time is None:
            return 0
        self.elapsed_seconds = int(time.time() - self.start_time)
        return self.elapsed_seconds

    def get_time_display(self) -> str:
        """获取时间显示字符串"""
        seconds = self.elapsed_seconds
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    def next_turn(self):
        """进入下一回合（数独游戏不需要）"""
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
        puzzle_state = []
        for i in range(self.GRID_SIZE):
            row = []
            for j in range(self.GRID_SIZE):
                cell_info = {
                    "row": i,
                    "col": j,
                    "value": self.puzzle[i][j],
                    "state": self.cell_states[i][j].name,
                    "solution": self.solution[i][j]
                }
                row.append(cell_info)
            puzzle_state.append(row)
        
        state.update({
            "grid_size": self.GRID_SIZE,
            "box_size": self.BOX_SIZE,
            "failure_count": self.failure_count,
            "max_failures": self.MAX_FAILURES,
            "elapsed_seconds": self.elapsed_seconds,
            "time_display": self.get_time_display(),
            "game_over": self.game_over,
            "won": self.won,
            "puzzle": puzzle_state
        })
        return state
