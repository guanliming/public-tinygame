import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from games.huarongdao.game import HuarongdaoGame

__all__ = [
    'HuarongdaoGame'
]
