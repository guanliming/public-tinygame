import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import asyncio
from typing import Optional
import flet as ft
from games.tetris.game import TetrisGame


class TetrisGameUI:
    """俄罗斯方块游戏界面"""
    
    def __init__(self, on_exit=None):
        self.game: Optional[TetrisGame] = None
        self.page: Optional[ft.Page] = None
        self.game_task: Optional[asyncio.Task] = None
        self.on_exit = on_exit
        
        self.game_container: Optional[ft.Container] = None
        self.next_container: Optional[ft.Container] = None
        self.score_text: Optional[ft.Text] = None
        self.pause_text: Optional[ft.Text] = None
        self.game_over_score_text: Optional[ft.Text] = None
        self.controls_help_text: Optional[ft.Text] = None
        
        self.welcome_screen: Optional[ft.Container] = None
        self.game_screen: Optional[ft.Container] = None
        self.game_over_screen: Optional[ft.Container] = None
        
        self.start_button: Optional[ft.Button] = None
        self.restart_button: Optional[ft.Button] = None
        self.back_button: Optional[ft.Button] = None
        self.exit_button: Optional[ft.Button] = None
        self.game_exit_button: Optional[ft.Button] = None
        
        self.CELL_SIZE = 35
        self.NEXT_CELL_SIZE = 20
        self.fast_fall: bool = False
    
    def build(self, page: ft.Page):
        """构建并返回UI控件"""
        self.page = page
        page.on_keyboard_event = self._on_keyboard_event
        return self._build_ui()
    
    def show(self):
        """显示初始界面"""
        self._show_welcome_screen()
    
    def _build_ui(self):
        """构建UI"""
        self.score_text = ft.Text(
            "分数: 0 / 20",
            size=24,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        self.pause_text = ft.Text(
            "已暂停 - 按空格键继续",
            size=20,
            color=ft.Colors.YELLOW,
            weight=ft.FontWeight.BOLD,
            visible=False
        )
        
        self.game_over_score_text = ft.Text(
            "分数: 0 / 20",
            size=24,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        self.controls_help_text = ft.Text(
            "A/D 移动 | F 旋转 | S 加速下落 | 空格 暂停",
            size=14,
            color=ft.Colors.GREY_400
        )
        
        game_width = TetrisGame.GRID_WIDTH * self.CELL_SIZE
        game_height = TetrisGame.GRID_HEIGHT * self.CELL_SIZE
        
        self.game_container = ft.Container(
            width=game_width,
            height=game_height,
            bgcolor=ft.Colors.GREY_900,
            border=ft.Border.all(3, ft.Colors.GREY_600),
            content=ft.Stack([])
        )
        
        self.next_container = ft.Container(
            width=160,
            height=160,
            bgcolor=ft.Colors.GREY_900,
            border=ft.Border.all(2, ft.Colors.GREY_600),
            alignment=ft.Alignment(0, 0),
            content=ft.Stack([])
        )
        
        self.start_button = ft.Button(
            "开始游戏",
            on_click=self._start_game,
            width=200,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.CYAN_700,
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
                bgcolor=ft.Colors.CYAN_700,
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
                        "俄罗斯方块",
                        size=48,
                        color=ft.Colors.CYAN,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "经典俄罗斯方块游戏",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "A 键：向左移动",
                        size=16,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Text(
                        "D 键：向右移动",
                        size=16,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Text(
                        "F 键：旋转方块",
                        size=16,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Text(
                        "S 键：加速下落",
                        size=16,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Text(
                        "空格键：暂停/继续",
                        size=16,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "每消除一行得1分，达到20分即可获胜！",
                        size=16,
                        color=ft.Colors.CYAN_400
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
        
        next_preview = ft.Column(
            [
                ft.Text(
                    "下一个",
                    size=16,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                self.next_container
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        right_panel = ft.Column(
            [
                next_preview,
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                self.score_text,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                self.controls_help_text
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        self.game_screen = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [self.pause_text, ft.Container(expand=True), self.game_exit_button],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [self.game_container, ft.Container(width=30), right_panel],
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
        else:
            self.game_over_screen.content.controls[0].value = "游戏结束"
            self.game_over_screen.content.controls[0].color = ft.Colors.RED
        
        self.welcome_screen.update()
        self.game_screen.update()
        self.game_over_screen.update()
    
    def _start_game(self, e):
        """开始游戏"""
        self.game = TetrisGame()
        self.game.init_game()
        self.game.is_running = True
        
        self._update_score()
        self._render_game()
        self._render_next_piece()
        
        self._show_game_screen()
        
        if self.page:
            self.game_task = self.page.run_task(self._game_loop)
    
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
    
    def _update_score(self):
        """更新分数显示"""
        if self.game:
            score_text = f"分数: {self.game.score} / {self.game.WIN_SCORE}"
            self.score_text.value = score_text
            self.game_over_score_text.value = score_text
            self.score_text.update()
            self.game_over_score_text.update()
    
    def _int_to_hex_color(self, color_int: int) -> str:
        """将整数颜色转换为十六进制颜色字符串"""
        return f"#{color_int:06x}"
    
    def _render_game(self):
        """渲染游戏"""
        if not self.game or not self.game_container:
            return
        
        stack = self.game_container.content
        stack.controls.clear()
        
        for y in range(self.game.GRID_HEIGHT):
            for x in range(self.game.GRID_WIDTH):
                if self.game.grid[y][x] is not None:
                    color = self._int_to_hex_color(self.game.grid[y][x])
                    cell = ft.Container(
                        width=self.CELL_SIZE - 1,
                        height=self.CELL_SIZE - 1,
                        bgcolor=color,
                        left=x * self.CELL_SIZE,
                        top=y * self.CELL_SIZE,
                        border=ft.Border.all(1, ft.Colors.BLACK38)
                    )
                    stack.controls.append(cell)
        
        if self.game.current_piece and self.game.current_piece.absolute_blocks:
            color = self._int_to_hex_color(self.game.current_piece.color)
            for x, y in self.game.current_piece.absolute_blocks:
                if y >= 0:
                    cell = ft.Container(
                        width=self.CELL_SIZE - 1,
                        height=self.CELL_SIZE - 1,
                        bgcolor=color,
                        left=x * self.CELL_SIZE,
                        top=y * self.CELL_SIZE,
                        border=ft.Border.all(1, ft.Colors.BLACK38)
                    )
                    stack.controls.append(cell)
        
        self.game_container.update()
    
    def _render_next_piece(self):
        """渲染下一个方块预览"""
        if not self.game or not self.game.next_piece or not self.next_container:
            return
        
        stack = self.next_container.content
        stack.controls.clear()
        
        blocks = self.game.next_piece.blocks
        color = self._int_to_hex_color(self.game.next_piece.color)
        
        min_x = min(x for x, y in blocks)
        max_x = max(x for x, y in blocks)
        min_y = min(y for x, y in blocks)
        max_y = max(y for x, y in blocks)
        
        piece_width = (max_x - min_x + 1) * self.NEXT_CELL_SIZE
        piece_height = (max_y - min_y + 1) * self.NEXT_CELL_SIZE
        
        container_width = 160
        container_height = 160
        
        offset_x = (container_width - piece_width) // 2 - min_x * self.NEXT_CELL_SIZE
        offset_y = (container_height - piece_height) // 2 - min_y * self.NEXT_CELL_SIZE
        
        for x, y in blocks:
            cell = ft.Container(
                width=self.NEXT_CELL_SIZE - 1,
                height=self.NEXT_CELL_SIZE - 1,
                bgcolor=color,
                left=offset_x + x * self.NEXT_CELL_SIZE,
                top=offset_y + y * self.NEXT_CELL_SIZE,
                border=ft.Border.all(1, ft.Colors.BLACK38)
            )
            stack.controls.append(cell)
        
        self.next_container.update()
    
    def _update_pause_display(self):
        """更新暂停显示"""
        if self.game:
            self.pause_text.visible = self.game.is_paused
            self.pause_text.update()
    
    def _on_keyboard_event(self, e):
        """键盘事件处理"""
        if not self.game or not self.game.is_running:
            return
        
        key = e.key
        
        if key == " ":
            self.game.toggle_pause()
            self._update_pause_display()
            return
        
        if self.game.is_paused:
            return
        
        if key.lower() == "a":
            self.game.move_left()
            self._render_game()
        elif key.lower() == "d":
            self.game.move_right()
            self._render_game()
        elif key.lower() == "f":
            self.game.rotate()
            self._render_game()
        elif key.lower() == "s":
            self.fast_fall = True
    
    async def _game_loop(self):
        """游戏主循环"""
        if not self.game:
            return
        
        while self.game.is_running:
            if self.game.is_paused:
                await asyncio.sleep(0.1)
                continue
            
            speed = self.game.FAST_FALL_SPEED if self.fast_fall else self.game.FALL_SPEED
            await asyncio.sleep(speed)
            
            if not self.game.is_running:
                break
            
            if self.game.is_paused:
                continue
            
            moved = self.game.move_down()
            
            self._update_score()
            self._render_game()
            
            if not moved:
                self.fast_fall = False
                self._render_next_piece()
            
            if self.game.game_over:
                self._show_game_over_screen(won=False)
                break
            
            if self.game.won:
                self._show_game_over_screen(won=True)
                break
