import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import random
import time
from enum import Enum
from typing import List, Optional, Tuple
from core.base_game import BaseGame


class CardState(Enum):
    """卡片状态枚举"""
    HIDDEN = 0
    REVEALED = 1
    MATCHED = 2


class FruitType(Enum):
    """水果类型枚举 - 15种水果"""
    APPLE = 1
    BANANA = 2
    ORANGE = 3
    GRAPE = 4
    STRAWBERRY = 5
    WATERMELON = 6
    PEACH = 7
    CHERRY = 8
    MANGO = 9
    PINEAPPLE = 10
    KIWI = 11
    LEMON = 12
    COCONUT = 13
    PEAR = 14
    PLUM = 15


class Card:
    """卡片类"""
    
    def __init__(self, fruit: FruitType, row: int, col: int):
        self.fruit = fruit
        self.row = row
        self.col = col
        self.state = CardState.HIDDEN
    
    def reveal(self) -> None:
        """翻开卡片"""
        if self.state == CardState.HIDDEN:
            self.state = CardState.REVEALED
    
    def hide(self) -> None:
        """隐藏卡片"""
        if self.state == CardState.REVEALED:
            self.state = CardState.HIDDEN
    
    def match(self) -> None:
        """匹配成功"""
        self.state = CardState.MATCHED
    
    def is_hidden(self) -> bool:
        return self.state == CardState.HIDDEN
    
    def is_revealed(self) -> bool:
        return self.state == CardState.REVEALED
    
    def is_matched(self) -> bool:
        return self.state == CardState.MATCHED


class LianliankanGame(BaseGame):
    """连连看游戏类"""
    
    ROWS = 4
    COLS = 4
    GAME_DURATION = 60
    TOTAL_CARDS = ROWS * COLS
    TOTAL_FRUITS = 15
    
    def __init__(self):
        super().__init__("连连看")
        self.board: List[List[Card]] = []
        self.revealed_cards: List[Card] = []
        self.matched_count: int = 0
        self.start_time: float = 0
        self.remaining_time: float = self.GAME_DURATION
        self.game_over: bool = False
        self.won: bool = False
        self.waiting_for_flip_back: bool = False
    
    def init_game(self) -> None:
        """初始化游戏"""
        self.board = []
        self.revealed_cards = []
        self.matched_count = 0
        self.start_time = 0
        self.remaining_time = self.GAME_DURATION
        self.game_over = False
        self.won = False
        self.waiting_for_flip_back = False
        self.is_running = False
        
        fruits = []
        for fruit in FruitType:
            fruits.append(fruit)
            fruits.append(fruit)
        
        random.shuffle(fruits)
        
        index = 0
        for row in range(self.ROWS):
            row_cards = []
            for col in range(self.COLS):
                card = Card(fruits[index], row, col)
                row_cards.append(card)
                index += 1
            self.board.append(row_cards)
    
    def start(self) -> None:
        """开始游戏"""
        self.init_game()
        self.is_running = True
        self.start_time = time.time()
    
    def update_time(self) -> float:
        """更新剩余时间"""
        if not self.start_time:
            return self.GAME_DURATION
        
        elapsed = time.time() - self.start_time
        self.remaining_time = max(0, self.GAME_DURATION - elapsed)
        
        if self.remaining_time <= 0 and not self.won:
            self.game_over = True
            self.is_running = False
        
        return self.remaining_time
    
    def get_remaining_time_display(self) -> str:
        """获取剩余时间显示字符串"""
        seconds = int(self.remaining_time)
        return f"{seconds}"
    
    def flip_card(self, row: int, col: int) -> Tuple[bool, Optional[Card], Optional[Card]]:
        """翻开卡片
        
        Returns:
            Tuple[bool, Optional[Card], Optional[Card]]: 
            - 第一个值：是否需要等待翻回（True表示需要）
            - 第二个值：第一张翻开的卡片（如果匹配成功或需要翻回）
            - 第三个值：第二张翻开的卡片（如果匹配成功或需要翻回）
        """
        if self.game_over or self.won or self.waiting_for_flip_back:
            return False, None, None
        
        if row < 0 or row >= self.ROWS or col < 0 or col >= self.COLS:
            return False, None, None
        
        card = self.board[row][col]
        
        if not card.is_hidden():
            return False, None, None
        
        card.reveal()
        self.revealed_cards.append(card)
        
        if len(self.revealed_cards) == 2:
            card1, card2 = self.revealed_cards
            
            if card1.fruit == card2.fruit:
                card1.match()
                card2.match()
                self.matched_count += 2
                self.revealed_cards = []
                
                if self.matched_count >= self.TOTAL_CARDS:
                    self.won = True
                    self.is_running = False
                
                return False, card1, card2
            else:
                self.waiting_for_flip_back = True
                return True, card1, card2
        
        return False, None, None
    
    def flip_back_cards(self) -> None:
        """翻回不匹配的卡片"""
        if len(self.revealed_cards) == 2:
            for card in self.revealed_cards:
                card.hide()
            self.revealed_cards = []
        self.waiting_for_flip_back = False
    
    def is_matched(self, row: int, col: int) -> bool:
        """检查卡片是否已匹配"""
        if row < 0 or row >= self.ROWS or col < 0 or col >= self.COLS:
            return False
        return self.board[row][col].is_matched()
    
    def is_revealed(self, row: int, col: int) -> bool:
        """检查卡片是否已翻开"""
        if row < 0 or row >= self.ROWS or col < 0 or col >= self.COLS:
            return False
        return self.board[row][col].is_revealed()
    
    def is_hidden(self, row: int, col: int) -> bool:
        """检查卡片是否隐藏"""
        if row < 0 or row >= self.ROWS or col < 0 or col >= self.COLS:
            return False
        return self.board[row][col].is_hidden()
    
    def get_fruit(self, row: int, col: int) -> Optional[FruitType]:
        """获取指定位置的水果类型"""
        if row < 0 or row >= self.ROWS or col < 0 or col >= self.COLS:
            return None
        return self.board[row][col].fruit
    
    def next_turn(self):
        """进入下一回合（连连看游戏不需要）"""
        pass
    
    def is_game_over(self) -> bool:
        """判断游戏是否结束"""
        return self.game_over or self.won
    
    def get_winner(self):
        """获取获胜者"""
        if self.won:
            return "You Win!"
        return None
    
    def get_state(self) -> dict:
        """获取游戏状态"""
        state = super().get_state()
        
        board_state = []
        for row in range(self.ROWS):
            row_data = []
            for col in range(self.COLS):
                card = self.board[row][col]
                cell_info = {
                    "row": row,
                    "col": col,
                    "fruit": card.fruit.name if card.is_revealed() or card.is_matched() else None,
                    "state": card.state.name,
                    "is_matched": card.is_matched(),
                    "is_revealed": card.is_revealed(),
                    "is_hidden": card.is_hidden()
                }
                row_data.append(cell_info)
            board_state.append(row_data)
        
        state.update({
            "rows": self.ROWS,
            "cols": self.COLS,
            "board": board_state,
            "matched_count": self.matched_count,
            "total_cards": self.TOTAL_CARDS,
            "remaining_time": self.remaining_time,
            "game_over": self.game_over,
            "won": self.won,
            "waiting_for_flip_back": self.waiting_for_flip_back
        })
        
        return state
