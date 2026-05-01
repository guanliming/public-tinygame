import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from games.lianliankan import LianliankanGame, CardState, FruitType


def test_game_initialization():
    """测试游戏初始化"""
    print("测试游戏初始化...")
    game = LianliankanGame()
    game.init_game()
    
    assert game.ROWS == 5
    assert game.COLS == 6
    assert game.TOTAL_CARDS == 30
    assert game.matched_count == 0
    assert game.game_over == False
    assert game.won == False
    
    print(f"  棋盘大小: {game.ROWS} 行 × {game.COLS} 列 = {game.TOTAL_CARDS} 张卡片")
    print("  ✓ 游戏初始化成功")


def test_fruit_distribution():
    """测试水果分布"""
    print("\n测试水果分布...")
    game = LianliankanGame()
    game.init_game()
    
    fruit_count = {}
    for row in range(game.ROWS):
        for col in range(game.COLS):
            fruit = game.get_fruit(row, col)
            if fruit not in fruit_count:
                fruit_count[fruit] = 0
            fruit_count[fruit] += 1
    
    print(f"  水果种类数: {len(fruit_count)}")
    assert len(fruit_count) == 15
    
    for fruit, count in fruit_count.items():
        print(f"    {fruit.name}: {count} 张")
        assert count == 2
    
    print("  ✓ 每种水果恰好 2 张")


def test_card_flip():
    """测试卡片翻开"""
    print("\n测试卡片翻开...")
    game = LianliankanGame()
    game.init_game()
    
    assert game.is_hidden(0, 0) == True
    assert game.is_revealed(0, 0) == False
    
    need_flip_back, card1, card2 = game.flip_card(0, 0)
    
    assert game.is_revealed(0, 0) == True
    assert need_flip_back == False
    assert card1 is None
    assert card2 is None
    
    print("  ✓ 单张卡片翻开成功")


def test_card_match():
    """测试卡片匹配"""
    print("\n测试卡片匹配...")
    game = LianliankanGame()
    game.init_game()
    
    fruit_positions = {}
    for row in range(game.ROWS):
        for col in range(game.COLS):
            fruit = game.get_fruit(row, col)
            if fruit not in fruit_positions:
                fruit_positions[fruit] = []
            fruit_positions[fruit].append((row, col))
    
    test_fruit = list(fruit_positions.keys())[0]
    (r1, c1), (r2, c2) = fruit_positions[test_fruit]
    
    print(f"  测试水果: {test_fruit.name}")
    print(f"  位置: ({r1},{c1}) 和 ({r2},{c2})")
    
    game.flip_card(r1, c1)
    need_flip_back, card1, card2 = game.flip_card(r2, c2)
    
    assert need_flip_back == False
    assert card1 is not None
    assert card2 is not None
    assert game.is_matched(r1, c1) == True
    assert game.is_matched(r2, c2) == True
    assert game.matched_count == 2
    
    print(f"  ✓ 匹配成功，已匹配数: {game.matched_count}")


def test_card_no_match():
    """测试卡片不匹配"""
    print("\n测试卡片不匹配...")
    game = LianliankanGame()
    game.init_game()
    
    fruit_positions = {}
    for row in range(game.ROWS):
        for col in range(game.COLS):
            fruit = game.get_fruit(row, col)
            if fruit not in fruit_positions:
                fruit_positions[fruit] = []
            fruit_positions[fruit].append((row, col))
    
    fruits = list(fruit_positions.keys())
    fruit1 = fruits[0]
    fruit2 = fruits[1]
    
    (r1, c1) = fruit_positions[fruit1][0]
    (r2, c2) = fruit_positions[fruit2][0]
    
    print(f"  测试不同水果: {fruit1.name} 和 {fruit2.name}")
    print(f"  位置: ({r1},{c1}) 和 ({r2},{c2})")
    
    game.flip_card(r1, c1)
    need_flip_back, card1, card2 = game.flip_card(r2, c2)
    
    assert need_flip_back == True
    assert card1 is not None
    assert card2 is not None
    assert game.is_revealed(r1, c1) == True
    assert game.is_revealed(r2, c2) == True
    assert game.waiting_for_flip_back == True
    
    print("  ✓ 不匹配，需要翻回")
    
    game.flip_back_cards()
    
    assert game.is_hidden(r1, c1) == True
    assert game.is_hidden(r2, c2) == True
    assert game.waiting_for_flip_back == False
    
    print("  ✓ 卡片已翻回隐藏状态")


def test_win_condition():
    """测试胜利条件"""
    print("\n测试胜利条件...")
    game = LianliankanGame()
    game.init_game()
    
    fruit_positions = {}
    for row in range(game.ROWS):
        for col in range(game.COLS):
            fruit = game.get_fruit(row, col)
            if fruit not in fruit_positions:
                fruit_positions[fruit] = []
            fruit_positions[fruit].append((row, col))
    
    for fruit, positions in fruit_positions.items():
        (r1, c1), (r2, c2) = positions
        game.flip_card(r1, c1)
        game.flip_card(r2, c2)
    
    assert game.matched_count == 30
    assert game.won == True
    assert game.is_game_over() == True
    
    print(f"  ✓ 全部匹配完成，已匹配数: {game.matched_count}")
    print("  ✓ 游戏胜利")


def test_timer():
    """测试计时器"""
    print("\n测试计时器...")
    game = LianliankanGame()
    game.init_game()
    game.start()
    
    import time
    time.sleep(0.5)
    
    remaining = game.update_time()
    
    assert remaining > 0
    assert remaining < 30
    
    print(f"  剩余时间: {remaining:.1f} 秒")
    print("  ✓ 计时器正常工作")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("连连看游戏核心逻辑测试")
    print("=" * 60)
    
    test_game_initialization()
    test_fruit_distribution()
    test_card_flip()
    test_card_match()
    test_card_no_match()
    test_win_condition()
    test_timer()
    
    print("\n" + "=" * 60)
    print("✓ 所有测试通过！")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
