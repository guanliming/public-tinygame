import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from games.snake.game import SnakeGame, Direction, Position

__all__ = [
    'SnakeGame', 'Direction', 'Position'
]
