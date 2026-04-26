import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import random
from typing import List, Optional
from enum import Enum
from core.base_game import BaseGame


class ObstacleType(Enum):
    CAR = 1
    TRUCK = 2
    ROCK = 3


class Obstacle:
    def __init__(self, lane: int, y: float, obstacle_type: ObstacleType):
        self.lane = lane
        self.y = y
        self.type = obstacle_type
        self.width = 40
        self.height = 60 if obstacle_type == ObstacleType.TRUCK else 45


class RoadLine:
    def __init__(self, y: float):
        self.y = y
        self.height = 30
        self.gap = 40


class RacingGame(BaseGame):
    LANE_COUNT = 3
    BASE_SPEED = 50.0
    MAX_SPEED = 150.0
    ACCELERATION = 80.0
    DECELERATION = 40.0
    FRICTION = 20.0
    WIN_TIME = 30.0
    
    GAME_WIDTH = 300
    GAME_HEIGHT = 600
    PLAYER_WIDTH = 40
    PLAYER_HEIGHT = 60
    
    LANE_WIDTH = GAME_WIDTH // LANE_COUNT
    
    OBSTACLE_SPAWN_INTERVAL = 2.0
    OBSTACLE_MIN_SPAWN_INTERVAL = 1.0

    def __init__(self):
        super().__init__("赛车游戏")
        self.player_lane = 1
        self.player_y = self.GAME_HEIGHT - 150
        self.speed = self.BASE_SPEED
        self.is_accelerating = False
        self.obstacles: List[Obstacle] = []
        self.road_lines: List[RoadLine] = []
        self.game_time = 0.0
        self.last_spawn_time = 0.0
        self.game_over = False
        self.won = False
        self.collision_offset = 5

    def init_game(self) -> None:
        self.player_lane = 1
        self.player_y = self.GAME_HEIGHT - 150
        self.speed = self.BASE_SPEED
        self.is_accelerating = False
        self.obstacles = []
        self.road_lines = []
        self.game_time = 0.0
        self.last_spawn_time = 0.0
        self.game_over = False
        self.won = False
        self.is_running = False
        
        self._init_road_lines()

    def _init_road_lines(self) -> None:
        total_height = self.GAME_HEIGHT + 100
        line_height_with_gap = RoadLine(0).height + RoadLine(0).gap
        num_lines = int(total_height // line_height_with_gap) + 2
        
        for i in range(num_lines):
            y = -RoadLine(0).height + i * line_height_with_gap
            self.road_lines.append(RoadLine(y))

    def start(self) -> None:
        self.init_game()
        self.is_running = True

    def move_left(self) -> None:
        if self.player_lane > 0:
            self.player_lane -= 1

    def move_right(self) -> None:
        if self.player_lane < self.LANE_COUNT - 1:
            self.player_lane += 1

    def set_accelerating(self, accelerating: bool) -> None:
        self.is_accelerating = accelerating

    def _update_speed(self, delta_time: float) -> None:
        if self.is_accelerating:
            self.speed = min(self.speed + self.ACCELERATION * delta_time, self.MAX_SPEED)
        else:
            if self.speed > self.BASE_SPEED:
                self.speed = max(self.speed - self.DECELERATION * delta_time, self.BASE_SPEED)
            elif self.speed < self.BASE_SPEED:
                self.speed = min(self.speed + self.FRICTION * delta_time, self.BASE_SPEED)

    def _get_occupied_lanes_ahead(self) -> set:
        occupied = set()
        check_distance = 200
        for obstacle in self.obstacles:
            if obstacle.y < check_distance and obstacle.y > -100:
                occupied.add(obstacle.lane)
        return occupied
    
    def _spawn_obstacle(self) -> None:
        occupied_lanes = self._get_occupied_lanes_ahead()
        
        max_obstacles = min(2, self.LANE_COUNT - 1)
        num_obstacles = random.randint(1, max_obstacles)
        
        used_lanes = set()
        
        for _ in range(num_obstacles):
            available_lanes = [
                l for l in range(self.LANE_COUNT) 
                if l not in used_lanes and l not in occupied_lanes
            ]
            
            if not available_lanes:
                all_lanes = set(range(self.LANE_COUNT))
                available_lanes = list(all_lanes - used_lanes - occupied_lanes)
                
                if not available_lanes:
                    available_lanes = list(all_lanes - used_lanes)
                    if not available_lanes:
                        break
            
            lane = random.choice(available_lanes)
            used_lanes.add(lane)
            
            obstacle_type = ObstacleType.CAR
            
            obstacle = Obstacle(lane, -80, obstacle_type)
            self.obstacles.append(obstacle)

    def _update_obstacles(self, delta_time: float) -> None:
        speed_factor = self.speed / self.BASE_SPEED
        move_distance = self.speed * delta_time * 0.5
        
        for obstacle in self.obstacles[:]:
            obstacle.y += move_distance
            
            if obstacle.y > self.GAME_HEIGHT + 100:
                self.obstacles.remove(obstacle)

    def _update_road_lines(self, delta_time: float) -> None:
        speed_factor = self.speed / self.BASE_SPEED
        move_distance = self.speed * delta_time * 0.5
        
        for line in self.road_lines:
            line.y += move_distance
            
            line_height_with_gap = line.height + line.gap
            num_lines = len(self.road_lines)
            total_height = num_lines * line_height_with_gap
            
            if line.y > self.GAME_HEIGHT + 50:
                min_y = min(l.y for l in self.road_lines)
                line.y = min_y - line_height_with_gap

    def _check_collision(self) -> bool:
        player_x = self.player_lane * self.LANE_WIDTH + (self.LANE_WIDTH - self.PLAYER_WIDTH) // 2
        player_right = player_x + self.PLAYER_WIDTH
        player_top = self.player_y
        player_bottom = self.player_y + self.PLAYER_HEIGHT
        
        player_x += self.collision_offset
        player_right -= self.collision_offset
        player_top += self.collision_offset
        player_bottom -= self.collision_offset
        
        for obstacle in self.obstacles:
            obs_x = obstacle.lane * self.LANE_WIDTH + (self.LANE_WIDTH - obstacle.width) // 2
            obs_right = obs_x + obstacle.width
            obs_top = obstacle.y
            obs_bottom = obstacle.y + obstacle.height
            
            if (player_x < obs_right and player_right > obs_x and
                player_top < obs_bottom and player_bottom > obs_top):
                return True
        
        return False

    def update(self, delta_time: float) -> bool:
        if self.game_over or self.won:
            return False
        
        self._update_speed(delta_time)
        self.game_time += delta_time
        
        if self.game_time >= self.WIN_TIME:
            self.won = True
            self.is_running = False
            return False
        
        spawn_interval = max(
            self.OBSTACLE_MIN_SPAWN_INTERVAL,
            self.OBSTACLE_SPAWN_INTERVAL - (self.speed - self.BASE_SPEED) * 0.005
        )
        
        if self.game_time - self.last_spawn_time >= spawn_interval:
            self._spawn_obstacle()
            self.last_spawn_time = self.game_time
        
        self._update_obstacles(delta_time)
        self._update_road_lines(delta_time)
        
        if self._check_collision():
            self.game_over = True
            self.is_running = False
            return False
        
        return True

    def get_player_x(self) -> int:
        return self.player_lane * self.LANE_WIDTH + (self.LANE_WIDTH - self.PLAYER_WIDTH) // 2

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
            "player_lane": self.player_lane,
            "player_y": self.player_y,
            "speed": self.speed,
            "game_time": self.game_time,
            "obstacles": [
                {
                    "lane": o.lane,
                    "y": o.y,
                    "type": o.type.name,
                    "width": o.width,
                    "height": o.height
                }
                for o in self.obstacles
            ],
            "game_over": self.game_over,
            "won": self.won
        })
        return state
