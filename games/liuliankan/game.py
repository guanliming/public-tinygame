import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import random
import time
from enum import Enum
from typing import List, Optional, Tuple
from core.base_game import BaseGame


class CardState(Enum):
    HIDDEN = 0
    FLIPPED = 1
    MATCHED = 2


class FruitType(Enum):
    APPLE = 0
    BANANA = 1
    ORANGE = 2
    GRAPE = 3
    STRAWBERRY = 4
    WATERMELON = 5
    PEACH = 6
    CHERRY = 7
    PINEAPPLE = 8
    MANGO = 9
    KIWI = 10
    COCONUT = 11
    LEMON = 12
    PEAR = 13
    BLUEBERRY = 14


FRUIT_EMOJIS = {
    FruitType.APPLE: "🍎",
    FruitType.BANANA: "🍌",
    FruitType.ORANGE: "🍊",
    FruitType.GRAPE: "🍇",
    FruitType.STRAWBERRY: "🍓",
    FruitType.WATERMELON: "🍉",
    FruitType.PEACH: "🍑",
    FruitType.CHERRY: "🍒",
    FruitType.PINEAPPLE: "🍍",
    FruitType.MANGO: "🥭",
    FruitType.KIWI: "🥝",
    FruitType.COCONUT: "🥥",
    FruitType.LEMON: "🍋",
    FruitType.PEAR: "🍐",
    FruitType.BLUEBERRY: "🫐",
}

BACK_EMOJI = "🐌"


class Card:
    def __init__(self, fruit_type: FruitType, row: int, col: int):
        self.fruit_type = fruit_type
        self.row = row
        self.col = col
        self.state = CardState.HIDDEN
    
    def get_emoji(self) -> str:
        if self.state == CardState.HIDDEN:
            return BACK_EMOJI
        return FRUIT_EMOJIS.get(self.fruit_type, "❓")
    
    def flip(self):
        if self.state == CardState.HIDDEN:
            self.state = CardState.FLIPPED
    
    def hide(self):
        if self.state == CardState.FLIPPED:
            self.state = CardState.HIDDEN
    
    def match(self):
        if self.state == CardState.FLIPPED:
            self.state = CardState.MATCHED


class LiuliankanGame(BaseGame):
    ROWS = 5
    COLS = 6
    TOTAL_CARDS = ROWS * COLS
    GAME_DURATION = 30
    MATCH_DELAY = 1.0
    
    def __init__(self):
        super().__init__("连连看")
        self.board: List[List[Card]] = []
        self.flipped_cards: List[Card] = []
        self.matched_pairs: int = 0
        self.total_pairs: int = self.TOTAL_CARDS // 2
        self.start_time: float = 0
        self.remaining_time: float = self.GAME_DURATION
        self.game_over: bool = False
        self.won: bool = False
        self.last_flip_time: float = 0
        self.waiting_for_hide: bool = False
    
    def init_game(self) -> None:
        fruit_types = list(FruitType)
        cards = []
        
        for i in range(self.total_pairs):
            fruit = fruit_types[i % len(fruit_types)]
            cards.append(fruit)
            cards.append(fruit)
        
        random.shuffle(cards)
        
        self.board = []
        card_index = 0
        for row in range(self.ROWS):
            row_cards = []
            for col in range(self.COLS):
                card = Card(cards[card_index], row, col)
                row_cards.append(card)
                card_index += 1
            self.board.append(row_cards)
        
        self.flipped_cards = []
        self.matched_pairs = 0
        self.start_time = 0
        self.remaining_time = self.GAME_DURATION
        self.game_over = False
        self.won = False
        self.last_flip_time = 0
        self.waiting_for_hide = False
        self.is_running = False
    
    def start(self) -> None:
        self.init_game()
        self.is_running = True
        self.start_time = time.time()
    
    def flip_card(self, row: int, col: int) -> Tuple[bool, Optional[List[Card]]]:
        if self.game_over or self.won:
            return False, None
        
        if row < 0 or row >= self.ROWS or col < 0 or col >= self.COLS:
            return False, None
        
        card = self.board[row][col]
        
        if card.state != CardState.HIDDEN:
            return False, None
        
        if len(self.flipped_cards) >= 2:
            return False, None
        
        if self.waiting_for_hide:
            return False, None
        
        card.flip()
        self.flipped_cards.append(card)
        self.last_flip_time = time.time()
        
        if len(self.flipped_cards) == 2:
            card1, card2 = self.flipped_cards
            if card1.fruit_type == card2.fruit_type:
                card1.match()
                card2.match()
                self.matched_pairs += 1
                matched_cards = self.flipped_cards.copy()
                self.flipped_cards = []
                
                if self.matched_pairs >= self.total_pairs:
                    self.won = True
                    self.is_running = False
                
                return True, matched_cards
            else:
                self.waiting_for_hide = True
                return True, None
        
        return True, None
    
    def check_and_hide_unmatched(self) -> bool:
        if not self.waiting_for_hide:
            return False
        
        if time.time() - self.last_flip_time >= self.MATCH_DELAY:
            for card in self.flipped_cards:
                card.hide()
            self.flipped_cards = []
            self.waiting_for_hide = False
            return True
        
        return False
    
    def update_time(self) -> float:
        if not self.start_time:
            return self.GAME_DURATION
        
        elapsed = time.time() - self.start_time
        self.remaining_time = max(0, self.GAME_DURATION - elapsed)
        
        if self.remaining_time <= 0 and not self.won:
            self.game_over = True
            self.is_running = False
        
        return self.remaining_time
    
    def next_turn(self):
        pass
    
    def is_game_over(self) -> bool:
        return self.game_over or self.won
    
    def get_winner(self):
        if self.won:
            return "You Win!"
        return None
    
    def get_state(self) -> dict:
        state = super().get_state()
        board_state = []
        for row in self.board:
            row_state = []
            for card in row:
                row_state.append({
                    "fruit": card.fruit_type.name,
                    "state": card.state.name,
                    "emoji": card.get_emoji(),
                    "row": card.row,
                    "col": card.col
                })
            board_state.append(row_state)
        
        state.update({
            "rows": self.ROWS,
            "cols": self.COLS,
            "board": board_state,
            "flipped_count": len(self.flipped_cards),
            "matched_pairs": self.matched_pairs,
            "total_pairs": self.total_pairs,
            "remaining_time": self.remaining_time,
            "game_over": self.game_over,
            "won": self.won,
            "waiting_for_hide": self.waiting_for_hide
        })
        return state
