import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import random
import time
from enum import Enum
from typing import List, Set, Optional
from core.base_game import BaseGame


class HoleState(Enum):
    EMPTY = 0
    SQUIRREL = 1
    HIT = 2


class WhackAMoleGame(BaseGame):
    HOLES_COUNT = 16
    GAME_DURATION = 20
    SQUIRRELS_PER_SECOND = 3
    SQUIRREL_STAY_TIME = 0.3
    WIN_SCORE = 20

    def __init__(self):
        super().__init__("打地鼠")
        self.hole_states: List[HoleState] = []
        self.active_holes: Set[int] = set()
        self.score: int = 0
        self.start_time: float = 0
        self.game_over: bool = False
        self.won: bool = False
        self.remaining_time: float = self.GAME_DURATION

    def init_game(self) -> None:
        self.hole_states = [HoleState.EMPTY for _ in range(self.HOLES_COUNT)]
        self.active_holes = set()
        self.score = 0
        self.start_time = 0
        self.game_over = False
        self.won = False
        self.remaining_time = self.GAME_DURATION
        self.is_running = False

    def start(self) -> None:
        self.init_game()
        self.is_running = True
        self.start_time = time.time()

    def spawn_squirrels(self) -> Set[int]:
        self._clear_expired_squirrels()
        
        if self.game_over or self.won:
            return set()

        available_holes = [i for i in range(self.HOLES_COUNT) if i not in self.active_holes]
        
        if len(available_holes) < self.SQUIRRELS_PER_SECOND:
            spawn_count = len(available_holes)
        else:
            spawn_count = self.SQUIRRELS_PER_SECOND

        if spawn_count > 0:
            new_holes = set(random.sample(available_holes, spawn_count))
            for hole_index in new_holes:
                self.hole_states[hole_index] = HoleState.SQUIRREL
            self.active_holes.update(new_holes)
            return new_holes
        return set()

    def _clear_expired_squirrels(self) -> None:
        for hole_index in list(self.active_holes):
            if self.hole_states[hole_index] == HoleState.SQUIRREL:
                self.hole_states[hole_index] = HoleState.EMPTY
                self.active_holes.discard(hole_index)

    def hide_squirrels(self, hole_indices: Set[int]) -> None:
        for hole_index in hole_indices:
            if self.hole_states[hole_index] == HoleState.SQUIRREL:
                self.hole_states[hole_index] = HoleState.EMPTY
                self.active_holes.discard(hole_index)

    def hit_hole(self, hole_index: int) -> bool:
        if self.game_over or self.won:
            return False

        if hole_index < 0 or hole_index >= self.HOLES_COUNT:
            return False

        if self.hole_states[hole_index] == HoleState.SQUIRREL:
            self.hole_states[hole_index] = HoleState.HIT
            self.active_holes.discard(hole_index)
            self.score += 1

            if self.score >= self.WIN_SCORE:
                self.won = True
                self.is_running = False
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
        state.update({
            "holes_count": self.HOLES_COUNT,
            "hole_states": [hs.name for hs in self.hole_states],
            "active_holes": list(self.active_holes),
            "score": self.score,
            "remaining_time": self.remaining_time,
            "game_over": self.game_over,
            "won": self.won,
            "win_score": self.WIN_SCORE
        })
        return state
