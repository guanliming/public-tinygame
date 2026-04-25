from public_tinygame.games.doudizhu import (
    create_deck, DoudizhuCard, Suit, CardType,
    get_card_type, compare_cards, DoudizhuGame
)


def test_deck_creation():
    print("=== 测试牌堆创建 ===")
    deck = create_deck()
    print(f"牌堆数量: {len(deck)} (应为 54)")
    print(f"前5张牌: {deck[:5]}")
    print(f"后5张牌: {deck[-5:]}")
    assert len(deck) == 54, "牌堆应该有54张牌"
    print("✓ 牌堆创建测试通过\n")


def test_shuffle_deal():
    print("=== 测试洗牌和发牌 ===")
    game = DoudizhuGame()
    game.start()
    
    print(f"底牌: {game.bottom_cards} (应为 3 张)")
    assert len(game.bottom_cards) == 3, "底牌应该有3张"
    
    for player in game.players:
        print(f"{player.name} 手牌数: {player.get_hand_count()} (应为 17 张)")
        print(f"  手牌: {player.hand}")
        assert player.get_hand_count() == 17, "每个玩家应该有17张牌"
    
    print("✓ 洗牌和发牌测试通过\n")


def test_card_type_recognition():
    print("=== 测试牌型识别 ===")
    
    single = [DoudizhuCard(3, Suit.SPADE)]
    card_type, info = get_card_type(single)
    print(f"单张 {single}: {card_type.name}, info={info}")
    assert card_type == CardType.SINGLE, "应该识别为单张"
    
    pair = [DoudizhuCard(3, Suit.SPADE), DoudizhuCard(3, Suit.HEART)]
    card_type, info = get_card_type(pair)
    print(f"对子 {pair}: {card_type.name}, info={info}")
    assert card_type == CardType.PAIR, "应该识别为对子"
    
    triple = [DoudizhuCard(5, Suit.SPADE), DoudizhuCard(5, Suit.HEART), DoudizhuCard(5, Suit.CLUB)]
    card_type, info = get_card_type(triple)
    print(f"三张 {triple}: {card_type.name}, info={info}")
    assert card_type == CardType.TRIPLE, "应该识别为三张"
    
    triple_one = triple + [DoudizhuCard(3, Suit.SPADE)]
    card_type, info = get_card_type(triple_one)
    print(f"三带一 {triple_one}: {card_type.name}, info={info}")
    assert card_type == CardType.TRIPLE_ONE, "应该识别为三带一"
    
    triple_two = triple + [DoudizhuCard(3, Suit.SPADE), DoudizhuCard(3, Suit.HEART)]
    card_type, info = get_card_type(triple_two)
    print(f"三带二 {triple_two}: {card_type.name}, info={info}")
    assert card_type == CardType.TRIPLE_TWO, "应该识别为三带二"
    
    straight = [
        DoudizhuCard(3, Suit.SPADE), DoudizhuCard(4, Suit.HEART),
        DoudizhuCard(5, Suit.CLUB), DoudizhuCard(6, Suit.DIAMOND),
        DoudizhuCard(7, Suit.SPADE)
    ]
    card_type, info = get_card_type(straight)
    print(f"顺子 {straight}: {card_type.name}, info={info}")
    assert card_type == CardType.STRAIGHT, "应该识别为顺子"
    
    bomb = [
        DoudizhuCard(8, Suit.SPADE), DoudizhuCard(8, Suit.HEART),
        DoudizhuCard(8, Suit.CLUB), DoudizhuCard(8, Suit.DIAMOND)
    ]
    card_type, info = get_card_type(bomb)
    print(f"炸弹 {bomb}: {card_type.name}, info={info}")
    assert card_type == CardType.BOMB, "应该识别为炸弹"
    
    rocket = [DoudizhuCard(16), DoudizhuCard(17)]
    card_type, info = get_card_type(rocket)
    print(f"王炸 {rocket}: {card_type.name}, info={info}")
    assert card_type == CardType.ROCKET, "应该识别为王炸"
    
    plane = [
        DoudizhuCard(3, Suit.SPADE), DoudizhuCard(3, Suit.HEART), DoudizhuCard(3, Suit.CLUB),
        DoudizhuCard(4, Suit.SPADE), DoudizhuCard(4, Suit.HEART), DoudizhuCard(4, Suit.CLUB)
    ]
    card_type, info = get_card_type(plane)
    print(f"飞机不带 {plane}: {card_type.name}, info={info}")
    assert card_type == CardType.PLANE, "应该识别为飞机不带"
    
    plane_single = plane + [DoudizhuCard(5, Suit.SPADE), DoudizhuCard(6, Suit.HEART)]
    card_type, info = get_card_type(plane_single)
    print(f"飞机带单 {plane_single}: {card_type.name}, info={info}")
    assert card_type == CardType.PLANE_SINGLE, "应该识别为飞机带单"
    
    plane_pair = plane + [
        DoudizhuCard(5, Suit.SPADE), DoudizhuCard(5, Suit.HEART),
        DoudizhuCard(6, Suit.SPADE), DoudizhuCard(6, Suit.HEART)
    ]
    card_type, info = get_card_type(plane_pair)
    print(f"飞机带对 {plane_pair}: {card_type.name}, info={info}")
    assert card_type == CardType.PLANE_PAIR, "应该识别为飞机带对"
    
    print("✓ 牌型识别测试通过\n")


def test_compare_cards():
    print("=== 测试牌比较 ===")
    
    single3 = [DoudizhuCard(3, Suit.SPADE)]
    single4 = [DoudizhuCard(4, Suit.HEART)]
    print(f"单张4 能否压过 单张3: {compare_cards(single4, single3)} (应为 True)")
    assert compare_cards(single4, single3) == True
    print(f"单张3 能否压过 单张4: {compare_cards(single3, single4)} (应为 False)")
    assert compare_cards(single3, single4) == False
    
    pair3 = [DoudizhuCard(3, Suit.SPADE), DoudizhuCard(3, Suit.HEART)]
    pair4 = [DoudizhuCard(4, Suit.SPADE), DoudizhuCard(4, Suit.HEART)]
    print(f"对子4 能否压过 对子3: {compare_cards(pair4, pair3)} (应为 True)")
    assert compare_cards(pair4, pair3) == True
    
    triple3 = [DoudizhuCard(3, Suit.SPADE), DoudizhuCard(3, Suit.HEART), DoudizhuCard(3, Suit.CLUB)]
    triple5 = [DoudizhuCard(5, Suit.SPADE), DoudizhuCard(5, Suit.HEART), DoudizhuCard(5, Suit.CLUB)]
    print(f"三张5 能否压过 三张3: {compare_cards(triple5, triple3)} (应为 True)")
    assert compare_cards(triple5, triple3) == True
    
    triple_one3 = triple3 + [DoudizhuCard(10, Suit.SPADE)]
    triple_one5 = triple5 + [DoudizhuCard(3, Suit.HEART)]
    print(f"三带一5 能否压过 三带一3: {compare_cards(triple_one5, triple_one3)} (应为 True)")
    assert compare_cards(triple_one5, triple_one3) == True
    
    straight3_7 = [
        DoudizhuCard(3, Suit.SPADE), DoudizhuCard(4, Suit.HEART),
        DoudizhuCard(5, Suit.CLUB), DoudizhuCard(6, Suit.DIAMOND),
        DoudizhuCard(7, Suit.SPADE)
    ]
    straight4_8 = [
        DoudizhuCard(4, Suit.SPADE), DoudizhuCard(5, Suit.HEART),
        DoudizhuCard(6, Suit.CLUB), DoudizhuCard(7, Suit.DIAMOND),
        DoudizhuCard(8, Suit.SPADE)
    ]
    print(f"顺子4-8 能否压过 顺子3-7: {compare_cards(straight4_8, straight3_7)} (应为 True)")
    assert compare_cards(straight4_8, straight3_7) == True
    
    bomb8 = [
        DoudizhuCard(8, Suit.SPADE), DoudizhuCard(8, Suit.HEART),
        DoudizhuCard(8, Suit.CLUB), DoudizhuCard(8, Suit.DIAMOND)
    ]
    bomb9 = [
        DoudizhuCard(9, Suit.SPADE), DoudizhuCard(9, Suit.HEART),
        DoudizhuCard(9, Suit.CLUB), DoudizhuCard(9, Suit.DIAMOND)
    ]
    print(f"炸弹8 能否压过 对子3: {compare_cards(bomb8, pair3)} (应为 True)")
    assert compare_cards(bomb8, pair3) == True
    print(f"炸弹9 能否压过 炸弹8: {compare_cards(bomb9, bomb8)} (应为 True)")
    assert compare_cards(bomb9, bomb8) == True
    
    rocket = [DoudizhuCard(16), DoudizhuCard(17)]
    print(f"王炸 能否压过 炸弹9: {compare_cards(rocket, bomb9)} (应为 True)")
    assert compare_cards(rocket, bomb9) == True
    
    print(f"对子3 能否压过 单张3: {compare_cards(pair3, single3)} (应为 False，牌型不同)")
    assert compare_cards(pair3, single3) == False
    
    print("✓ 牌比较测试通过\n")


def test_game_flow():
    print("=== 测试游戏流程 ===")
    
    game = DoudizhuGame()
    game.start()
    
    print(f"游戏状态: {game.get_state()}")
    
    game.set_dizhu(0)
    print(f"\n设置玩家0为地主后:")
    print(f"地主(玩家0)手牌数: {game.players[0].get_hand_count()} (应为 20 张)")
    assert game.players[0].get_hand_count() == 20
    
    print(f"农民(玩家1)手牌数: {game.players[1].get_hand_count()} (应为 17 张)")
    assert game.players[1].get_hand_count() == 17
    print(f"农民(玩家2)手牌数: {game.players[2].get_hand_count()} (应为 17 张)")
    assert game.players[2].get_hand_count() == 17
    
    current_player = game.get_current_player()
    print(f"\n当前玩家: {current_player.name}")
    
    print("✓ 游戏流程测试通过\n")


def main():
    print("=" * 50)
    print("斗地主游戏框架测试")
    print("=" * 50 + "\n")
    
    test_deck_creation()
    test_shuffle_deal()
    test_card_type_recognition()
    test_compare_cards()
    test_game_flow()
    
    print("=" * 50)
    print("所有测试通过!")
    print("=" * 50)


if __name__ == "__main__":
    main()
