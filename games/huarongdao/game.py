import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import random
import time
from typing import List, Optional, Tuple, Set
from core.base_game import BaseGame


class HuarongdaoGame(BaseGame):
    """华容道数字拼图游戏类"""

    GRID_SIZE = 5
    TOTAL_CELLS = GRID_SIZE * GRID_SIZE
    NUM_COUNT = 23
    SHUFFLE_MOVES = 2000

    def __init__(self):
        super().__init__("华容道")
        self.board: List[List[int]] = []
        self.empty_positions: List[Tuple[int, int]] = []
        self.start_time: Optional[float] = None
        self.elapsed_seconds: int = 0
        self.game_over: bool = False
        self.won: bool = False
        self.move_count: int = 0

    def init_game(self) -> None:
        """初始化游戏"""
        self._create_solved_board()
        self.start_time = None
        self.elapsed_seconds = 0
        self.game_over = False
        self.won = False
        self.move_count = 0
        self.is_running = False

    def _create_solved_board(self) -> None:
        """创建已解决的棋盘"""
        self.board = []
        self.empty_positions = []
        num = 1
        for i in range(self.GRID_SIZE):
            row = []
            for j in range(self.GRID_SIZE):
                if num <= self.NUM_COUNT:
                    row.append(num)
                    num += 1
                else:
                    row.append(0)
                    self.empty_positions.append((i, j))
            self.board.append(row)

    def start(self) -> None:
        """开始游戏"""
        self.init_game()
        self._shuffle_board()
        self.is_running = True
        self.start_time = time.time()

    def _get_random_empty_pos(self) -> Tuple[int, int]:
        """随机获取一个空白格位置"""
        return random.choice(self.empty_positions)

    def _get_adjacent_empty_pos(self, row: int, col: int) -> Optional[Tuple[int, int]]:
        """获取与指定位置相邻的空白格位置"""
        for empty_row, empty_col in self.empty_positions:
            if (abs(row - empty_row) == 1 and col == empty_col) or \
               (abs(col - empty_col) == 1 and row == empty_row):
                return (empty_row, empty_col)
        return None

    def _shuffle_board(self) -> None:
        """打乱棋盘 - 通过随机移动确保可解"""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        last_empty_pos: Optional[Tuple[int, int]] = None
        
        for _ in range(self.SHUFFLE_MOVES):
            empty_pos = self._get_random_empty_pos()
            empty_row, empty_col = empty_pos
            
            valid_moves = []
            
            for dr, dc in directions:
                new_row, new_col = empty_row + dr, empty_col + dc
                
                if (new_row, new_col) == last_empty_pos:
                    continue
                
                if 0 <= new_row < self.GRID_SIZE and 0 <= new_col < self.GRID_SIZE:
                    if self.board[new_row][new_col] != 0:
                        valid_moves.append((dr, dc, new_row, new_col))
            
            if valid_moves:
                move = random.choice(valid_moves)
                dr, dc, new_row, new_col = move
                
                self.board[empty_row][empty_col] = self.board[new_row][new_col]
                self.board[new_row][new_col] = 0
                
                self.empty_positions.remove(empty_pos)
                self.empty_positions.append((new_row, new_col))
                last_empty_pos = empty_pos

    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """获取所有可移动的数字位置"""
        valid_moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for empty_row, empty_col in self.empty_positions:
            for dr, dc in directions:
                new_row, new_col = empty_row + dr, empty_col + dc
                if 0 <= new_row < self.GRID_SIZE and 0 <= new_col < self.GRID_SIZE:
                    if self.board[new_row][new_col] != 0:
                        valid_moves.append((new_row, new_col))
        
        return list(set(valid_moves))

    def can_move(self, row: int, col: int) -> bool:
        """检查指定位置的数字是否可以移动"""
        if not (0 <= row < self.GRID_SIZE and 0 <= col < self.GRID_SIZE):
            return False
        
        if self.board[row][col] == 0:
            return False
        
        return self._get_adjacent_empty_pos(row, col) is not None

    def move(self, row: int, col: int) -> bool:
        """
        移动指定位置的数字到相邻的空白格
        
        Args:
            row: 数字所在行
            col: 数字所在列
        
        Returns:
            bool: True 表示移动成功，False 表示无法移动
        """
        if self.game_over or self.won:
            return False
        
        if not self.can_move(row, col):
            return False
        
        empty_pos = self._get_adjacent_empty_pos(row, col)
        if empty_pos is None:
            return False
        
        empty_row, empty_col = empty_pos
        
        self.board[empty_row][empty_col] = self.board[row][col]
        self.board[row][col] = 0
        
        self.empty_positions.remove(empty_pos)
        self.empty_positions.append((row, col))
        
        self.move_count += 1
        
        if self._check_win():
            self.won = True
            self.is_running = False
        
        return True

    def _check_win(self) -> bool:
        """检查是否获胜"""
        expected = 1
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                if expected <= self.NUM_COUNT:
                    if self.board[i][j] != expected:
                        return False
                    expected += 1
                else:
                    if self.board[i][j] != 0:
                        return False
        return True

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
        """进入下一回合（华容道游戏不需要）"""
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
        state.update({
            "grid_size": self.GRID_SIZE,
            "board": self.board,
            "empty_positions": self.empty_positions,
            "move_count": self.move_count,
            "elapsed_seconds": self.elapsed_seconds,
            "time_display": self.get_time_display(),
            "game_over": self.game_over,
            "won": self.won
        })
        return state
