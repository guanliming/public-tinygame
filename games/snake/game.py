import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import random
from typing import List, Optional
from enum import Enum
from core.base_game import BaseGame


class Direction(Enum):
    """方向枚举"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


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


class SnakeGame(BaseGame):
    """贪吃蛇游戏类"""

    GRID_WIDTH = 70
    GRID_HEIGHT = 50
    INITIAL_FOOD_COUNT = 30
    WIN_SCORE = 50
    MOVE_SPEED = 0.15

    def __init__(self):
        super().__init__("贪吃蛇")
        self.snake: List[Position] = []
        self.direction: Direction = Direction.RIGHT
        self.next_direction: Direction = Direction.RIGHT
        self.foods: set[Position] = set()
        self.score: int = 0
        self.game_over: bool = False
        self.won: bool = False

    def init_game(self) -> None:
        """初始化游戏"""
        self.snake = [Position(self.GRID_WIDTH // 2, self.GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.foods = set()
        self.score = 0
        self.game_over = False
        self.won = False
        self.is_running = False
        
        self._generate_initial_foods()

    def _generate_initial_foods(self) -> None:
        """生成初始食物"""
        for _ in range(self.INITIAL_FOOD_COUNT):
            self._generate_food()

    def _generate_food(self) -> None:
        """生成一个食物，确保不会出现在蛇身上"""
        available_positions = []
        for x in range(self.GRID_WIDTH):
            for y in range(self.GRID_HEIGHT):
                pos = Position(x, y)
                if pos not in self.snake and pos not in self.foods:
                    available_positions.append(pos)
        
        if available_positions:
            food = random.choice(available_positions)
            self.foods.add(food)

    def start(self) -> None:
        """开始游戏"""
        self.init_game()
        self.is_running = True

    def set_direction(self, new_direction: Direction) -> None:
        """设置蛇的移动方向，防止反向移动"""
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        
        if new_direction != opposite_directions.get(self.direction):
            self.next_direction = new_direction

    def move(self) -> bool:
        """移动蛇"""
        self.direction = self.next_direction
        
        head = self.snake[0]
        dx, dy = self.direction.value
        
        new_head_x = (head.x + dx) % self.GRID_WIDTH
        new_head_y = (head.y + dy) % self.GRID_HEIGHT
        
        new_head = Position(new_head_x, new_head_y)
        
        if new_head in self.snake[1:]:
            self.game_over = True
            self.is_running = False
            return False
        
        self.snake.insert(0, new_head)
        
        if new_head in self.foods:
            self.foods.remove(new_head)
            self.score += 1
            self._generate_food()
            
            if self.score >= self.WIN_SCORE:
                self.won = True
                self.is_running = False
                return False
        else:
            self.snake.pop()
        
        return True

    def next_turn(self):
        """进入下一回合，返回当前玩家（贪吃蛇游戏不需要）"""
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
            "snake": [{"x": p.x, "y": p.y} for p in self.snake],
            "foods": [{"x": f.x, "y": f.y} for f in self.foods],
            "score": self.score,
            "direction": self.direction.name,
            "game_over": self.game_over,
            "won": self.won,
            "grid_width": self.GRID_WIDTH,
            "grid_height": self.GRID_HEIGHT
        })
        return state
