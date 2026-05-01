import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import asyncio
from typing import Optional, List
import flet as ft
from games.junqi.game import (
    JunqiGame, PlayerSide, Piece, PieceType, Position
)


class JunqiGameUI:
    """军棋游戏界面"""
    
    def __init__(self, on_exit=None):
        self.game: Optional[JunqiGame] = None
        self.page: Optional[ft.Page] = None
        self.on_exit = on_exit
        
        self.board_container: Optional[ft.Container] = None
        self.cells_grid: Optional[ft.GridView] = None
        self.turn_text: Optional[ft.Text] = None
        self.selected_pos: Optional[Position] = None
        self.valid_moves: List[Position] = []
        
        self.welcome_screen: Optional[ft.Container] = None
        self.game_screen: Optional[ft.Container] = None
        
        self.start_button: Optional[ft.Button] = None
        self.exit_button: Optional[ft.Button] = None
        self.game_exit_button: Optional[ft.Button] = None
        self.win_restart_button: Optional[ft.Button] = None
        self.win_exit_button: Optional[ft.Button] = None
        
        self.PIECE_NAMES = {
            PieceType.COMMANDER: "司令",
            PieceType.CORPS: "军长",
            PieceType.DIVISION: "师长",
            PieceType.BRIGADE: "旅长",
            PieceType.REGIMENT: "团长",
            PieceType.BATTALION: "营长",
            PieceType.COMPANY: "连长",
            PieceType.PLATOON: "排长",
            PieceType.ENGINEER: "工兵",
            PieceType.BOMB: "炸弹",
            PieceType.MINE: "地雷",
            PieceType.FLAG: "军旗",
        }
    
    def build(self, page: ft.Page):
        """构建并返回UI控件"""
        self.page = page
        return self._build_ui()
    
    def show(self):
        """显示初始界面"""
        self._show_welcome_screen()
    
    def _build_ui(self):
        """构建UI"""
        self.turn_text = ft.Text(
            "红方回合",
            size=24,
            color=ft.Colors.RED,
            weight=ft.FontWeight.BOLD
        )
        
        self.cells_grid = ft.GridView(
            width=480,
            height=400,
            runs_count=12,
            spacing=1,
            run_spacing=1
        )
        
        self.board_container = ft.Container(
            content=self.cells_grid,
            padding=10,
            bgcolor=ft.Colors.BROWN_500,
            border=ft.Border.all(5, ft.Colors.BROWN_800),
            border_radius=10
        )
        
        self.start_button = ft.Button(
            "开始游戏",
            on_click=self._start_game,
            width=200,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
            )
        )
        
        self.exit_button = ft.Button(
            "退出游戏",
            on_click=self._exit_to_selector,
            width=200,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.RED,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
            )
        )
        
        self.game_exit_button = ft.Button(
            "退出",
            on_click=self._exit_game_during_play,
            width=100,
            height=40,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.RED,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD)
            )
        )
        
        self.win_restart_button = ft.Button(
            "再来一局",
            on_click=self._win_screen_restart,
            width=200,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
            )
        )
        
        self.win_exit_button = ft.Button(
            "退出游戏",
            on_click=self._win_screen_exit,
            width=200,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.RED,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
            )
        )
        
        self.welcome_screen = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "军棋",
                        size=48,
                        color=ft.Colors.BLUE,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "人机对战军棋",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "红方先行，吃掉对方军旗获胜",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "规则：司令 > 军长 > 师长 > 旅长 > 团长 > 营长 > 连长 > 排长 > 工兵",
                        size=14,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Text(
                        "炸弹: 与任何棋子同归于尽 | 地雷: 只能被工兵挖或炸弹炸",
                        size=14,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Text(
                        "铁路线: 可沿铁路直线任意距离移动 | 工兵可沿铁路线拐弯",
                        size=14,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Divider(height=50, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [self.start_button, self.exit_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            expand=True,
            alignment=ft.Alignment(0, 0)
        )
        
        self.game_screen = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [self.turn_text, ft.Container(expand=True), self.game_exit_button],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [self.board_container],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            expand=True,
            visible=False
        )
        
        return ft.Stack(
            [
                self.welcome_screen,
                self.game_screen
            ],
            expand=True
        )
    
    def _show_welcome_screen(self):
        """显示欢迎界面"""
        self.welcome_screen.visible = True
        self.game_screen.visible = False
        
        if self.page:
            self.page.update()
    
    def _show_game_screen(self):
        """显示游戏界面"""
        self.welcome_screen.visible = False
        self.game_screen.visible = True
        
        if self.page:
            self.page.update()
    
    def _start_game(self, e):
        """开始游戏"""
        self.game = JunqiGame()
        self.game.init_game()
        self.game.setup_default_board()
        self.game.is_running = True
        self.selected_pos = None
        self.valid_moves = []
        
        self._update_turn_display()
        self._render_board()
        
        self._show_game_screen()
    
    def _exit_to_selector(self, e):
        """退出到游戏选择页面"""
        self.game = None
        if self.on_exit:
            self.on_exit()
    
    def _exit_game_during_play(self, e):
        """游戏进行中退出"""
        self.game = None
        self._exit_to_selector(e)
    
    def _win_screen_restart(self, e):
        """胜利界面重新开始"""
        self._start_game(e)
    
    def _win_screen_exit(self, e):
        """胜利界面退出"""
        self._exit_to_selector(e)
    
    def _update_turn_display(self):
        """更新回合显示"""
        if self.game:
            if self.game.current_player == PlayerSide.RED:
                self.turn_text.value = "红方回合（玩家）"
                self.turn_text.color = ft.Colors.RED
            else:
                self.turn_text.value = "蓝方回合（AI）"
                self.turn_text.color = ft.Colors.BLUE
            self.turn_text.update()
    
    def _render_board(self):
        """渲染游戏面板"""
        if not self.game or not self.cells_grid:
            return
        
        self.cells_grid.controls.clear()
        
        for row in range(self.game.BOARD_HEIGHT):
            for col in range(self.game.BOARD_WIDTH):
                piece = self.game.board[row][col]
                pos = Position(col, row)
                is_selected = self.selected_pos == pos
                is_valid_move = pos in self.valid_moves
                btn = self._create_cell_button(piece, row, col, is_selected, is_valid_move)
                self.cells_grid.controls.append(btn)
        
        self.cells_grid.update()
    
    def _create_cell_button(self, piece: Optional[Piece], row: int, col: int, 
                            is_selected: bool, is_valid_move: bool) -> ft.Container:
        """创建单元格按钮"""
        pos = Position(col, row)
        
        bg_color = ft.Colors.BROWN_300
        if self.game.is_camp(pos):
            bg_color = ft.Colors.BROWN_200
        elif self.game.is_railway(pos):
            bg_color = ft.Colors.BROWN_400
        
        if is_selected:
            border = ft.Border.all(3, ft.Colors.YELLOW)
        elif is_valid_move:
            border = ft.Border.all(2, ft.Colors.GREEN)
        else:
            border = ft.Border.all(1, ft.Colors.BROWN_700)
        
        container = ft.Container(
            width=38,
            height=38,
            alignment=ft.Alignment(0, 0),
            bgcolor=bg_color,
            border=border,
            border_radius=3,
            on_click=lambda e, r=row, c=col: self._on_cell_click(r, c)
        )
        
        if piece and piece.is_alive:
            if piece.side == PlayerSide.RED:
                text_color = ft.Colors.RED
                if piece.piece_type == PieceType.FLAG:
                    emoji = "🚩"
                else:
                    emoji = self.PIECE_NAMES.get(piece.piece_type, "?")
            else:
                text_color = ft.Colors.BLUE
                if piece.piece_type == PieceType.FLAG:
                    emoji = "🏁"
                else:
                    emoji = self.PIECE_NAMES.get(piece.piece_type, "?")
            
            container.content = ft.Text(
                emoji,
                size=10,
                color=text_color,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER
            )
        
        return container
    
    def _on_cell_click(self, row: int, col: int):
        """单元格点击事件"""
        if not self.game or not self.game.is_running:
            return
        
        if self.game.current_player != PlayerSide.RED:
            return
        
        clicked_pos = Position(col, row)
        
        if self.selected_pos is None:
            piece = self.game.board[row][col]
            if piece and piece.is_alive and piece.side == PlayerSide.RED and piece.can_move():
                self.selected_pos = clicked_pos
                self.valid_moves = self.game.get_valid_moves(clicked_pos)
                self._render_board()
        else:
            if clicked_pos == self.selected_pos:
                self.selected_pos = None
                self.valid_moves = []
                self._render_board()
                return
            
            piece = self.game.board[row][col]
            if piece and piece.is_alive and piece.side == PlayerSide.RED:
                if piece.can_move():
                    self.selected_pos = clicked_pos
                    self.valid_moves = self.game.get_valid_moves(clicked_pos)
                    self._render_board()
                return
            
            if clicked_pos in self.valid_moves:
                success, result = self.game.make_move(self.selected_pos, clicked_pos)
                
                if success:
                    self.selected_pos = None
                    self.valid_moves = []
                    self._render_board()
                    
                    if self.game.game_over:
                        self.game.is_running = False
                        self._show_win_message()
                        return
                    
                    self._update_turn_display()
                    
                    self._do_ai_move()
                else:
                    self.selected_pos = None
                    self.valid_moves = []
                    self._render_board()
            else:
                self.selected_pos = None
                self.valid_moves = []
                self._render_board()
    
    def _do_ai_move(self):
        """执行AI走棋"""
        if not self.game:
            return
        
        ai_move = self.game.get_ai_move()
        
        if ai_move:
            from_pos, to_pos = ai_move
            self.game.make_move(from_pos, to_pos)
            self._update_turn_display()
            self._render_board()
            
            if self.game.game_over:
                self.game.is_running = False
                self._show_win_message()
                return
    
    def _show_win_message(self):
        """显示胜利消息"""
        if self.game.winner == PlayerSide.RED:
            winner = "红方（玩家）"
            won = True
        else:
            winner = "蓝方（AI）"
            won = False
        self._show_game_over_screen(winner, won)
    
    def _show_game_over_screen(self, message: str, won: bool):
        """显示游戏结束界面"""
        import flet as ft
        
        content_col = self.game_screen.content
        
        if len(content_col.controls) > 3:
            content_col.controls = content_col.controls[:3]
        
        title_text = "恭喜获胜！" if won else "游戏结束"
        title_color = ft.Colors.GREEN if won else ft.Colors.RED
        
        result_text = ft.Text(
            title_text,
            size=36,
            color=title_color,
            weight=ft.FontWeight.BOLD
        )
        
        message_text = ft.Text(
            f"{message}获胜！",
            size=24,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        buttons_row = ft.Row(
            [self.win_restart_button, self.win_exit_button],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
        
        content_col.controls.extend([
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            result_text,
            message_text,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            buttons_row
        ])
        
        content_col.update()
