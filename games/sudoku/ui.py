import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import asyncio
from typing import Optional, List, Tuple
import flet as ft
from games.sudoku.game import SudokuGame, CellState as SudokuCellState


class SudokuGameUI:
    """数独游戏界面"""
    
    CELL_SIZE = 50
    BOARD_PADDING = 10
    
    def __init__(self, on_exit=None):
        self.game: Optional[SudokuGame] = None
        self.page: Optional[ft.Page] = None
        self.game_task: Optional[asyncio.Task] = None
        self.on_exit = on_exit
        
        self.selected_cell: Optional[Tuple[int, int]] = None
        self.cell_containers: List[List[Optional[ft.Container]]] = []
        self.number_buttons: List[Optional[ft.Button]] = []
        
        self.time_text: Optional[ft.Text] = None
        self.failures_text: Optional[ft.Text] = None
        self.error_tip: Optional[ft.Text] = None
        self.game_over_message: Optional[ft.Text] = None
        
        self.welcome_screen: Optional[ft.Container] = None
        self.game_screen: Optional[ft.Container] = None
        self.game_over_screen: Optional[ft.Container] = None
        
        self.start_button: Optional[ft.Button] = None
        self.restart_button: Optional[ft.Button] = None
        self.back_button: Optional[ft.Button] = None
        self.exit_button: Optional[ft.Button] = None
        self.game_exit_button: Optional[ft.Button] = None
        self.clear_button: Optional[ft.Button] = None
    
    def build(self, page: ft.Page):
        """构建并返回UI控件"""
        self.page = page
        return self._build_ui()
    
    def show(self):
        """显示初始界面"""
        self._show_welcome_screen()
    
    def _build_ui(self):
        """构建UI"""
        self.time_text = ft.Text(
            "时间: 00:00",
            size=20,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        self.failures_text = ft.Text(
            "失败: 0 / 8",
            size=20,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        self.error_tip = ft.Text(
            "",
            size=18,
            color=ft.Colors.RED,
            weight=ft.FontWeight.BOLD,
            visible=False
        )
        
        self.game_over_message = ft.Text(
            "",
            size=26,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        self.start_button = ft.Button(
            "开始游戏",
            on_click=self._start_game,
            width=200,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.DEEP_ORANGE_700,
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
                bgcolor=ft.Colors.DEEP_ORANGE_700,
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
        
        self.clear_button = ft.Button(
            "清除",
            on_click=self._clear_selected_cell,
            width=100,
            height=40,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREY_700,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD)
            )
        )
        
        self.welcome_screen = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "🧩 数独游戏",
                        size=48,
                        color=ft.Colors.DEEP_ORANGE,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "棋盘大小: 9 × 9",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "规则: 每行、每列、每个3×3宫格中",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "数字1-9只能出现一次",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "点击空格子选中，再点击下方数字填入",
                        size=16,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Text(
                        "填错有提示，失败超过8次游戏结束",
                        size=16,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Text(
                        "每次游戏随机显示35个数字",
                        size=16,
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
                        [self.time_text, ft.Container(expand=True), self.failures_text, ft.Container(expand=True), self.game_exit_button],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [self.error_tip],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    ft.Container(
                        content=ft.Stack([]),
                        expand=True,
                        alignment=ft.Alignment(0, 0)
                    ),
                    ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
                    self._build_number_pad()
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
                    self.game_over_message,
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
    
    def _build_number_pad(self) -> ft.Container:
        """构建数字选择面板"""
        self.number_buttons = []
        
        number_row = []
        for num in range(1, 10):
            btn = ft.Button(
                str(num),
                on_click=lambda e, n=num: self._on_number_click(n),
                width=self.CELL_SIZE,
                height=self.CELL_SIZE,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_GREY_700,
                    color=ft.Colors.WHITE,
                    text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)
                )
            )
            self.number_buttons.append(btn)
            number_row.append(btn)
        
        number_row.append(self.clear_button)
        
        return ft.Container(
            content=ft.Row(
                number_row,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8
            ),
            padding=10
        )
    
    def _show_welcome_screen(self):
        """显示欢迎界面"""
        self.welcome_screen.visible = True
        self.game_screen.visible = False
        self.game_over_screen.visible = False
        
        self.welcome_screen.update()
        self.game_screen.update()
        self.game_over_screen.update()
    
    def _show_game_screen(self):
        """显示游戏界面"""
        self.welcome_screen.visible = False
        self.game_screen.visible = True
        self.game_over_screen.visible = False
        
        self.welcome_screen.update()
        self.game_screen.update()
        self.game_over_screen.update()
    
    def _show_game_over_screen(self, won: bool = False):
        """显示游戏结束界面"""
        self.welcome_screen.visible = False
        self.game_screen.visible = False
        self.game_over_screen.visible = True
        
        if won:
            self.game_over_screen.content.controls[0].value = "🎉 恭喜获胜！"
            self.game_over_screen.content.controls[0].color = ft.Colors.GREEN
            self.game_over_message.value = f"用时: {self.game.get_time_display()} | 失败次数: {self.game.failure_count}"
        else:
            self.game_over_screen.content.controls[0].value = "游戏结束"
            self.game_over_screen.content.controls[0].color = ft.Colors.RED
            self.game_over_message.value = f"失败次数: {self.game.failure_count} / {self.game.MAX_FAILURES}"
        
        self.welcome_screen.update()
        self.game_screen.update()
        self.game_over_screen.update()
    
    def _start_game(self, e):
        """开始游戏"""
        self.game = SudokuGame()
        self.game.init_game()
        self.game.is_running = True
        self.game.start()
        
        self.selected_cell = None
        self._build_game_board()
        self._update_time_display()
        self._update_failures_display()
        self._hide_error_tip()
        
        self._show_game_screen()
        
        if self.page:
            self.game_task = self.page.run_task(self._game_loop)
    
    def _build_game_board(self):
        """构建数独棋盘"""
        if not self.game or not self.game_screen:
            return
        
        board_container = self.game_screen.content.controls[4]
        stack = board_container.content
        stack.controls.clear()
        
        board_size = self.game.GRID_SIZE * self.CELL_SIZE + 2
        total_width = board_size
        total_height = board_size
        
        board_bg = ft.Container(
            width=total_width,
            height=total_height,
            bgcolor=ft.Colors.AMBER_100,
            border=ft.Border.all(3, ft.Colors.BROWN_800),
            border_radius=5
        )
        stack.controls.append(board_bg)
        
        self.cell_containers = [[None for _ in range(self.game.GRID_SIZE)] for _ in range(self.game.GRID_SIZE)]
        
        for i in range(self.game.GRID_SIZE):
            for j in range(self.game.GRID_SIZE):
                is_right_border = (j + 1) % self.game.BOX_SIZE == 0 and j < self.game.GRID_SIZE - 1
                is_bottom_border = (i + 1) % self.game.BOX_SIZE == 0 and i < self.game.GRID_SIZE - 1
                
                border = ft.Border(
                    top=ft.BorderSide(1, ft.Colors.BROWN_400),
                    bottom=ft.BorderSide(3 if is_bottom_border else 1, ft.Colors.BROWN_400 if not is_bottom_border else ft.Colors.BROWN_800),
                    left=ft.BorderSide(1, ft.Colors.BROWN_400),
                    right=ft.BorderSide(3 if is_right_border else 1, ft.Colors.BROWN_400 if not is_right_border else ft.Colors.BROWN_800)
                )
                
                cell_value = self.game.puzzle[i][j]
                cell_state = self.game.cell_states[i][j]
                
                is_fixed = cell_state == SudokuCellState.FIXED
                
                cell_content = None
                if cell_value != 0:
                    cell_content = ft.Text(
                        str(cell_value),
                        size=28,
                        color=ft.Colors.BLACK if is_fixed else ft.Colors.BLUE_700,
                        weight=ft.FontWeight.BOLD
                    )
                
                cell = ft.Container(
                    width=self.CELL_SIZE,
                    height=self.CELL_SIZE,
                    bgcolor=ft.Colors.AMBER_50,
                    border=border,
                    alignment=ft.Alignment(0, 0),
                    content=cell_content,
                    on_click=lambda e, row=i, col=j: self._on_cell_click(row, col),
                    data={"row": i, "col": j}
                )
                
                cell_left = j * self.CELL_SIZE + 1
                cell_top = i * self.CELL_SIZE + 1
                
                cell_wrapper = ft.Container(
                    content=cell,
                    left=cell_left,
                    top=cell_top
                )
                
                self.cell_containers[i][j] = cell
                stack.controls.append(cell_wrapper)
        
        board_container.update()
    
    def _on_cell_click(self, row: int, col: int):
        """格子点击事件"""
        if not self.game or not self.game.is_running:
            return
        
        if self.game.cell_states[row][col] == SudokuCellState.FIXED:
            return
        
        self._hide_error_tip()
        
        if self.selected_cell:
            old_row, old_col = self.selected_cell
            self._update_cell_style(old_row, old_col, selected=False)
        
        self.selected_cell = (row, col)
        self._update_cell_style(row, col, selected=True)
    
    def _update_cell_style(self, row: int, col: int, selected: bool = False):
        """更新格子样式"""
        if not self.cell_containers or not self.cell_containers[row][col]:
            return
        
        cell = self.cell_containers[row][col]
        state = self.game.cell_states[row][col]
        
        if state == SudokuCellState.FILLED_WRONG:
            cell.bgcolor = ft.Colors.RED_100
        elif state == SudokuCellState.FILLED_CORRECT:
            cell.bgcolor = ft.Colors.GREEN_100
        elif selected:
            cell.bgcolor = ft.Colors.LIGHT_BLUE_200
        else:
            cell.bgcolor = ft.Colors.AMBER_50
        
        cell.update()
    
    def _on_number_click(self, num: int):
        """数字按钮点击事件"""
        if not self.game or not self.game.is_running:
            return
        
        if not self.selected_cell:
            return
        
        row, col = self.selected_cell
        
        continue_game = self.game.make_move(row, col, num)
        
        self._update_cell_display(row, col)
        self._update_failures_display()
        
        if self.game.cell_states[row][col] == SudokuCellState.FILLED_WRONG:
            self._show_error_tip("填入错误！")
            self._update_cell_style(row, col, selected=True)
            self._hide_error_tip_delayed()
        else:
            self._update_cell_style(row, col, selected=True)
        
        if not continue_game:
            if self.game.won:
                if self.game_task and not self.game_task.done():
                    self.game_task.cancel()
                self._show_game_over_screen(won=True)
            else:
                if self.game_task and not self.game_task.done():
                    self.game_task.cancel()
                self._show_game_over_screen(won=False)
    
    def _clear_selected_cell(self, e):
        """清除选中格子的数字"""
        if not self.game or not self.game.is_running:
            return
        
        if not self.selected_cell:
            return
        
        row, col = self.selected_cell
        
        cleared = self.game.clear_cell(row, col)
        
        if cleared:
            self._hide_error_tip()
            self._update_cell_display(row, col)
            self._update_cell_style(row, col, selected=True)
    
    def _update_cell_display(self, row: int, col: int):
        """更新格子显示"""
        if not self.cell_containers or not self.cell_containers[row][col]:
            return
        
        cell = self.cell_containers[row][col]
        value = self.game.puzzle[row][col]
        state = self.game.cell_states[row][col]
        
        if value != 0:
            is_fixed = state == SudokuCellState.FIXED
            is_wrong = state == SudokuCellState.FILLED_WRONG
            
            text_color = ft.Colors.BLACK if is_fixed else (ft.Colors.RED if is_wrong else ft.Colors.BLUE_700)
            
            cell.content = ft.Text(
                str(value),
                size=28,
                color=text_color,
                weight=ft.FontWeight.BOLD
            )
        else:
            cell.content = None
        
        cell.update()
    
    def _show_error_tip(self, message: str):
        """显示错误提示"""
        if self.error_tip:
            self.error_tip.value = message
            self.error_tip.visible = True
            self.error_tip.update()
    
    def _hide_error_tip(self):
        """隐藏错误提示"""
        if self.error_tip:
            self.error_tip.visible = False
            self.error_tip.update()
    
    def _hide_error_tip_delayed(self):
        """延迟隐藏错误提示"""
        if self.page:
            self.page.run_task(self._hide_error_tip_after_delay)
    
    async def _hide_error_tip_after_delay(self):
        """异步延迟隐藏错误提示"""
        await asyncio.sleep(2)
        self._hide_error_tip()
    
    def _update_time_display(self):
        """更新时间显示"""
        if self.game and self.time_text:
            self.game.update_time()
            self.time_text.value = f"时间: {self.game.get_time_display()}"
            self.time_text.update()
    
    def _update_failures_display(self):
        """更新失败次数显示"""
        if self.game and self.failures_text:
            self.failures_text.value = f"失败: {self.game.failure_count} / {self.game.MAX_FAILURES}"
            
            if self.game.failure_count >= 6:
                self.failures_text.color = ft.Colors.RED
            elif self.game.failure_count >= 4:
                self.failures_text.color = ft.Colors.ORANGE
            else:
                self.failures_text.color = ft.Colors.WHITE
            
            self.failures_text.update()
    
    def _restart_game(self, e):
        """重新开始游戏"""
        if self.game_task and not self.game_task.done():
            self.game_task.cancel()
        
        self._start_game(e)
    
    def _back_to_welcome(self, e):
        """返回欢迎界面"""
        if self.game_task and not self.game_task.done():
            self.game_task.cancel()
        
        self.game = None
        self._show_welcome_screen()
    
    def _exit_to_selector(self, e):
        """退出到游戏选择页面"""
        if self.game_task and not self.game_task.done():
            self.game_task.cancel()
        
        self.game = None
        if self.on_exit:
            self.on_exit()
    
    def _exit_game_during_play(self, e):
        """游戏进行中退出"""
        if self.game_task and not self.game_task.done():
            self.game_task.cancel()
        
        self.game = None
        self._exit_to_selector(e)
    
    async def _game_loop(self):
        """游戏主循环"""
        if not self.game:
            return
        
        while self.game.is_running:
            self._update_time_display()
            await asyncio.sleep(1)
