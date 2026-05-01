import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import random
import json
from typing import List, Optional, Tuple, Dict
from enum import Enum
from core.base_game import BaseGame


class PlayerSide(Enum):
    """玩家阵营"""
    RED = 1
    BLUE = 2


class PieceType(Enum):
    """棋子类型"""
    FLAG = 0
    MINE = 1
    BOMB = 2
    ENGINEER = 3
    PLATOON = 4
    COMPANY = 5
    BATTALION = 6
    REGIMENT = 7
    BRIGADE = 8
    DIVISION = 9
    CORPS = 10
    COMMANDER = 11


PIECE_NAMES = {
    PieceType.FLAG: "军旗",
    PieceType.MINE: "地雷",
    PieceType.BOMB: "炸弹",
    PieceType.ENGINEER: "工兵",
    PieceType.PLATOON: "排长",
    PieceType.COMPANY: "连长",
    PieceType.BATTALION: "营长",
    PieceType.REGIMENT: "团长",
    PieceType.BRIGADE: "旅长",
    PieceType.DIVISION: "师长",
    PieceType.CORPS: "军长",
    PieceType.COMMANDER: "司令"
}


PIECE_RANK = {
    PieceType.FLAG: 0,
    PieceType.MINE: -1,
    PieceType.BOMB: -2,
    PieceType.ENGINEER: 1,
    PieceType.PLATOON: 2,
    PieceType.COMPANY: 3,
    PieceType.BATTALION: 4,
    PieceType.REGIMENT: 5,
    PieceType.BRIGADE: 6,
    PieceType.DIVISION: 7,
    PieceType.CORPS: 8,
    PieceType.COMMANDER: 9
}


class Position:
    """位置类"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Position({self.x}, {self.y})"

    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)


class Piece:
    """棋子类"""

    def __init__(self, piece_type: PieceType, side: PlayerSide, position: Position):
        self.piece_type = piece_type
        self.side = side
        self.position = position
        self.is_alive = True

    def can_move(self) -> bool:
        """判断棋子是否可以移动"""
        return self.piece_type not in [PieceType.FLAG, PieceType.MINE]

    def get_name(self) -> str:
        return PIECE_NAMES[self.piece_type]

    def get_rank(self) -> int:
        return PIECE_RANK[self.piece_type]

    def to_dict(self) -> dict:
        return {
            "type": self.piece_type.value,
            "side": self.side.value,
            "position": self.position.to_tuple(),
            "is_alive": self.is_alive
        }


class Move:
    """走棋类"""

    def __init__(self, from_pos: Position, to_pos: Position, piece: Piece, captured_piece: Optional[Piece] = None):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece = piece
        self.captured_piece = captured_piece
        self.result = None


class GamePhase(Enum):
    """游戏阶段"""
    LAYOUT = 1
    PLAYING = 2
    GAME_OVER = 3


class JunqiGame(BaseGame):
    """军旗游戏类"""

    BOARD_WIDTH = 5
    BOARD_HEIGHT = 12

    RED_TOP = 6
    RED_BOTTOM = 11
    BLUE_TOP = 0
    BLUE_BOTTOM = 5

    def __init__(self):
        super().__init__("军旗")
        self.board: List[List[Optional[Piece]]] = []
        self.pieces: Dict[PlayerSide, List[Piece]] = {
            PlayerSide.RED: [],
            PlayerSide.BLUE: []
        }
        self.current_player: PlayerSide = PlayerSide.RED
        self.game_over: bool = False
        self.winner: Optional[PlayerSide] = None
        self.moves: List[Move] = []
        self.last_ai_move: Optional[Move] = None
        self.phase: GamePhase = GamePhase.LAYOUT
        self.revealed_pieces: Dict[Tuple[int, int], bool] = {}
        self.selected_piece_for_layout: Optional[Tuple[int, int]] = None

    def init_game(self) -> None:
        """初始化游戏"""
        self.board = [[None for _ in range(self.BOARD_WIDTH)] for _ in range(self.BOARD_HEIGHT)]
        self.pieces = {
            PlayerSide.RED: [],
            PlayerSide.BLUE: []
        }
        self.current_player = PlayerSide.RED
        self.game_over = False
        self.winner = None
        self.moves = []
        self.last_ai_move = None
        self.is_running = False
        self.phase = GamePhase.LAYOUT
        self.revealed_pieces = {}
        self.selected_piece_for_layout = None

    def start(self) -> None:
        """开始游戏"""
        self.init_game()
        self.is_running = True

    def setup_default_board(self) -> None:
        """设置默认棋盘布局"""
        self._generate_default_pieces(PlayerSide.RED)
        self._generate_default_pieces(PlayerSide.BLUE)

    def _generate_default_pieces(self, side: PlayerSide) -> List[Piece]:
        """生成默认棋子布局"""
        pieces = []

        if side == PlayerSide.RED:
            mine_positions = [(0, 11), (4, 11), (2, 10)]
            bomb_positions = [(1, 10), (3, 10)]
            engineer_positions = [(0, 8), (4, 8), (2, 6)]
            platoon_positions = [(1, 8), (3, 8), (4, 6)]
            company_positions = [(0, 9), (4, 9), (0, 6)]
            battalion_positions = [(0, 7), (4, 7)]
            regiment_positions = [(2, 9), (3, 6)]
            brigade_positions = [(2, 7), (1, 6)]
            division_positions = [(0, 10), (4, 10)]
            corps_position = (1, 11)
            commander_position = (3, 11)
            flag_position = (2, 11)
        else:
            mine_positions = [(0, 0), (4, 0), (2, 1)]
            bomb_positions = [(1, 1), (3, 1)]
            engineer_positions = [(0, 3), (4, 3), (2, 5)]
            platoon_positions = [(1, 3), (3, 3), (4, 5)]
            company_positions = [(0, 2), (4, 2), (0, 5)]
            battalion_positions = [(0, 4), (4, 4)]
            regiment_positions = [(2, 2), (3, 5)]
            brigade_positions = [(2, 4), (1, 5)]
            division_positions = [(0, 1), (4, 1)]
            corps_position = (1, 0)
            commander_position = (3, 0)
            flag_position = (2, 0)

        def add_piece(piece_type: PieceType, x: int, y: int):
            piece = Piece(piece_type, side, Position(x, y))
            pieces.append(piece)
            self.board[y][x] = piece
            self.pieces[side].append(piece)

        add_piece(PieceType.FLAG, flag_position[0], flag_position[1])

        for x, y in mine_positions:
            add_piece(PieceType.MINE, x, y)

        for x, y in bomb_positions:
            add_piece(PieceType.BOMB, x, y)

        for x, y in engineer_positions:
            add_piece(PieceType.ENGINEER, x, y)

        for x, y in platoon_positions:
            add_piece(PieceType.PLATOON, x, y)

        for x, y in company_positions:
            add_piece(PieceType.COMPANY, x, y)

        for x, y in battalion_positions:
            add_piece(PieceType.BATTALION, x, y)

        for x, y in regiment_positions:
            add_piece(PieceType.REGIMENT, x, y)

        for x, y in brigade_positions:
            add_piece(PieceType.BRIGADE, x, y)

        for x, y in division_positions:
            add_piece(PieceType.DIVISION, x, y)

        add_piece(PieceType.CORPS, corps_position[0], corps_position[1])
        add_piece(PieceType.COMMANDER, commander_position[0], commander_position[1])

        return pieces

    def is_piece_visible(self, piece: Piece, viewer: PlayerSide) -> bool:
        """判断棋子对某个玩家是否可见"""
        if piece.side == viewer:
            return True
        pos_tuple = (piece.position.x, piece.position.y)
        return self.revealed_pieces.get(pos_tuple, False)

    def reveal_piece(self, x: int, y: int) -> None:
        """揭示棋子（战斗后或特殊情况）"""
        self.revealed_pieces[(x, y)] = True

    def is_valid_position(self, x: int, y: int) -> bool:
        """判断是否是有效棋盘位置"""
        if x < 0 or x >= self.BOARD_WIDTH or y < 0 or y >= self.BOARD_HEIGHT:
            return False
        return True

    def get_camp_positions(self, side: PlayerSide) -> List[Tuple[int, int]]:
        """获取某方的行营位置"""
        if side == PlayerSide.RED:
            return [
                (1, 7), (3, 7),
                (2, 8),
                (1, 9), (3, 9)
            ]
        else:
            return [
                (1, 2), (3, 2),
                (2, 3),
                (1, 4), (3, 4)
            ]

    def is_camp(self, pos: Position) -> bool:
        """判断位置是否是行营"""
        red_camps = self.get_camp_positions(PlayerSide.RED)
        blue_camps = self.get_camp_positions(PlayerSide.BLUE)
        return pos.to_tuple() in red_camps or pos.to_tuple() in blue_camps

    def get_base_positions(self, side: PlayerSide) -> List[Tuple[int, int]]:
        """获取某方的大本营位置"""
        if side == PlayerSide.RED:
            return [(0, 11), (2, 11), (4, 11)]
        else:
            return [(0, 0), (2, 0), (4, 0)]

    def is_base(self, pos: Position, side: PlayerSide) -> bool:
        """判断位置是否是某方的大本营"""
        return pos.to_tuple() in self.get_base_positions(side)

    def get_valid_layout_positions(self, side: PlayerSide) -> List[Tuple[int, int]]:
        """获取某方可以布局的位置（兵站和大本营）"""
        if side == PlayerSide.RED:
            positions = []
            for y in range(6, 12):
                for x in range(5):
                    if not self.is_camp(Position(x, y)):
                        positions.append((x, y))
            return positions
        else:
            positions = []
            for y in range(0, 6):
                for x in range(5):
                    if not self.is_camp(Position(x, y)):
                        positions.append((x, y))
            return positions

    def can_place_piece(self, piece_type: PieceType, x: int, y: int, side: PlayerSide) -> bool:
        """判断棋子是否可以放置在某个位置"""
        if self.is_camp(Position(x, y)):
            return False

        base_positions = self.get_base_positions(side)
        if piece_type == PieceType.FLAG:
            return (x, y) in base_positions

        if piece_type == PieceType.MINE:
            if side == PlayerSide.RED:
                return y >= 10
            else:
                return y <= 1

        if piece_type == PieceType.BOMB:
            if side == PlayerSide.RED:
                return y < 11
            else:
                return y > 0

        return True

    def swap_pieces_for_layout(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        """布局阶段交换两个棋子的位置"""
        if self.phase != GamePhase.LAYOUT:
            return False

        piece1 = self.board[y1][x1]
        piece2 = self.board[y2][x2]

        if piece1 and piece1.side != PlayerSide.RED:
            return False

        if piece2 and piece2.side != PlayerSide.RED:
            return False

        if self.is_camp(Position(x1, y1)) or self.is_camp(Position(x2, y2)):
            return False

        if piece2 is None:
            if piece1 is None:
                return False
            if not self.can_place_piece(piece1.piece_type, x2, y2, PlayerSide.RED):
                return False

            self.board[y2][x2] = piece1
            self.board[y1][x1] = None
            piece1.position = Position(x2, y2)
            return True
        else:
            if piece1 is None:
                if not self.can_place_piece(piece2.piece_type, x1, y1, PlayerSide.RED):
                    return False

                self.board[y1][x1] = piece2
                self.board[y2][x2] = None
                piece2.position = Position(x1, y1)
                return True
            else:
                if not self.can_place_piece(piece1.piece_type, x2, y2, PlayerSide.RED):
                    return False
                if not self.can_place_piece(piece2.piece_type, x1, y1, PlayerSide.RED):
                    return False

                self.board[y1][x1] = piece2
                self.board[y2][x2] = piece1
                piece1.position = Position(x2, y2)
                piece2.position = Position(x1, y1)
                return True

    def start_play_phase(self) -> None:
        """开始对战阶段"""
        self.phase = GamePhase.PLAYING
        self.current_player = PlayerSide.RED

    def is_railway(self, pos: Position) -> bool:
        """判断位置是否在铁路线上"""
        if not self.is_valid_position(pos.x, pos.y):
            return False

        if pos.y in [1, 5, 6, 10]:
            return True
        if pos.x in [0, 4] and pos.y in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            return True

        return False

    def is_valid_move(self, from_pos: Position, to_pos: Position) -> bool:
        """判断走棋是否有效"""
        if self.phase != GamePhase.PLAYING:
            return False

        if from_pos == to_pos:
            return False

        piece = self.board[from_pos.y][from_pos.x]
        if not piece or not piece.is_alive:
            return False
        if piece.side != self.current_player:
            return False
        if not piece.can_move():
            return False

        to_piece = self.board[to_pos.y][to_pos.x]
        if to_piece and to_piece.is_alive and to_piece.side == piece.side:
            return False
        if to_piece and to_piece.is_alive and self.is_camp(to_pos):
            return False

        if self.is_on_road(from_pos, to_pos, piece):
            return True
        if self.is_on_railway(from_pos, to_pos, piece):
            return True

        return False

    def is_on_road(self, from_pos: Position, to_pos: Position, piece: Piece) -> bool:
        """判断是否是公路移动（一步）"""
        dx = abs(to_pos.x - from_pos.x)
        dy = abs(to_pos.y - from_pos.y)

        if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):
            if not self.is_camp(from_pos) and not self.is_camp(to_pos):
                return True

        camp_adjacent = {
            (1, 2): [(0, 2), (1, 1), (1, 3), (2, 2)],
            (3, 2): [(2, 2), (3, 1), (3, 3), (4, 2)],
            (2, 3): [(1, 3), (2, 2), (2, 4), (3, 3)],
            (1, 4): [(0, 4), (1, 3), (1, 5), (2, 4)],
            (3, 4): [(2, 4), (3, 3), (3, 5), (4, 4)],
            (1, 7): [(0, 7), (1, 6), (1, 8), (2, 7)],
            (3, 7): [(2, 7), (3, 6), (3, 8), (4, 7)],
            (2, 8): [(1, 8), (2, 7), (2, 9), (3, 8)],
            (1, 9): [(0, 9), (1, 8), (1, 10), (2, 9)],
            (3, 9): [(2, 9), (3, 8), (3, 10), (4, 9)],
        }

        from_tuple = from_pos.to_tuple()
        to_tuple = to_pos.to_tuple()

        if from_tuple in camp_adjacent and to_tuple in camp_adjacent[from_tuple]:
            return True
        if to_tuple in camp_adjacent and from_tuple in camp_adjacent[to_tuple]:
            return True

        return False

    def is_on_railway(self, from_pos: Position, to_pos: Position, piece: Piece) -> bool:
        """判断是否是铁路移动"""
        if not self.is_railway(from_pos) or not self.is_railway(to_pos):
            return False

        if piece.piece_type == PieceType.ENGINEER:
            return self._engineer_railway_move(from_pos, to_pos)
        else:
            return self._regular_railway_move(from_pos, to_pos)

    def _regular_railway_move(self, from_pos: Position, to_pos: Position) -> bool:
        """普通棋子铁路移动（直线）"""
        if from_pos.x != to_pos.x and from_pos.y != to_pos.y:
            return False

        if from_pos.x == to_pos.x:
            min_y = min(from_pos.y, to_pos.y)
            max_y = max(from_pos.y, to_pos.y)
            for y in range(min_y + 1, max_y):
                if self.board[y][from_pos.x] and self.board[y][from_pos.x].is_alive:
                    return False
        else:
            min_x = min(from_pos.x, to_pos.x)
            max_x = max(from_pos.x, to_pos.x)
            for x in range(min_x + 1, max_x):
                if self.board[from_pos.y][x] and self.board[from_pos.y][x].is_alive:
                    return False

        return True

    def _engineer_railway_move(self, from_pos: Position, to_pos: Position) -> bool:
        """工兵铁路移动（可转弯）"""
        if from_pos == to_pos:
            return False

        visited = set()
        queue = [from_pos]
        visited.add(from_pos.to_tuple())

        while queue:
            current = queue.pop(0)

            if current == to_pos:
                return True

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = Position(current.x + dx, current.y + dy)
                next_tuple = next_pos.to_tuple()

                if next_tuple in visited:
                    continue
                if not self.is_railway(next_pos):
                    continue
                if self.board[next_pos.y][next_pos.x] and self.board[next_pos.y][next_pos.x].is_alive:
                    if next_pos != to_pos:
                        continue

                visited.add(next_tuple)
                queue.append(next_pos)

        return False

    def get_valid_moves(self, pos: Position) -> List[Position]:
        """获取某个位置棋子的所有有效移动位置"""
        piece = self.board[pos.y][pos.x]
        if not piece or not piece.is_alive or not piece.can_move():
            return []

        valid_moves = []

        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                to_pos = Position(x, y)
                if self.is_valid_move(pos, to_pos):
                    valid_moves.append(to_pos)

        return valid_moves

    def make_move(self, from_pos: Position, to_pos: Position) -> Tuple[bool, str]:
        """执行走棋"""
        if not self.is_valid_move(from_pos, to_pos):
            return False, "无效走棋"

        piece = self.board[from_pos.y][from_pos.x]
        to_piece = self.board[to_pos.y][to_pos.x]

        move_result = None

        if to_piece and to_piece.is_alive:
            self.reveal_piece(from_pos.x, from_pos.y)
            self.reveal_piece(to_pos.x, to_pos.y)

            result, message = self._combat(piece, to_piece)
            move_result = result

            if result == "capture":
                to_piece.is_alive = False
                self.board[to_pos.y][to_pos.x] = piece
                self.board[from_pos.y][from_pos.x] = None
                piece.position = to_pos

                if to_piece.piece_type == PieceType.FLAG:
                    self.game_over = True
                    self.winner = piece.side
                    self.is_running = False
                    self.phase = GamePhase.GAME_OVER
                    move_result = "flag_capture"

            elif result == "both_die":
                piece.is_alive = False
                to_piece.is_alive = False
                self.board[to_pos.y][to_pos.x] = None
                self.board[from_pos.y][from_pos.x] = None

            elif result == "die":
                piece.is_alive = False
                self.board[from_pos.y][from_pos.x] = None
        else:
            self.board[to_pos.y][to_pos.x] = piece
            self.board[from_pos.y][from_pos.x] = None
            piece.position = to_pos

        move = Move(from_pos, to_pos, piece, to_piece)
        move.result = move_result
        self.moves.append(move)

        if self.current_player == PlayerSide.BLUE:
            self.last_ai_move = move

        if not self.game_over:
            self.current_player = PlayerSide.BLUE if self.current_player == PlayerSide.RED else PlayerSide.RED

        return True, move_result or "moved"

    def _combat(self, attacker: Piece, defender: Piece) -> Tuple[str, str]:
        """战斗结算"""
        if attacker.piece_type == PieceType.BOMB or defender.piece_type == PieceType.BOMB:
            return "both_die", "炸弹爆炸，同归于尽"

        if defender.piece_type == PieceType.MINE:
            if attacker.piece_type == PieceType.ENGINEER:
                return "capture", "工兵排雷成功"
            else:
                return "both_die", "触碰地雷，同归于尽"

        if defender.piece_type == PieceType.FLAG:
            return "capture", "军旗被夺，游戏结束"

        attacker_rank = attacker.get_rank()
        defender_rank = defender.get_rank()

        if attacker_rank > defender_rank:
            return "capture", f"{attacker.get_name()}吃掉{defender.get_name()}"
        elif attacker_rank == defender_rank:
            return "both_die", "同归于尽"
        else:
            return "die", f"{attacker.get_name()}被{defender.get_name()}吃掉"

    def get_ai_move(self) -> Optional[Tuple[Position, Position]]:
        """获取AI走棋"""
        if self.game_over or self.phase != GamePhase.PLAYING:
            return None

        if self.current_player != PlayerSide.BLUE:
            return None

        ai_pieces = [p for p in self.pieces[PlayerSide.BLUE] if p.is_alive and p.can_move()]

        if not ai_pieces:
            return None

        best_move = None
        best_score = -1

        for piece in ai_pieces:
            valid_moves = self.get_valid_moves(piece.position)

            for to_pos in valid_moves:
                score = self._evaluate_move(piece, to_pos)
                if score > best_score:
                    best_score = score
                    best_move = (piece.position, to_pos)
                elif score == best_score and random.random() > 0.5:
                    best_move = (piece.position, to_pos)

        if best_move:
            return best_move

        for piece in ai_pieces:
            valid_moves = self.get_valid_moves(piece.position)
            if valid_moves:
                return (piece.position, random.choice(valid_moves))

        return None

    def _evaluate_move(self, piece: Piece, to_pos: Position) -> int:
        """评估走棋分数"""
        score = 0
        to_piece = self.board[to_pos.y][to_pos.x]

        if to_piece and to_piece.is_alive and to_piece.side == PlayerSide.RED:
            if to_piece.piece_type == PieceType.FLAG:
                score += 100000
            elif to_piece.piece_type == PieceType.COMMANDER:
                score += 500
            elif to_piece.piece_type == PieceType.CORPS:
                score += 400
            elif to_piece.piece_type == PieceType.DIVISION:
                score += 300
            elif to_piece.piece_type == PieceType.BRIGADE:
                score += 200
            elif to_piece.piece_type == PieceType.REGIMENT:
                score += 150
            elif to_piece.piece_type == PieceType.BATTALION:
                score += 100
            elif to_piece.piece_type == PieceType.COMPANY:
                score += 80
            elif to_piece.piece_type == PieceType.PLATOON:
                score += 60
            elif to_piece.piece_type == PieceType.ENGINEER:
                score += 50
            elif to_piece.piece_type == PieceType.MINE:
                if piece.piece_type == PieceType.ENGINEER:
                    score += 200
                else:
                    score -= 100
            elif to_piece.piece_type == PieceType.BOMB:
                score -= 50

            attacker_rank = piece.get_rank()
            defender_rank = to_piece.get_rank()

            if to_piece.piece_type not in [PieceType.MINE, PieceType.BOMB]:
                if attacker_rank > defender_rank:
                    score += 50
                elif attacker_rank == defender_rank:
                    score -= 20
                else:
                    score -= 100
        else:
            if self.is_camp(to_pos):
                score += 30

            red_flag = [p for p in self.pieces[PlayerSide.RED] if p.piece_type == PieceType.FLAG and p.is_alive]
            if red_flag:
                flag_pos = red_flag[0].position
                distance = abs(to_pos.x - flag_pos.x) + abs(to_pos.y - flag_pos.y)
                score += max(0, 50 - distance * 2)

        return score

    def next_turn(self):
        """进入下一回合，返回当前玩家"""
        return self.current_player

    def is_game_over(self) -> bool:
        """判断游戏是否结束"""
        return self.game_over

    def get_winner(self):
        """获取获胜者"""
        return self.winner

    def save_board(self, filepath: str) -> bool:
        """保存棋盘布局"""
        try:
            board_data = {
                "red": [],
                "blue": []
            }

            for piece in self.pieces[PlayerSide.RED]:
                if piece.is_alive:
                    board_data["red"].append(piece.to_dict())

            for piece in self.pieces[PlayerSide.BLUE]:
                if piece.is_alive:
                    board_data["blue"].append(piece.to_dict())

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(board_data, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            print(f"保存棋盘失败: {e}")
            return False

    def load_board(self, filepath: str) -> bool:
        """加载棋盘布局"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                board_data = json.load(f)

            self.board = [[None for _ in range(self.BOARD_WIDTH)] for _ in range(self.BOARD_HEIGHT)]
            self.pieces = {
                PlayerSide.RED: [],
                PlayerSide.BLUE: []
            }

            for piece_data in board_data.get("red", []):
                piece = Piece(
                    PieceType(piece_data["type"]),
                    PlayerSide.RED,
                    Position(piece_data["position"][0], piece_data["position"][1])
                )
                piece.is_alive = piece_data.get("is_alive", True)
                self.board[piece.position.y][piece.position.x] = piece
                self.pieces[PlayerSide.RED].append(piece)

            for piece_data in board_data.get("blue", []):
                piece = Piece(
                    PieceType(piece_data["type"]),
                    PlayerSide.BLUE,
                    Position(piece_data["position"][0], piece_data["position"][1])
                )
                piece.is_alive = piece_data.get("is_alive", True)
                self.board[piece.position.y][piece.position.x] = piece
                self.pieces[PlayerSide.BLUE].append(piece)

            return True
        except Exception as e:
            print(f"加载棋盘失败: {e}")
            return False

    def get_state(self) -> dict:
        """获取游戏状态"""
        state = super().get_state()
        state.update({
            "board_width": self.BOARD_WIDTH,
            "board_height": self.BOARD_HEIGHT,
            "current_player": self.current_player.name if self.current_player else None,
            "game_over": self.game_over,
            "winner": self.winner.name if self.winner else None,
            "moves_count": len(self.moves),
            "phase": self.phase.name
        })
        return state


def get_all_pieces() -> List[Tuple[PieceType, int]]:
    """获取所有棋子类型和数量"""
    return [
        (PieceType.FLAG, 1),
        (PieceType.MINE, 3),
        (PieceType.BOMB, 2),
        (PieceType.ENGINEER, 3),
        (PieceType.PLATOON, 3),
        (PieceType.COMPANY, 3),
        (PieceType.BATTALION, 2),
        (PieceType.REGIMENT, 2),
        (PieceType.BRIGADE, 2),
        (PieceType.DIVISION, 2),
        (PieceType.CORPS, 1),
        (PieceType.COMMANDER, 1)
    ]


def generate_default_board() -> Dict[PlayerSide, List[Piece]]:
    """生成默认棋盘布局"""
    game = JunqiGame()
    game.init_game()
    game.setup_default_board()
    return game.pieces
