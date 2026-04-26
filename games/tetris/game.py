import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import random
from enum import Enum
from typing import List, Tuple, Optional
from core.base_game import BaseGame


class TetrominoShape(Enum):
    """方块形状枚举"""
    I = "I"
    L = "L"
    T = "T"
    O = "O"
    S = "S"
    Z = "Z"
    J = "J"


class Tetromino:
    """俄罗斯方块形状类"""
    
    SHAPES = {
        TetrominoShape.I: [
            [(0, 0), (0, 1), (0, 2), (0, 3)],
            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(0, 0), (0, 1), (0, 2), (0, 3)],
            [(0, 1), (1, 1), (2, 1), (3, 1)]
        ],
        TetrominoShape.L: [
            [(0, 0), (0, 1), (0, 2), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (2, 0)],
            [(0, 0), (1, 0), (1, 1), (1, 2)],
            [(0, 1), (0, 2), (1, 1), (2, 1)]
        ],
        TetrominoShape.J: [
            [(1, 0), (1, 1), (1, 2), (0, 2)],
            [(0, 0), (0, 1), (1, 1), (2, 1)],
            [(0, 0), (1, 0), (0, 1), (0, 2)],
            [(0, 1), (1, 1), (2, 1), (2, 2)]
        ],
        TetrominoShape.T: [
            [(0, 1), (1, 0), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (1, 2), (2, 1)],
            [(1, 0), (1, 1), (1, 2), (0, 1)],
            [(0, 1), (1, 0), (1, 1), (2, 1)]
        ],
        TetrominoShape.O: [
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)]
        ],
        TetrominoShape.S: [
            [(0, 1), (0, 2), (1, 0), (1, 1)],
            [(0, 1), (1, 1), (1, 2), (2, 2)],
            [(0, 1), (0, 2), (1, 0), (1, 1)],
            [(0, 1), (1, 1), (1, 2), (2, 2)]
        ],
        TetrominoShape.Z: [
            [(0, 0), (0, 1), (1, 1), (1, 2)],
            [(0, 2), (1, 1), (1, 2), (2, 1)],
            [(0, 0), (0, 1), (1, 1), (1, 2)],
            [(0, 2), (1, 1), (1, 2), (2, 1)]
        ]
    }
    
    COLORS = {
        TetrominoShape.I: 0x00FFFF,
        TetrominoShape.L: 0xFFA500,
        TetrominoShape.J: 0x0000FF,
        TetrominoShape.T: 0x800080,
        TetrominoShape.O: 0xFFFF00,
        TetrominoShape.S: 0x00FF00,
        TetrominoShape.Z: 0xFF0000
    }
    
    def __init__(self, shape: TetrominoShape = None):
        if shape is None:
            shape = random.choice(list(TetrominoShape))
        self.shape = shape
        self.rotation = 0
        self.x = 0
        self.y = 0
    
    @property
    def color(self) -> int:
        return self.COLORS[self.shape]
    
    @property
    def blocks(self) -> List[Tuple[int, int]]:
        """获取当前旋转状态下的所有方块坐标（相对位置）"""
        return self.SHAPES[self.shape][self.rotation % 4]
    
    @property
    def absolute_blocks(self) -> List[Tuple[int, int]]:
        """获取当前位置下的所有方块绝对坐标"""
        return [(self.x + dx, self.y + dy) for dx, dy in self.blocks]
    
    def rotate(self) -> None:
        """顺时针旋转90度"""
        self.rotation = (self.rotation + 1) % 4
    
    def rotate_back(self) -> None:
        """逆时针旋转90度（用于回退无效旋转）"""
        self.rotation = (self.rotation - 1) % 4
    
    def get_rotated_blocks(self) -> List[Tuple[int, int]]:
        """获取旋转后的方块坐标（不实际改变旋转状态）"""
        new_rotation = (self.rotation + 1) % 4
        return [(self.x + dx, self.y + dy) for dx, dy in self.SHAPES[self.shape][new_rotation]]


class TetrisGame(BaseGame):
    """俄罗斯方块游戏类"""
    
    GRID_WIDTH = 10
    GRID_HEIGHT = 20
    WIN_SCORE = 20
    FALL_SPEED = 0.5
    FAST_FALL_SPEED = 0.1
    
    def __init__(self):
        super().__init__("俄罗斯方块")
        self.grid: List[List[Optional[int]]] = []
        self.current_piece: Optional[Tetromino] = None
        self.next_piece: Optional[Tetromino] = None
        self.score: int = 0
        self.game_over: bool = False
        self.won: bool = False
        self.is_paused: bool = False
        self.fast_fall: bool = False
    
    def init_game(self) -> None:
        """初始化游戏"""
        self.grid = [[None for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        self.current_piece = None
        self.next_piece = Tetromino()
        self.score = 0
        self.game_over = False
        self.won = False
        self.is_paused = False
        self.fast_fall = False
        self.is_running = False
        
        self._spawn_piece()
    
    def _spawn_piece(self) -> None:
        """生成新方块"""
        if self.next_piece is None:
            self.next_piece = Tetromino()
        
        self.current_piece = self.next_piece
        self.current_piece.x = self.GRID_WIDTH // 2 - 2
        self.current_piece.y = 0
        
        self.next_piece = Tetromino()
        
        if self._check_collision(self.current_piece.absolute_blocks):
            self.game_over = True
            self.is_running = False
    
    def _check_collision(self, blocks: List[Tuple[int, int]]) -> bool:
        """检查方块是否碰撞
        
        Args:
            blocks: 要检查的方块坐标列表
            
        Returns:
            True 如果发生碰撞，False 否则
        """
        for x, y in blocks:
            if x < 0 or x >= self.GRID_WIDTH:
                return True
            if y >= self.GRID_HEIGHT:
                return True
            if y >= 0 and self.grid[y][x] is not None:
                return True
        return False
    
    def move_left(self) -> bool:
        """向左移动方块
        
        Returns:
            True 如果移动成功，False 否则
        """
        if not self.current_piece or self.is_paused:
            return False
        
        test_blocks = [(x - 1, y) for x, y in self.current_piece.absolute_blocks]
        if not self._check_collision(test_blocks):
            self.current_piece.x -= 1
            return True
        return False
    
    def move_right(self) -> bool:
        """向右移动方块
        
        Returns:
            True 如果移动成功，False 否则
        """
        if not self.current_piece or self.is_paused:
            return False
        
        test_blocks = [(x + 1, y) for x, y in self.current_piece.absolute_blocks]
        if not self._check_collision(test_blocks):
            self.current_piece.x += 1
            return True
        return False
    
    def move_down(self) -> bool:
        """向下移动方块
        
        Returns:
            True 如果移动成功，False 否则（表示方块已经着陆）
        """
        if not self.current_piece or self.is_paused:
            return False
        
        test_blocks = [(x, y + 1) for x, y in self.current_piece.absolute_blocks]
        if not self._check_collision(test_blocks):
            self.current_piece.y += 1
            return True
        else:
            self._lock_piece()
            return False
    
    def rotate(self) -> bool:
        """旋转方块
        
        Returns:
            True 如果旋转成功，False 否则
        """
        if not self.current_piece or self.is_paused:
            return False
        
        if self.current_piece.shape == TetrominoShape.O:
            return False
        
        rotated_blocks = self.current_piece.get_rotated_blocks()
        
        wall_kicks = [
            [(0, 0)],
            [(-1, 0), (1, 0)],
            [(-2, 0), (2, 0)],
            [(0, -1), (0, 1)]
        ]
        
        for kicks in wall_kicks:
            for kick_x, kick_y in kicks:
                kicked_blocks = [(x + kick_x, y + kick_y) for x, y in rotated_blocks]
                if not self._check_collision(kicked_blocks):
                    self.current_piece.rotate()
                    self.current_piece.x += kick_x
                    self.current_piece.y += kick_y
                    return True
        
        return False
    
    def _lock_piece(self) -> None:
        """将当前方块固定到格子上"""
        if not self.current_piece:
            return
        
        for x, y in self.current_piece.absolute_blocks:
            if y >= 0:
                self.grid[y][x] = self.current_piece.color
        
        self._clear_lines()
        self._spawn_piece()
    
    def _clear_lines(self) -> None:
        """检查并清除填满的行"""
        lines_to_clear = []
        
        for y in range(self.GRID_HEIGHT):
            if all(self.grid[y][x] is not None for x in range(self.GRID_WIDTH)):
                lines_to_clear.append(y)
        
        if lines_to_clear:
            for y in lines_to_clear:
                self.score += 1
            
            if self.score >= self.WIN_SCORE:
                self.won = True
                self.is_running = False
            
            for line in lines_to_clear:
                self.grid.pop(line)
                self.grid.insert(0, [None for _ in range(self.GRID_WIDTH)])
    
    def toggle_pause(self) -> None:
        """切换暂停状态"""
        if not self.game_over and not self.won:
            self.is_paused = not self.is_paused
    
    def start(self) -> None:
        """开始游戏"""
        self.init_game()
        self.is_running = True
    
    def next_turn(self):
        """进入下一回合（俄罗斯方块游戏不需要）"""
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
        for y in range(self.GRID_HEIGHT):
            row = []
            for x in range(self.GRID_WIDTH):
                row.append({
                    "x": x,
                    "y": y,
                    "color": self.grid[y][x]
                })
            grid_state.append(row)
        
        current_piece_state = None
        if self.current_piece:
            current_piece_state = {
                "shape": self.current_piece.shape.value,
                "blocks": self.current_piece.absolute_blocks,
                "color": self.current_piece.color
            }
        
        next_piece_state = None
        if self.next_piece:
            next_piece_state = {
                "shape": self.next_piece.shape.value,
                "blocks": self.next_piece.blocks,
                "color": self.next_piece.color
            }
        
        state.update({
            "grid_width": self.GRID_WIDTH,
            "grid_height": self.GRID_HEIGHT,
            "score": self.score,
            "win_score": self.WIN_SCORE,
            "game_over": self.game_over,
            "won": self.won,
            "is_paused": self.is_paused,
            "grid": grid_state,
            "current_piece": current_piece_state,
            "next_piece": next_piece_state
        })
        return state
