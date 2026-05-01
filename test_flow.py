import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("Testing complete game flow...")
print("=" * 50)

import flet as ft
from games import HuarongdaoGameUI, SnakeGameUI, TetrisGameUI

class MockPage:
    def __init__(self):
        self.title = ""
        self.bgcolor = None
        self.width = 800
        self.height = 600
        self.controls = []
        self.on_keyboard_event = None
        self.window_width = 800
        self.window_height = 600
        self._page = self
        
    def clean(self):
        print("  [MockPage] clean() called")
        self.controls = []
        
    def add(self, control):
        print(f"  [MockPage] add() called with: {type(control).__name__}")
        self.controls.append(control)
        control._SetAttrInternal("_page", self)
        
    def update(self):
        print(f"  [MockPage] update() called")
        print(f"  [MockPage] Current controls: {[type(c).__name__ for c in self.controls]}")
        if self.controls:
            main_control = self.controls[0]
            if hasattr(main_control, 'controls'):
                for i, child in enumerate(main_control.controls):
                    if hasattr(child, 'visible'):
                        print(f"    - Child {i}: {type(child).__name__}, visible={child.visible}")

def test_game_ui(name, ui_class):
    print(f"\nTesting {name}...")
    
    mock_page = MockPage()
    
    print("  1. Creating UI instance...")
    ui = ui_class()
    print(f"     OK: {type(ui).__name__} created")
    
    print("  2. Calling build()...")
    content = ui.build(mock_page)
    print(f"     OK: build() returned {type(content).__name__}")
    
    print("  3. Calling page.add()...")
    mock_page.add(content)
    print("     OK: added to page")
    
    print("  4. Calling show()...")
    try:
        ui.show()
        print("     OK: show() completed")
    except Exception as e:
        print(f"     ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print(f"  5. Checking UI state...")
    if hasattr(ui, 'welcome_screen'):
        print(f"     welcome_screen.visible = {ui.welcome_screen.visible}")
    if hasattr(ui, 'game_screen'):
        print(f"     game_screen.visible = {ui.game_screen.visible}")
    if hasattr(ui, 'game_over_screen'):
        print(f"     game_over_screen.visible = {ui.game_over_screen.visible}")
    
    return True

print("\n" + "=" * 50)
all_passed = True

all_passed = test_game_ui("HuarongdaoGameUI", HuarongdaoGameUI) and all_passed
all_passed = test_game_ui("SnakeGameUI", SnakeGameUI) and all_passed
all_passed = test_game_ui("TetrisGameUI", TetrisGameUI) and all_passed

print("\n" + "=" * 50)
if all_passed:
    print("All tests passed!")
else:
    print("Some tests failed!")
print("=" * 50)
