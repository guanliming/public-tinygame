import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import Optional, List
import flet as ft
from games.gomoku.game import GomokuGame, PlayerColor


class GomokuGameUI:
    """五子棋游戏界面"""
    
    def __init__(self, on_exit=None):
        self.game: Optional[GomokuGame] = None
        self.page: Optional[ft.Page] = None
        self.on_exit = on_exit
        
        self.board_container: Optional[ft.Container] = None
        self.cells_grid: Optional[ft.GridView] = None
        self.turn_text: Optional[ft.Text] = None
        self.win_cells: List[int] = []
        
        self.welcome_screen: Optional[ft.Container] = None
        self.game_screen: Optional[ft.Container] = None
        
        self.start_button: Optional[ft.Button] = None
        self.exit_button: Optional[ft.Button] = None
        self.game_exit_button: Optional[ft.Button] = None
        self.win_restart_button: Optional[ft.Button] = None
        self.win_exit_button: Optional[ft.Button] = None
    
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
            "黑棋先行",
            size=24,
            color=ft.Colors.BLACK,
            weight=ft.FontWeight.BOLD
        )
        
        self.cells_grid = ft.GridView(
            width=600,
            height=600,
            runs_count=15,
            spacing=0,
            run_spacing=0
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
                        "五子棋",
                        size=48,
                        color=ft.Colors.BLUE,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "人机对战五子棋",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "黑棋先行，先连成五子者获胜",
                        size=18,
                        color=ft.Colors.WHITE
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
        print("[DEBUG Gomoku] _show_welcome_screen called")
        print(f"[DEBUG Gomoku] self.page is None: {self.page is None}")
        print(f"[DEBUG Gomoku] welcome_screen visible before: {self.welcome_screen.visible if self.welcome_screen else 'None'}")
        print(f"[DEBUG Gomoku] game_screen visible before: {self.game_screen.visible if self.game_screen else 'None'}")
        
        self.welcome_screen.visible = True
        self.game_screen.visible = False
        
        print(f"[DEBUG Gomoku] welcome_screen visible after: {self.welcome_screen.visible}")
        print(f"[DEBUG Gomoku] game_screen visible after: {self.game_screen.visible}")
        
        if self.page:
            print("[DEBUG Gomoku] Calling page.update()...")
            self.page.update()
            print("[DEBUG Gomoku] page.update() completed")
        else:
            print("[DEBUG Gomoku] self.page is None, cannot update")
    
    def _show_game_screen(self):
        """显示游戏界面"""
        self.welcome_screen.visible = False
        self.game_screen.visible = True
        
        if self.page:
            self.page.update()
    
    def _start_game(self, e):
        """开始游戏"""
        self.game = GomokuGame()
        self.game.init_game()
        self.game.is_running = True
        self.win_cells = []
        
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
            if self.game.current_player == PlayerColor.BLACK:
                self.turn_text.value = "黑棋回合（玩家）"
                self.turn_text.color = ft.Colors.BLACK
            else:
                self.turn_text.value = "白棋回合（AI）"
                self.turn_text.color = ft.Colors.WHITE
            self.turn_text.update()
    
    def _is_board_full(self) -> bool:
        """检查棋盘是否已满"""
        if not self.game:
            return True
        
        for row in range(self.game.BOARD_SIZE):
            for col in range(self.game.BOARD_SIZE):
                if self.game.board[row][col] is None:
                    return False
        return True
    
    def _render_board(self):
        """渲染游戏面板"""
        if not self.game or not self.cells_grid:
            return
        
        self.cells_grid.controls.clear()
        
        for row in range(self.game.BOARD_SIZE):
            for col in range(self.game.BOARD_SIZE):
                cell = self.game.board[row][col]
                btn = self._create_cell_button(cell, row, col)
                self.cells_grid.controls.append(btn)
        
        self.cells_grid.update()
    
    def _create_cell_button(self, cell: PlayerColor, row: int, col: int) -> ft.Container:
        """创建单元格按钮"""
        is_win_cell = (row * self.game.BOARD_SIZE + col) in self.win_cells
        
        container = ft.Container(
            width=40,
            height=40,
            alignment=ft.Alignment(0, 0),
            bgcolor=ft.Colors.BROWN_400,
            border=ft.Border.all(1, ft.Colors.BROWN_700),
            on_click=lambda e, r=row, c=col: self._on_cell_click(r, c)
        )
        
        if cell == PlayerColor.BLACK:
            container.content = ft.Container(
                width=32,
                height=32,
                bgcolor=ft.Colors.YELLOW if is_win_cell else ft.Colors.BLACK,
                border_radius=16,
                border=ft.Border.all(2, ft.Colors.RED if is_win_cell else ft.Colors.WHITE)
            )
        elif cell == PlayerColor.WHITE:
            container.content = ft.Container(
                width=32,
                height=32,
                bgcolor=ft.Colors.YELLOW if is_win_cell else ft.Colors.WHITE,
                border_radius=16,
                border=ft.Border.all(2, ft.Colors.RED if is_win_cell else ft.Colors.BLACK)
            )
        
        return container
    
    def _on_cell_click(self, row: int, col: int):
        """单元格点击事件"""
        if not self.game:
            return
        
        if not self.game.is_running:
            return
        
        if self.game.current_player != PlayerColor.BLACK:
            return
        
        if not self.game.is_valid_move(col, row):
            return
        
        self.game.make_move(col, row)
        self._update_turn_display()
        self._render_board()
        
        if self.game.game_over:
            self.win_cells = []
            self._render_board()
            self.game.is_running = False
            self._show_win_message()
            return
        
        if self._is_board_full():
            self.game.is_running = False
            self._show_draw_message()
            return
        
        self._do_ai_move()
    
    def _do_ai_move(self):
        """执行AI走棋"""
        if not self.game:
            return
        
        ai_move = self.game.get_ai_move()
        
        if ai_move:
            x, y = ai_move
            self.game.make_move(x, y)
            self._update_turn_display()
            self._render_board()
            
            if self.game.game_over:
                self.win_cells = []
                self._render_board()
                self.game.is_running = False
                self._show_win_message()
                return
            
            if self._is_board_full():
                self.game.is_running = False
                self._show_draw_message()
                return
    
    def _show_win_message(self):
        """显示胜利消息"""
        winner = "黑棋" if self.game.winner == PlayerColor.BLACK else "白棋"
        self._show_game_over_screen(winner, won=(self.game.winner == PlayerColor.BLACK))
    
    def _show_draw_message(self):
        """显示平局消息"""
        self._show_game_over_screen("平局", won=False)
    
    def _show_game_over_screen(self, message: str, won: bool):
        """显示游戏结束界面"""
        import flet as ft
        
        content_col = self.game_screen.content
        
        if len(content_col.controls) > 3:
            content_col.controls = content_col.controls[:3]
        
        if won:
            title_text = "恭喜获胜！"
            title_color = ft.Colors.GREEN
        elif message == "平局":
            title_text = "游戏结束"
            title_color = ft.Colors.ORANGE
        else:
            title_text = "游戏结束"
            title_color = ft.Colors.RED
        
        result_text = ft.Text(
            title_text,
            size=36,
            color=title_color,
            weight=ft.FontWeight.BOLD
        )
        
        message_text = ft.Text(
            message,
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
