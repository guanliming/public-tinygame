import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from games.gomoku.game import GomokuGame, PlayerColor, Position, Move

__all__ = [
    'GomokuGame', 'PlayerColor', 'Position', 'Move'
]
