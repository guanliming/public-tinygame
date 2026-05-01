import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import Optional, List
import flet as ft
from games.minesweeper.game import MinesweeperGame, CellState


class MinesweeperGameUI:
    """扫雷游戏界面"""
    
    def __init__(self, on_exit=None):
        self.game: Optional[MinesweeperGame] = None
        self.page: Optional[ft.Page] = None
        self.on_exit = on_exit
        
        self.flag_count_text: Optional[ft.Text] = None
        self.game_over_score_text: Optional[ft.Text] = None
        self.board_container: Optional[ft.Container] = None
        self.cells_grid: Optional[ft.GridView] = None
        
        self.welcome_screen: Optional[ft.Container] = None
        self.game_screen: Optional[ft.Container] = None
        self.game_over_screen: Optional[ft.Container] = None
        
        self.start_button: Optional[ft.Button] = None
        self.restart_button: Optional[ft.Button] = None
        self.back_button: Optional[ft.Button] = None
        self.exit_button: Optional[ft.Button] = None
        self.game_exit_button: Optional[ft.Button] = None
        
        self.cell_buttons: List[List[Optional[ft.Container]]] = []
    
    def build(self, page: ft.Page):
        """构建并返回UI控件"""
        self.page = page
        return self._build_ui()
    
    def show(self):
        """显示初始界面"""
        self._show_welcome_screen()
    
    def _build_ui(self):
        """构建UI"""
        self.flag_count_text = ft.Text(
            f"剩余旗子: {MinesweeperGame.MINE_COUNT}",
            size=20,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        self.game_over_score_text = ft.Text(
            "",
            size=24,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        self.cells_grid = ft.GridView(
            width=400,
            height=400,
            runs_count=10,
            spacing=2,
            run_spacing=2
        )
        
        self.board_container = ft.Container(
            content=self.cells_grid,
            padding=10,
            bgcolor=ft.Colors.GREY_900,
            border=ft.Border.all(5, ft.Colors.GREY_700),
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
        
        self.restart_button = ft.Button(
            "再玩一次",
            on_click=self._restart_game,
            width=200,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
            )
        )
        
        self.back_button = ft.Button(
            "返回",
            on_click=self._back_to_welcome,
            width=200,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREY,
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
        
        self.welcome_screen = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "扫雷游戏",
                        size=48,
                        color=ft.Colors.BLUE,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        f"{MinesweeperGame.GRID_WIDTH}×{MinesweeperGame.GRID_HEIGHT} 网格",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        f"{MinesweeperGame.MINE_COUNT} 颗雷",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "左键翻开格子，右键标记问号",
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
                        [self.flag_count_text, ft.Container(expand=True), self.game_exit_button],
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
        
        self.game_over_screen = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "游戏结束",
                        size=48,
                        color=ft.Colors.RED,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    self.game_over_score_text,
                    ft.Divider(height=50, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [self.restart_button, self.back_button, self.exit_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
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
                self.game_screen,
                self.game_over_screen
            ],
            expand=True
        )
    
    def _show_welcome_screen(self):
        """显示欢迎界面"""
        self.welcome_screen.visible = True
        self.game_screen.visible = False
        self.game_over_screen.visible = False
        
        if self.page:
            self.page.update()
    
    def _show_game_screen(self):
        """显示游戏界面"""
        self.welcome_screen.visible = False
        self.game_screen.visible = True
        self.game_over_screen.visible = False
        
        if self.page:
            self.page.update()
    
    def _show_game_over_screen(self, won: bool = False):
        """显示游戏结束界面"""
        self.welcome_screen.visible = False
        self.game_screen.visible = False
        self.game_over_screen.visible = True
        
        if won:
            self.game_over_screen.content.controls[0].value = "恭喜获胜！"
            self.game_over_screen.content.controls[0].color = ft.Colors.GREEN
            self.game_over_score_text.value = "你成功避开了所有地雷！"
        else:
            self.game_over_screen.content.controls[0].value = "游戏结束"
            self.game_over_screen.content.controls[0].color = ft.Colors.RED
            self.game_over_score_text.value = "你踩到了地雷！"
        
        if self.page:
            self.page.update()
    
    def _start_game(self, e):
        """开始游戏"""
        self.game = MinesweeperGame()
        self.game.init_game()
        self.game.is_running = True
        
        self.cell_buttons = [[None for _ in range(self.game.GRID_WIDTH)] for _ in range(self.game.GRID_HEIGHT)]
        
        self._render_board()
        self._update_flag_count()
        
        self._show_game_screen()
    
    def _restart_game(self, e):
        """重新开始游戏"""
        self._start_game(e)
    
    def _back_to_welcome(self, e):
        """返回欢迎界面"""
        self.game = None
        self._show_welcome_screen()
    
    def _exit_to_selector(self, e):
        """退出到游戏选择页面"""
        self.game = None
        if self.on_exit:
            self.on_exit()
    
    def _exit_game_during_play(self, e):
        """游戏进行中退出"""
        self.game = None
        self._exit_to_selector(e)
    
    def _update_flag_count(self):
        """更新旗子计数"""
        if self.game:
            questioned_count = sum(
                1 for row in range(self.game.GRID_HEIGHT)
                for col in range(self.game.GRID_WIDTH)
                if self.game.cell_states[row][col] == CellState.QUESTIONED
            )
            remaining = self.game.MINE_COUNT - questioned_count
            self.flag_count_text.value = f"剩余旗子: {remaining}"
            self.flag_count_text.update()
    
    def _render_board(self):
        """渲染游戏面板"""
        if not self.game or not self.cells_grid:
            return
        
        self.cells_grid.controls.clear()
        
        for row in range(self.game.GRID_HEIGHT):
            for col in range(self.game.GRID_WIDTH):
                btn = self._create_cell_button(row, col)
                self.cell_buttons[row][col] = btn
                self.cells_grid.controls.append(btn)
        
        self.cells_grid.update()
    
    def _create_cell_button(self, row: int, col: int) -> ft.Container:
        """创建单元格按钮"""
        container = ft.Container(
            width=38,
            height=38,
            alignment=ft.Alignment(0, 0),
            border=ft.Border.all(1, ft.Colors.BLACK12),
            on_click=lambda e, r=row, c=col: self._on_left_click(r, c),
            on_secondary_tap=lambda e, r=row, c=col: self._on_right_click(r, c)
        )
        
        text = ft.Text(
            size=16,
            weight=ft.FontWeight.BOLD
        )
        
        container.content = text
        self._update_cell_style(container, row, col)
        
        return container
    
    def _update_cell_style(self, container: ft.Container, row: int, col: int):
        """更新单元格样式"""
        if not self.game:
            return
        
        text = container.content
        cell_state = self.game.cell_states[row][col]
        is_mine = self.game.grid[row][col]
        adjacent_mines = self.game.get_adjacent_mine_count(row, col)
        
        if cell_state == CellState.QUESTIONED:
            container.bgcolor = ft.Colors.GREY_400
            text.value = "❓"
            text.color = ft.Colors.RED
        elif cell_state == CellState.HIDDEN:
            container.bgcolor = ft.Colors.GREY_500
            text.value = ""
            text.color = ft.Colors.TRANSPARENT
        elif cell_state == CellState.REVEALED:
            if is_mine:
                container.bgcolor = ft.Colors.RED
                text.value = "💣"
                text.color = ft.Colors.WHITE
            else:
                container.bgcolor = ft.Colors.GREY_200
                if adjacent_mines > 0:
                    text.value = str(adjacent_mines)
                    text.color = self._get_number_color(adjacent_mines)
                else:
                    text.value = ""
                    text.color = ft.Colors.TRANSPARENT
        
        container.update()
    
    def _get_number_color(self, count: int) -> str:
        """根据数字获取颜色"""
        colors = [
            ft.Colors.BLUE,
            ft.Colors.GREEN,
            ft.Colors.RED,
            ft.Colors.PURPLE,
            ft.Colors.MAROON,
            ft.Colors.TURQUOISE,
            ft.Colors.BLACK,
            ft.Colors.GREY
        ]
        return colors[count - 1] if count - 1 < len(colors) else ft.Colors.BLACK
    
    def _on_left_click(self, row: int, col: int):
        """左键点击事件"""
        if not self.game:
            return
        
        cell_state = self.game.cell_states[row][col]
        
        if cell_state == CellState.QUESTIONED or cell_state == CellState.REVEALED:
            return
        
        continue_game = self.game.left_click(row, col)
        
        self._render_board()
        
        if not continue_game:
            if self.game.won:
                self._show_game_over_screen(won=True)
            else:
                self._show_game_over_screen(won=False)
    
    def _on_right_click(self, row: int, col: int):
        """右键点击事件（标记问号）"""
        if not self.game:
            return
        
        cell_state = self.game.cell_states[row][col]
        
        if cell_state == CellState.REVEALED:
            return
        
        self.game.right_click(row, col)
        self._update_flag_count()
        
        if self.cell_buttons[row][col]:
            self._update_cell_style(self.cell_buttons[row][col], row, col)
