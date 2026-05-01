import sys
import io
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("=" * 50)
print("Testing game imports...")
print("=" * 50)

test_results = []

try:
    print("\n1. Testing HuarongdaoGameUI import...")
    from games.huarongdao import HuarongdaoGameUI
    print("   OK HuarongdaoGameUI imported successfully")
    print(f"   - Class: {HuarongdaoGameUI}")
    print(f"   - Has build: {hasattr(HuarongdaoGameUI, 'build')}")
    print(f"   - Has show: {hasattr(HuarongdaoGameUI, 'show')}")
    test_results.append(("HuarongdaoGameUI", True))
except Exception as e:
    print(f"   FAIL HuarongdaoGameUI import failed: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(("HuarongdaoGameUI", False))

try:
    print("\n2. Testing SudokuGameUI import...")
    from games.sudoku import SudokuGameUI
    print("   OK SudokuGameUI imported successfully")
    print(f"   - Class: {SudokuGameUI}")
    print(f"   - Has build: {hasattr(SudokuGameUI, 'build')}")
    print(f"   - Has show: {hasattr(SudokuGameUI, 'show')}")
    test_results.append(("SudokuGameUI", True))
except Exception as e:
    print(f"   FAIL SudokuGameUI import failed: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(("SudokuGameUI", False))

try:
    print("\n3. Testing TetrisGameUI import...")
    from games.tetris import TetrisGameUI
    print("   OK TetrisGameUI imported successfully")
    print(f"   - Class: {TetrisGameUI}")
    print(f"   - Has build: {hasattr(TetrisGameUI, 'build')}")
    print(f"   - Has show: {hasattr(TetrisGameUI, 'show')}")
    test_results.append(("TetrisGameUI", True))
except Exception as e:
    print(f"   FAIL TetrisGameUI import failed: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(("TetrisGameUI", False))

try:
    print("\n4. Testing TwentyOneGameUI import...")
    from games.twentyone import TwentyOneGameUI
    print("   OK TwentyOneGameUI imported successfully")
    print(f"   - Class: {TwentyOneGameUI}")
    print(f"   - Has build: {hasattr(TwentyOneGameUI, 'build')}")
    print(f"   - Has show: {hasattr(TwentyOneGameUI, 'show')}")
    test_results.append(("TwentyOneGameUI", True))
except Exception as e:
    print(f"   FAIL TwentyOneGameUI import failed: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(("TwentyOneGameUI", False))

try:
    print("\n5. Testing SnakeGameUI import...")
    from games.snake import SnakeGameUI
    print("   OK SnakeGameUI imported successfully")
    print(f"   - Class: {SnakeGameUI}")
    print(f"   - Has build: {hasattr(SnakeGameUI, 'build')}")
    print(f"   - Has show: {hasattr(SnakeGameUI, 'show')}")
    test_results.append(("SnakeGameUI", True))
except Exception as e:
    print(f"   FAIL SnakeGameUI import failed: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(("SnakeGameUI", False))

try:
    print("\n6. Testing DoudizhuGameUI import...")
    from games.doudizhu import DoudizhuGameUI
    print("   OK DoudizhuGameUI imported successfully")
    print(f"   - Class: {DoudizhuGameUI}")
    print(f"   - Has build: {hasattr(DoudizhuGameUI, 'build')}")
    print(f"   - Has show: {hasattr(DoudizhuGameUI, 'show')}")
    test_results.append(("DoudizhuGameUI", True))
except Exception as e:
    print(f"   FAIL DoudizhuGameUI import failed: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(("DoudizhuGameUI", False))

try:
    print("\n7. Testing MinesweeperGameUI import...")
    from games.minesweeper import MinesweeperGameUI
    print("   OK MinesweeperGameUI imported successfully")
    print(f"   - Class: {MinesweeperGameUI}")
    print(f"   - Has build: {hasattr(MinesweeperGameUI, 'build')}")
    print(f"   - Has show: {hasattr(MinesweeperGameUI, 'show')}")
    test_results.append(("MinesweeperGameUI", True))
except Exception as e:
    print(f"   FAIL MinesweeperGameUI import failed: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(("MinesweeperGameUI", False))

try:
    print("\n8. Testing WhackAMoleGameUI import...")
    from games.whackamole import WhackAMoleGameUI
    print("   OK WhackAMoleGameUI imported successfully")
    print(f"   - Class: {WhackAMoleGameUI}")
    print(f"   - Has build: {hasattr(WhackAMoleGameUI, 'build')}")
    print(f"   - Has show: {hasattr(WhackAMoleGameUI, 'show')}")
    test_results.append(("WhackAMoleGameUI", True))
except Exception as e:
    print(f"   FAIL WhackAMoleGameUI import failed: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(("WhackAMoleGameUI", False))

try:
    print("\n9. Testing GomokuGameUI import...")
    from games.gomoku import GomokuGameUI
    print("   OK GomokuGameUI imported successfully")
    print(f"   - Class: {GomokuGameUI}")
    print(f"   - Has build: {hasattr(GomokuGameUI, 'build')}")
    print(f"   - Has show: {hasattr(GomokuGameUI, 'show')}")
    test_results.append(("GomokuGameUI", True))
except Exception as e:
    print(f"   FAIL GomokuGameUI import failed: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(("GomokuGameUI", False))

try:
    print("\n10. Testing JunqiGameUI import...")
    from games.junqi import JunqiGameUI
    print("   OK JunqiGameUI imported successfully")
    print(f"   - Class: {JunqiGameUI}")
    print(f"   - Has build: {hasattr(JunqiGameUI, 'build')}")
    print(f"   - Has show: {hasattr(JunqiGameUI, 'show')}")
    test_results.append(("JunqiGameUI", True))
except Exception as e:
    print(f"   FAIL JunqiGameUI import failed: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(("JunqiGameUI", False))

try:
    print("\n11. Testing RacingGameUI import...")
    from games.racing import RacingGameUI
    print("   OK RacingGameUI imported successfully")
    print(f"   - Class: {RacingGameUI}")
    print(f"   - Has build: {hasattr(RacingGameUI, 'build')}")
    print(f"   - Has show: {hasattr(RacingGameUI, 'show')}")
    test_results.append(("RacingGameUI", True))
except Exception as e:
    print(f"   FAIL RacingGameUI import failed: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(("RacingGameUI", False))

print("\n" + "=" * 50)
print("Test Results Summary:")
print("=" * 50)
passed = sum(1 for _, result in test_results if result)
failed = len(test_results) - passed
print(f"Total: {len(test_results)} tests")
print(f"Passed: {passed}")
print(f"Failed: {failed}")

if failed > 0:
    print("\nFailed tests:")
    for name, result in test_results:
        if not result:
            print(f"  - {name}")
else:
    print("\nAll imports successful!")
