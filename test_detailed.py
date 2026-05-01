import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("Detailed Test for Game Collection")
print("=" * 60)

print("\n1. Testing imports...")
try:
    import flet as ft
    print(f"   - flet: OK (version {ft.__version__})")
except Exception as e:
    print(f"   - flet: FAILED - {e}")
    sys.exit(1)

print("\n2. Testing GameSelector class...")
try:
    from app import GameSelector
    print("   - GameSelector: OK")
    
    selector = GameSelector()
    print("   - GameSelector instance: OK")
    
    print("\n3. Testing _build_selector_ui...")
    selector_ui = selector._build_selector_ui()
    print(f"   - _build_selector_ui returned: {type(selector_ui).__name__}")
    
    if hasattr(selector_ui, 'content'):
        content = selector_ui.content
        print(f"   - Content type: {type(content).__name__}")
        if hasattr(content, 'controls'):
            controls = content.controls
            print(f"   - Number of controls: {len(controls)}")
            for i, ctrl in enumerate(controls):
                print(f"     - Control {i}: {type(ctrl).__name__}")
    
except Exception as e:
    print(f"   - GameSelector: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n4. Testing all game UI classes...")

from games import (
    HuarongdaoGameUI,
    SudokuGameUI,
    TetrisGameUI,
    TwentyOneGameUI,
    SnakeGameUI,
    DoudizhuGameUI,
    MinesweeperGameUI,
    WhackAMoleGameUI,
    GomokuGameUI,
    JunqiGameUI,
    RacingGameUI
)

game_uies = [
    ("HuarongdaoGameUI", HuarongdaoGameUI),
    ("SudokuGameUI", SudokuGameUI),
    ("TetrisGameUI", TetrisGameUI),
    ("TwentyOneGameUI", TwentyOneGameUI),
    ("SnakeGameUI", SnakeGameUI),
    ("DoudizhuGameUI", DoudizhuGameUI),
    ("MinesweeperGameUI", MinesweeperGameUI),
    ("WhackAMoleGameUI", WhackAMoleGameUI),
    ("GomokuGameUI", GomokuGameUI),
    ("JunqiGameUI", JunqiGameUI),
    ("RacingGameUI", RacingGameUI),
]

all_passed = True
for name, ui_class in game_uies:
    print(f"\n   Testing {name}...")
    try:
        ui = ui_class()
        print(f"     - Instance created: OK")
        
        has_build = hasattr(ui, 'build') and callable(ui.build)
        has_show = hasattr(ui, 'show') and callable(ui.show)
        
        print(f"     - Has build(): {has_build}")
        print(f"     - Has show(): {has_show}")
        
        if not has_build or not has_show:
            all_passed = False
            print(f"     - ERROR: Missing required methods!")
            
    except Exception as e:
        all_passed = False
        print(f"     - ERROR: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 60)
if all_passed:
    print("All tests passed!")
else:
    print("Some tests failed!")
print("=" * 60)
