import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from games.whackamole.game import WhackAMoleGame, HoleState

__all__ = [
    'WhackAMoleGame', 'HoleState'
]
