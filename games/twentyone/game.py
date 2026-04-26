import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import random
from typing import List, Optional, Tuple
from itertools import permutations
from core.base_game import BaseGame


class TwentyOneGame(BaseGame):
    """21点游戏类"""

    def __init__(self):
        super().__init__("21点")
        self.numbers: List[int] = []
        self.solution: Optional[str] = None
        self.has_solution: bool = False

    def init_game(self) -> None:
        """初始化游戏"""
        self.is_running = False
        self.numbers = []
        self.solution = None
        self.has_solution = False

    def start(self) -> None:
        """开始游戏"""
        self.init_game()
        self.is_running = True
        self.next_question()

    def next_question(self) -> None:
        """生成下一题"""
        while True:
            self.numbers = [random.randint(1, 13) for _ in range(4)]
            self.solution = self._find_solution(self.numbers)
            if self.solution:
                self.has_solution = True
                break

    def _find_solution(self, numbers: List[int]) -> Optional[str]:
        """
        查找21点的解法
        使用递归方式尝试所有可能的运算组合
        """
        if len(numbers) == 1:
            if abs(numbers[0] - 21) < 1e-6:
                return str(numbers[0])
            return None

        for i in range(len(numbers)):
            for j in range(len(numbers)):
                if i == j:
                    continue

                remaining = [numbers[k] for k in range(len(numbers)) if k != i and k != j]
                
                a, b = numbers[i], numbers[j]
                
                ops = [
                    ('+', a + b),
                    ('-', a - b),
                    ('-', b - a),
                    ('*', a * b),
                ]
                
                if b != 0 and a % b == 0:
                    ops.append(('/', a // b))
                if a != 0 and b % a == 0:
                    ops.append(('/', b // a))

                for op_symbol, result in ops:
                    new_numbers = remaining + [result]
                    sub_solution = self._find_solution(new_numbers)
                    
                    if sub_solution:
                        result_str = str(result)
                        if result_str in sub_solution:
                            if op_symbol == '+' or op_symbol == '*':
                                expr = f"({a} {op_symbol} {b})"
                            elif op_symbol == '-':
                                if result == a - b:
                                    expr = f"({a} - {b})"
                                else:
                                    expr = f"({b} - {a})"
                            elif op_symbol == '/':
                                if result == a // b:
                                    expr = f"({a} / {b})"
                                else:
                                    expr = f"({b} / {a})"
                            else:
                                expr = f"({a} {op_symbol} {b})"
                            
                            solution = sub_solution.replace(result_str, expr, 1)
                            return solution
        
        return None

    def get_solution_expression(self) -> Optional[str]:
        """获取解法表达式"""
        return self.solution

    def next_turn(self):
        """进入下一回合（不需要）"""
        pass

    def is_game_over(self) -> bool:
        """判断游戏是否结束"""
        return False

    def get_winner(self):
        """获取获胜者"""
        return None

    def get_state(self) -> dict:
        """获取游戏状态"""
        state = super().get_state()
        state.update({
            "numbers": self.numbers,
            "has_solution": self.has_solution,
            "solution": self.solution
        })
        return state
