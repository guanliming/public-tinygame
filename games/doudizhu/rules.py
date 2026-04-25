import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from collections import Counter
from typing import Optional
from games.doudizhu.card import DoudizhuCard, CardType


def get_card_values(cards: list[DoudizhuCard]) -> list[int]:
    """获取卡牌的权重值列表"""
    return [card.get_weight() for card in cards]


def get_value_counts(cards: list[DoudizhuCard]) -> dict[int, int]:
    """统计每个值的出现次数"""
    values = get_card_values(cards)
    return dict(Counter(values))


def is_straight(values: list[int]) -> bool:
    """判断是否为顺子（连续5张或更多，不包含2和大小王）"""
    if len(values) < 5:
        return False
    
    sorted_vals = sorted(values)
    
    for v in sorted_vals:
        if v >= 15:
            return False
    
    for i in range(1, len(sorted_vals)):
        if sorted_vals[i] - sorted_vals[i-1] != 1:
            return False
    
    return True


def get_straight_max(values: list[int]) -> Optional[int]:
    """获取顺子的最大值"""
    if is_straight(values):
        return max(values)
    return None


def get_plane_sequences(triplet_values: list[int]) -> list[list[int]]:
    """从三张牌的数值中找出所有可能的飞机序列（至少连续2个）"""
    sorted_triplets = sorted(triplet_values)
    
    for v in sorted_triplets:
        if v >= 15:
            return []
    
    if len(sorted_triplets) < 2:
        return []
    
    sequences = []
    current_seq = [sorted_triplets[0]]
    
    for i in range(1, len(sorted_triplets)):
        if sorted_triplets[i] == sorted_triplets[i-1] + 1:
            current_seq.append(sorted_triplets[i])
        else:
            if len(current_seq) >= 2:
                sequences.append(current_seq)
            current_seq = [sorted_triplets[i]]
    
    if len(current_seq) >= 2:
        sequences.append(current_seq)
    
    return sequences


def get_card_type(cards: list[DoudizhuCard]) -> tuple[CardType, dict]:
    """
    识别牌型
    返回: (牌型枚举, 额外信息字典)
    额外信息包含:
    - 单张: {'value': 数值}
    - 对子: {'value': 数值}
    - 三张: {'value': 数值}
    - 三带一: {'triple': 三张数值, 'single': 带的单张}
    - 三带二: {'triple': 三张数值, 'pair': 带的对子}
    - 顺子: {'max': 最大值, 'length': 长度}
    - 炸弹: {'value': 数值}
    - 王炸: {}
    - 飞机不带: {'max': 最大值, 'length': 飞机长度}
    - 飞机带单: {'max': 最大值, 'length': 飞机长度}
    - 飞机带对: {'max': 最大值, 'length': 飞机长度}
    """
    if not cards:
        return (CardType.INVALID, {})
    
    n = len(cards)
    value_counts = get_value_counts(cards)
    values = list(value_counts.keys())
    counts = list(value_counts.values())
    
    if n == 2 and 16 in values and 17 in values:
        return (CardType.ROCKET, {})
    
    if n == 1:
        return (CardType.SINGLE, {'value': values[0]})
    
    if n == 2 and 2 in counts:
        return (CardType.PAIR, {'value': [k for k, v in value_counts.items() if v == 2][0]})
    
    if n == 4:
        if 4 in counts:
            return (CardType.BOMB, {'value': [k for k, v in value_counts.items() if v == 4][0]})
        if 3 in counts and 1 in counts:
            triple_val = [k for k, v in value_counts.items() if v == 3][0]
            single_val = [k for k, v in value_counts.items() if v == 1][0]
            return (CardType.TRIPLE_ONE, {'triple': triple_val, 'single': single_val})
    
    if n == 3 and 3 in counts:
        return (CardType.TRIPLE, {'value': [k for k, v in value_counts.items() if v == 3][0]})
    
    if n == 5:
        if 3 in counts and 2 in counts:
            triple_val = [k for k, v in value_counts.items() if v == 3][0]
            pair_val = [k for k, v in value_counts.items() if v == 2][0]
            return (CardType.TRIPLE_TWO, {'triple': triple_val, 'pair': pair_val})
        
        if n == 5 and all(c == 1 for c in counts):
            if is_straight(values):
                return (CardType.STRAIGHT, {'max': max(values), 'length': n})
    
    if n >= 5 and all(c == 1 for c in counts):
        if is_straight(values):
            return (CardType.STRAIGHT, {'max': max(values), 'length': n})
    
    triplet_values = [k for k, v in value_counts.items() if v == 3]
    if triplet_values:
        plane_seqs = get_plane_sequences(triplet_values)
        
        for seq in plane_seqs:
            seq_len = len(seq)
            expected_count = 3 * seq_len
            
            remaining_cards = n - expected_count
            
            if remaining_cards == 0:
                return (CardType.PLANE, {'max': max(seq), 'length': seq_len})
            
            if remaining_cards == seq_len:
                return (CardType.PLANE_SINGLE, {'max': max(seq), 'length': seq_len})
            
            if remaining_cards == seq_len * 2:
                remaining_counts = {k: v for k, v in value_counts.items() if k not in seq}
                if all(c % 2 == 0 for c in remaining_counts.values()):
                    return (CardType.PLANE_PAIR, {'max': max(seq), 'length': seq_len})
    
    return (CardType.INVALID, {})


def compare_cards(hand_a: list[DoudizhuCard], hand_b: list[DoudizhuCard]) -> bool:
    """
    判断 hand_a 是否能压过 hand_b
    返回 True 如果 hand_a 可以压过 hand_b，否则返回 False
    
    规则：
    1. 王炸可以压过所有牌型
    2. 炸弹可以压过除炸弹和王炸外的所有牌型
    3. 相同牌型才能比较（炸弹和王炸除外）
    4. 相同牌型时比较主牌的大小
    """
    if not hand_b:
        return bool(hand_a) and get_card_type(hand_a)[0] != CardType.INVALID
    
    type_a, info_a = get_card_type(hand_a)
    type_b, info_b = get_card_type(hand_b)
    
    if type_a == CardType.INVALID:
        return False
    
    if type_a == CardType.ROCKET:
        return True
    
    if type_b == CardType.ROCKET:
        return False
    
    if type_a == CardType.BOMB:
        if type_b == CardType.BOMB:
            return info_a['value'] > info_b['value']
        return True
    
    if type_b == CardType.BOMB:
        return False
    
    if type_a != type_b:
        return False
    
    if type_a == CardType.SINGLE:
        return info_a['value'] > info_b['value']
    
    if type_a == CardType.PAIR:
        return info_a['value'] > info_b['value']
    
    if type_a == CardType.TRIPLE:
        return info_a['value'] > info_b['value']
    
    if type_a in (CardType.TRIPLE_ONE, CardType.TRIPLE_TWO):
        return info_a['triple'] > info_b['triple']
    
    if type_a == CardType.STRAIGHT:
        if info_a['length'] != info_b['length']:
            return False
        return info_a['max'] > info_b['max']
    
    if type_a in (CardType.PLANE, CardType.PLANE_SINGLE, CardType.PLANE_PAIR):
        if info_a['length'] != info_b['length']:
            return False
        return info_a['max'] > info_b['max']
    
    return False
