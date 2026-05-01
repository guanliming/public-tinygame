import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import traceback

GAMES = [
    ("Huarongdao", "games.huarongdao.ui", "HuarongdaoGameUI"),
    ("Tetris", "games.tetris.ui", "TetrisGameUI"),
    ("Snake", "games.snake.ui", "SnakeGameUI"),
    ("Minesweeper", "games.minesweeper.ui", "MinesweeperGameUI"),
    ("WhackAMole", "games.whackamole.ui", "WhackAMoleGameUI"),
    ("Sudoku", "games.sudoku.ui", "SudokuGameUI"),
    ("TwentyOne", "games.twentyone.ui", "TwentyOneGameUI"),
    ("Racing", "games.racing.ui", "RacingGameUI"),
    ("Junqi", "games.junqi.ui", "JunqiGameUI"),
    ("Gomoku", "games.gomoku.ui", "GomokuGameUI"),
]

def test_game_imports():
    print("=" * 60)
    print("Testing Game Imports")
    print("=" * 60)
    
    all_passed = True
    
    for game_name, module_name, class_name in GAMES:
        print(f"\n[TEST] {game_name}")
        try:
            module = __import__(module_name, fromlist=[class_name])
            ui_class = getattr(module, class_name)
            print(f"  [OK] Imported {class_name} from {module_name}")
            
            print(f"  [INFO] Checking attributes and methods...")
            instance = ui_class(on_exit=lambda: None)
            
            attrs = ['welcome_screen', 'game_screen', 'game_over_screen', 'show', '_show_welcome_screen', '_build_ui']
            for attr in attrs:
                if hasattr(instance, attr):
                    print(f"    [OK] Has {attr}")
                else:
                    print(f"    [WARN] Missing {attr}")
            
        except Exception as e:
            print(f"  [FAIL] {e}")
            traceback.print_exc()
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("All imports passed!")
    else:
        print("Some imports failed!")
    print("=" * 60)

def test_game_classes():
    print("\n" + "=" * 60)
    print("Testing Game Logic Classes")
    print("=" * 60)
    
    game_logic_classes = [
        ("Huarongdao", "games.huarongdao.game", "HuarongdaoGame"),
        ("Tetris", "games.tetris.game", "TetrisGame"),
        ("Snake", "games.snake.game", "SnakeGame"),
        ("Minesweeper", "games.minesweeper.game", "MinesweeperGame"),
        ("WhackAMole", "games.whackamole.game", "WhackAMoleGame"),
        ("Sudoku", "games.sudoku.game", "SudokuGame"),
        ("TwentyOne", "games.twentyone.game", "TwentyOneGame"),
        ("Racing", "games.racing.game", "RacingGame"),
        ("Junqi", "games.junqi.game", "JunqiGame"),
        ("Gomoku", "games.gomoku.game", "GomokuGame"),
    ]
    
    for game_name, module_name, class_name in game_logic_classes:
        print(f"\n[TEST] {game_name} - {class_name}")
        try:
            module = __import__(module_name, fromlist=[class_name])
            game_class = getattr(module, class_name)
            print(f"  [OK] Imported {class_name}")
            
            print(f"  [INFO] Checking attributes...")
            instance = game_class()
            
            print(f"    [INFO] Instance created: {type(instance)}")
            print(f"    [INFO] Attributes: {[a for a in dir(instance) if not a.startswith('_')]}")
            
        except Exception as e:
            print(f"  [FAIL] {e}")
            traceback.print_exc()

if __name__ == "__main__":
    test_game_imports()
    test_game_classes()
