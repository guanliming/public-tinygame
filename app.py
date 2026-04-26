import sys
import asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import flet as ft
from typing import Optional, List
from games.doudizhu import (
    DoudizhuGame, DoudizhuPlayer, PlayerRole, DoudizhuCard,
    get_card_type, compare_cards, CardType
)
from games.snake import SnakeGame, Direction, Position
from games.twentyone import TwentyOneGame
from games.minesweeper import MinesweeperGame, CellState
from games.whackamole import WhackAMoleGame, HoleState
from games.gomoku import GomokuGame, PlayerColor
from games.tetris import TetrisGame


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


class TwentyOneGameUI:
    """21点游戏界面"""
    
    def __init__(self, on_exit=None):
        self.game: Optional[TwentyOneGame] = None
        self.page: Optional[ft.Page] = None
        self.on_exit = on_exit
        
        self.numbers_text: Optional[ft.Text] = None
        self.solution_text: Optional[ft.Text] = None
        self.message_text: Optional[ft.Text] = None
        
        self.welcome_screen: Optional[ft.Container] = None
        self.game_screen: Optional[ft.Container] = None
        
        self.start_button: Optional[ft.Button] = None
        self.next_button: Optional[ft.Button] = None
        self.solution_button: Optional[ft.Button] = None
        self.exit_button: Optional[ft.Button] = None
        self.game_exit_button: Optional[ft.Button] = None
    
    def build(self, page: ft.Page):
        """构建并返回UI控件"""
        self.page = page
        return self._build_ui()
    
    def show(self):
        """显示初始界面"""
        self._show_welcome_screen()
    
    def _build_ui(self):
        """构建UI"""
        self.numbers_text = ft.Text(
            "数字: ",
            size=36,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        self.solution_text = ft.Text(
            "",
            size=24,
            color=ft.Colors.YELLOW,
            weight=ft.FontWeight.BOLD
        )
        
        self.message_text = ft.Text(
            "",
            size=18,
            color=ft.Colors.GREY_400,
            weight=ft.FontWeight.BOLD
        )
        
        self.start_button = ft.Button(
            "开始游戏",
            on_click=self._start_game,
            width=200,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
            )
        )
        
        self.next_button = ft.Button(
            "下一题",
            on_click=self._next_question,
            width=150,
            height=50,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
            )
        )
        
        self.solution_button = ft.Button(
            "解答",
            on_click=self._show_solution,
            width=150,
            height=50,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.ORANGE,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
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
                        "21点游戏",
                        size=48,
                        color=ft.Colors.GREEN,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "使用 + - * / 将四个数字计算出 21",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "点击\"解答\"按钮查看计算方式",
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
                        [ft.Container(expand=True), self.game_exit_button],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "请用以下数字计算出 21:",
                        size=20,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    self.numbers_text,
                    ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                    self.solution_text,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self.message_text,
                    ft.Divider(height=50, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [self.next_button, self.solution_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=30
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
        
        self.welcome_screen.update()
        self.game_screen.update()
    
    def _show_game_screen(self):
        """显示游戏界面"""
        self.welcome_screen.visible = False
        self.game_screen.visible = True
        
        self.welcome_screen.update()
        self.game_screen.update()
    
    def _start_game(self, e):
        """开始游戏"""
        self.game = TwentyOneGame()
        self.game.init_game()
        self.game.is_running = True
        self.game.next_question()
        
        self._update_numbers()
        self.solution_text.value = ""
        self.message_text.value = ""
        
        self._show_game_screen()
    
    def _next_question(self, e):
        """下一题"""
        if self.game:
            self.game.next_question()
            self._update_numbers()
            self.solution_text.value = ""
            self.message_text.value = ""
            self.solution_text.update()
            self.message_text.update()
    
    def _show_solution(self, e):
        """显示解答"""
        if self.game and self.game.solution:
            solution = self.game.solution
            self.solution_text.value = f"解法: {solution} = 21"
            self.message_text.value = "点击\"下一题\"继续挑战"
        else:
            self.solution_text.value = "暂无解法"
            self.message_text.value = ""
        self.solution_text.update()
        self.message_text.update()
    
    def _update_numbers(self):
        """更新数字显示"""
        if self.game and self.game.numbers:
            nums = "  ".join(str(n) for n in self.game.numbers)
            self.numbers_text.value = nums
            self.numbers_text.update()
    
    def _exit_to_selector(self, e):
        """退出到游戏选择页面"""
        self.game = None
        if self.on_exit:
            self.on_exit()
    
    def _exit_game_during_play(self, e):
        """游戏进行中退出"""
        self.game = None
        self._exit_to_selector(e)


class SnakeGameUI:
    """贪吃蛇游戏界面"""
    
    def __init__(self, on_exit=None):
        self.game: Optional[SnakeGame] = None
        self.page: Optional[ft.Page] = None
        self.game_task: Optional[asyncio.Task] = None
        self.on_exit = on_exit
        
        self.game_container: Optional[ft.Container] = None
        self.game_score_text: Optional[ft.Text] = None
        self.game_over_score_text: Optional[ft.Text] = None
        self.message_text: Optional[ft.Text] = None
        
        self.welcome_screen: Optional[ft.Container] = None
        self.game_screen: Optional[ft.Container] = None
        self.game_over_screen: Optional[ft.Container] = None
        
        self.start_button: Optional[ft.Button] = None
        self.restart_button: Optional[ft.Button] = None
        self.back_button: Optional[ft.Button] = None
        self.exit_button: Optional[ft.Button] = None
        self.game_exit_button: Optional[ft.Button] = None
    
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
        self.game_score_text = ft.Text(
            "分数: 0",
            size=24,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        self.game_over_score_text = ft.Text(
            "分数: 0",
            size=24,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        self.message_text = ft.Text(
            "",
            size=18,
            color=ft.Colors.RED,
            weight=ft.FontWeight.BOLD
        )
        
        game_width = 700
        game_height = 500
        cell_size = 10
        
        self.game_container = ft.Container(
            width=game_width,
            height=game_height,
            bgcolor=ft.Colors.GREY_900,
            border=ft.Border.all(2, ft.Colors.WHITE),
            content=ft.Stack([])
        )
        
        self.start_button = ft.Button(
            "开始游戏",
            on_click=self._start_game,
            width=200,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN,
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
                bgcolor=ft.Colors.GREEN,
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
                        "贪吃蛇游戏",
                        size=48,
                        color=ft.Colors.GREEN,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "使用 WASD 键控制方向",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "吃到 50 个豆子即可获胜",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "头部碰到身体则游戏结束",
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
                        [self.game_score_text, ft.Container(expand=True), self.game_exit_button],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [self.game_container],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [self.message_text],
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
            self.game_over_screen.content.controls[0].value = "恭喜获胜！"
            self.game_over_screen.content.controls[0].color = ft.Colors.GREEN
        else:
            self.game_over_screen.content.controls[0].value = "游戏结束"
            self.game_over_screen.content.controls[0].color = ft.Colors.RED
        
        self.welcome_screen.update()
        self.game_screen.update()
        self.game_over_screen.update()
    
    def _start_game(self, e):
        """开始游戏"""
        self.game = SnakeGame()
        self.game.init_game()
        self.game.is_running = True
        
        self._update_score()
        self._render_game()
        
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
            score_text = f"分数: {self.game.score}"
            self.game_score_text.value = score_text
            self.game_over_score_text.value = score_text
            self.game_score_text.update()
            self.game_over_score_text.update()
    
    def _render_game(self):
        """渲染游戏"""
        if not self.game or not self.game_container:
            return
        
        stack = self.game_container.content
        stack.controls.clear()
        
        cell_size = 10
        
        for pos in self.game.snake:
            x = pos.x * cell_size
            y = pos.y * cell_size
            
            cell = ft.Container(
                width=cell_size,
                height=cell_size,
                bgcolor=ft.Colors.GREEN,
                left=x,
                top=y
            )
            stack.controls.append(cell)
        
        if self.game.snake:
            head = self.game.snake[0]
            x = head.x * cell_size
            y = head.y * cell_size
            
            head_cell = ft.Container(
                width=cell_size,
                height=cell_size,
                bgcolor=ft.Colors.LIGHT_GREEN,
                left=x,
                top=y
            )
            stack.controls.append(head_cell)
        
        for food in self.game.foods:
            x = food.x * cell_size
            y = food.y * cell_size
            
            food_cell = ft.Container(
                width=cell_size,
                height=cell_size,
                bgcolor=ft.Colors.RED,
                left=x,
                top=y
            )
            stack.controls.append(food_cell)
        
        self.game_container.update()
    
    def _on_keyboard_event(self, e):
        """键盘事件处理"""
        if not self.game or not self.game.is_running:
            return
        
        key = e.key.lower()
        
        if key == 'w':
            self.game.set_direction(Direction.UP)
        elif key == 's':
            self.game.set_direction(Direction.DOWN)
        elif key == 'a':
            self.game.set_direction(Direction.LEFT)
        elif key == 'd':
            self.game.set_direction(Direction.RIGHT)
    
    async def _game_loop(self):
        """游戏循环"""
        if not self.game:
            return
        
        while self.game.is_running:
            await asyncio.sleep(self.game.MOVE_SPEED)
            
            if not self.game.is_running:
                break
            
            continue_game = self.game.move()
            
            self._update_score()
            self._render_game()
            
            if not continue_game:
                if self.game.won:
                    self._show_game_over_screen(won=True)
                else:
                    self._show_game_over_screen(won=False)
                break


class CardWidget(ft.Container):
    """卡牌组件"""
    
    def __init__(self, card: DoudizhuCard, on_click=None, selected: bool = False):
        super().__init__()
        self.card = card
        self.selected = selected
        self.on_click_callback = on_click
        
        self.width = 60
        self.height = 90
        self.border_radius = 8
        self.padding = 5
        self.margin = ft.margin.only(top=45, bottom=0)
        self.animate = ft.Animation(200, ft.AnimationCurve.EASE_OUT)
        
        self._update_style()
        
    def _get_card_color(self):
        """获取卡牌颜色"""
        if self.card.is_joker():
            if self.card.value == 16:
                return ft.Colors.GREEN
            return ft.Colors.RED
        if self.card.suit and self.card.suit.value in ("♥", "♦"):
            return ft.Colors.RED
        return ft.Colors.BLACK
    
    def _get_card_display(self):
        """获取卡牌显示内容"""
        value_map = {
            3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
            8: "8", 9: "9", 10: "10", 11: "J", 12: "Q",
            13: "K", 14: "A", 15: "2", 16: "小", 17: "大"
        }
        value = value_map.get(self.card.value, str(self.card.value))
        
        if self.card.is_joker():
            return f"{value}\n王"
        
        suit = self.card.suit.value if self.card.suit else ""
        return f"{suit}\n{value}"
    
    def _update_style(self):
        """更新样式"""
        color = self._get_card_color()
        display_text = self._get_card_display()
        
        self.bgcolor = ft.Colors.WHITE
        self.border = ft.Border.all(2, ft.Colors.BLACK12)
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=3,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 2)
        )
        
        if self.selected:
            self.margin = ft.margin.only(top=0, bottom=45)
            self.border = ft.Border.all(3, ft.Colors.BLUE)
        else:
            self.margin = ft.margin.only(top=45, bottom=0)
        
        self.content = ft.Column(
            [
                ft.Text(
                    display_text,
                    size=16,
                    color=color,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        self.on_click = self._on_click
    
    def _on_click(self, e):
        """点击事件"""
        self.selected = not self.selected
        self._update_style()
        self.update()
        if self.on_click_callback:
            self.on_click_callback(self)


class PlayerInfoWidget(ft.Column):
    """玩家信息组件"""
    
    def __init__(self, player: DoudizhuPlayer, is_current: bool = False):
        super().__init__()
        self.player = player
        self.is_current = is_current
        
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 5
        
        self._build_widget()
    
    def _build_widget(self):
        """构建组件"""
        avatar_color = ft.Colors.BLUE_GREY_400
        if self.player.role == PlayerRole.DIZHU:
            avatar_color = ft.Colors.ORANGE
        
        border_color = ft.Colors.TRANSPARENT
        if self.is_current:
            border_color = ft.Colors.GREEN
        
        self.controls = [
            ft.Container(
                content=ft.Icon(
                    ft.Icons.PERSON,
                    size=40,
                    color=ft.Colors.WHITE
                ),
                width=60,
                height=60,
                bgcolor=avatar_color,
                border_radius=30,
                border=ft.Border.all(3, border_color),
                alignment=ft.Alignment(0, 0)
            ),
            ft.Row(
                [
                    ft.Text(
                        self.player.name,
                        size=14,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(
                        f"({self.player.role.value})",
                        size=12,
                        color=ft.Colors.ORANGE if self.player.role == PlayerRole.DIZHU else ft.Colors.GREY
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Text(
                f"手牌: {self.player.get_hand_count()} 张",
                size=12,
                color=ft.Colors.GREY_600
            )
        ]
    
    def update_info(self):
        """更新信息"""
        self._build_widget()
        self.update()


class PlayedCardsWidget(ft.Column):
    """玩家出牌展示组件"""
    
    def __init__(self, player_index: int):
        super().__init__()
        self.player_index = player_index
        self.played_cards: List[DoudizhuCard] = []
        self.pass_text: Optional[ft.Text] = None
        self.cards_row: Optional[ft.Row] = None
        self.opacity = 1.0
        
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 5
        
        self._build_widget()
    
    def _build_widget(self):
        """构建组件"""
        self.pass_text = ft.Text(
            "要不起",
            size=16,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD,
            visible=False
        )
        
        self.cards_row = ft.Row(
            [],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=2
        )
        
        self.controls = [self.pass_text, self.cards_row]
    
    def show_played_cards(self, cards: List[DoudizhuCard]):
        """显示出的牌"""
        self.played_cards = cards
        self.pass_text.visible = False
        
        self.cards_row.controls.clear()
        for card in cards:
            card_widget = CardWidget(card)
            card_widget.width = 45
            card_widget.height = 68
            card_widget.margin = ft.margin.all(0)
            self.cards_row.controls.append(card_widget)
        
        self.opacity = 1.0
        self.update()
    
    def show_pass(self):
        """显示要不起"""
        self.played_cards = []
        self.pass_text.visible = True
        self.cards_row.controls.clear()
        self.opacity = 1.0
        self.update()
    
    def clear(self):
        """清空显示"""
        self.played_cards = []
        self.pass_text.visible = False
        self.cards_row.controls.clear()
        self.opacity = 1.0
        self.update()
    
    def fade_out(self, duration_ms: int = 1000):
        """淡出效果"""
        pass


class DoudizhuGameUI:
    """斗地主游戏界面"""
    
    def __init__(self, on_exit=None):
        self.game: Optional[DoudizhuGame] = None
        self.player_index = 0
        self.selected_cards: List[DoudizhuCard] = []
        self.card_widgets: List[CardWidget] = []
        self.on_exit = on_exit
        
        self.page: Optional[ft.Page] = None
        
        self.player_info_widgets: List[PlayerInfoWidget] = []
        self.played_cards_widgets: List[PlayedCardsWidget] = []
        
        self.hand_cards_row: Optional[ft.Row] = None
        self.message_text: Optional[ft.Text] = None
        self.bottom_cards_row: Optional[ft.Row] = None
        
        self.start_button: Optional[ft.Button] = None
        self.play_button: Optional[ft.Button] = None
        self.pass_button: Optional[ft.Button] = None
        self.exit_button: Optional[ft.Button] = None
    
    def build(self, page: ft.Page):
        """构建并返回UI控件"""
        self.page = page
        return self._build_ui()
    
    def show(self):
        """显示初始界面"""
        self._show_message("欢迎来到斗地主！点击\"开始游戏\"按钮开始游戏。")
    
    def _build_ui(self):
        """构建UI - 三人斗地主布局：我在底部，对手在左边和顶部"""
        self.start_button = ft.Button(
            "开始游戏",
            on_click=self._start_game,
            width=150,
            height=50,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
            )
        )
        
        self.play_button = ft.Button(
            "出牌",
            on_click=self._play_cards,
            width=100,
            height=50,
            disabled=True,
            visible=False,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD)
            )
        )
        
        self.pass_button = ft.Button(
            "不要",
            on_click=self._pass_turn,
            width=100,
            height=50,
            disabled=True,
            visible=False,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.RED,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD)
            )
        )
        
        self.exit_button = ft.Button(
            "退出",
            on_click=self._exit_game,
            width=100,
            height=50,
            visible=False,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREY,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD)
            )
        )
        
        self.message_text = ft.Text(
            "",
            size=16,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        
        self.bottom_cards_row = ft.Row(
            [],
            alignment=ft.MainAxisAlignment.START,
            spacing=2
        )
        
        self.hand_cards_row = ft.Row(
            [],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=2,
            wrap=True
        )
        
        for i in range(3):
            widget = PlayerInfoWidget(
                DoudizhuPlayer(i, f"玩家{i+1}"),
                is_current=False
            )
            self.player_info_widgets.append(widget)
            played_widget = PlayedCardsWidget(i)
            self.played_cards_widgets.append(played_widget)
        
        top_left_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text("底牌:", size=14, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                    self.bottom_cards_row
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START
            ),
            width=150,
            alignment=ft.Alignment(-1, -1)
        )
        
        north_player_container = ft.Column(
            [
                self.player_info_widgets[1],
                ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                self.played_cards_widgets[1]
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        west_player_container = ft.Column(
            [
                self.player_info_widgets[2],
                ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                self.played_cards_widgets[2]
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=1
        )
        
        center_container = ft.Column(
            [
                self.message_text,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    [self.start_button, self.play_button, self.pass_button, self.exit_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=2
        )
        
        south_player_container = ft.Column(
            [
                self.played_cards_widgets[0],
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                self.player_info_widgets[0],
                ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                ft.Text("我的手牌:", size=14, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                self.hand_cards_row
            ],
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        top_row = ft.Row(
            [
                top_left_container,
                ft.Container(expand=True),
                north_player_container,
                ft.Container(expand=True),
                ft.Container(width=150)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        middle_row = ft.Row(
            [
                west_player_container,
                center_container
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        bottom_row = ft.Row(
            [south_player_container],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        return ft.Column(
            [
                top_row,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                middle_row,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                bottom_row
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    
    def _show_message(self, message: str):
        """显示消息"""
        if self.message_text:
            self.message_text.value = message
            self.message_text.update()
    
    def _update_player_info(self):
        """更新玩家信息"""
        if not self.game:
            return
        
        for i, player in enumerate(self.game.players):
            widget = self.player_info_widgets[i]
            widget.player = player
            widget.is_current = player.is_current
            widget.update_info()
    
    def _update_hand_cards(self):
        """更新玩家手牌"""
        if not self.game:
            return
        
        player = self.game.players[self.player_index]
        self.card_widgets = []
        self.selected_cards = []
        
        self.hand_cards_row.controls.clear()
        
        for card in player.hand:
            card_widget = CardWidget(card, on_click=self._on_card_click)
            self.card_widgets.append(card_widget)
            self.hand_cards_row.controls.append(card_widget)
        
        self.hand_cards_row.update()
    
    def _show_played_cards_for_player(self, player: DoudizhuPlayer, cards: List[DoudizhuCard]):
        """在对应玩家的出牌区域显示牌"""
        player_idx = player.player_id
        if 0 <= player_idx < len(self.played_cards_widgets):
            self.played_cards_widgets[player_idx].show_played_cards(cards)
    
    def _show_pass_for_player(self, player: DoudizhuPlayer):
        """在对应玩家的出牌区域显示要不起"""
        player_idx = player.player_id
        if 0 <= player_idx < len(self.played_cards_widgets):
            self.played_cards_widgets[player_idx].show_pass()
    
    def _clear_all_played_cards(self):
        """清除所有玩家的出牌显示"""
        for widget in self.played_cards_widgets:
            widget.clear()
    
    def _update_last_played_cards(self):
        """更新最后出牌显示（已废弃，使用_show_played_cards_for_player代替）"""
        pass
    
    def _update_bottom_cards(self):
        """更新底牌显示"""
        if not self.game:
            return
        
        self.bottom_cards_row.controls.clear()
        
        for card in self.game.bottom_cards:
            card_widget = CardWidget(card)
            card_widget.width = 40
            card_widget.height = 60
            self.bottom_cards_row.controls.append(card_widget)
        
        self.bottom_cards_row.update()
    
    def _on_card_click(self, card_widget: CardWidget):
        """卡牌点击事件"""
        if card_widget.selected:
            if card_widget.card not in self.selected_cards:
                self.selected_cards.append(card_widget.card)
        else:
            if card_widget.card in self.selected_cards:
                self.selected_cards.remove(card_widget.card)
    
    def _start_game(self, e):
        """开始游戏"""
        self.game = DoudizhuGame()
        
        self.game.players = [
            DoudizhuPlayer(0, "我"),
            DoudizhuPlayer(1, "机器人1"),
            DoudizhuPlayer(2, "机器人2")
        ]
        
        self.game.init_game()
        self.game.shuffle()
        self.game.deal()
        self.game.is_running = True
        
        self.player_index = 0
        self.game.set_dizhu(0)
        
        self._update_player_info()
        self._update_hand_cards()
        self._clear_all_played_cards()
        self._update_bottom_cards()
        
        self.start_button.visible = False
        self.exit_button.visible = True
        self.play_button.disabled = False
        self.play_button.visible = True
        
        self._update_buttons()
        
        self._show_message(f"游戏开始！你是地主。请选择牌并点击\"出牌\"。")
    
    def _update_buttons(self):
        """更新按钮状态"""
        if not self.game:
            return
        
        current_player = self.game.get_current_player()
        
        if current_player == self.game.players[self.player_index]:
            self.play_button.disabled = False
            self.play_button.visible = True
            
            if self.game.last_played_cards and self.game.last_played_player != current_player:
                self.pass_button.disabled = False
                self.pass_button.visible = True
            else:
                self.pass_button.disabled = True
                self.pass_button.visible = False
        else:
            self.play_button.disabled = True
            self.pass_button.disabled = True
            self.pass_button.visible = False
        
        self.play_button.update()
        self.pass_button.update()
        self.start_button.update()
        if self.exit_button:
            self.exit_button.update()
    
    def _exit_game(self, e):
        """退出游戏，回到开始界面"""
        self.game = None
        self.selected_cards = []
        self.card_widgets = []
        
        if self.on_exit:
            self.on_exit()
        else:
            self.start_button.visible = True
            self.start_button.disabled = False
            self.exit_button.visible = False
            self.play_button.visible = False
            self.play_button.disabled = True
            self.pass_button.visible = False
            self.pass_button.disabled = True
            
            self.hand_cards_row.controls.clear()
            self.bottom_cards_row.controls.clear()
            self._clear_all_played_cards()
            
            for widget in self.player_info_widgets:
                widget.player = DoudizhuPlayer(widget.player.player_id, f"玩家{widget.player.player_id + 1}")
                widget.is_current = False
                widget.update_info()
            
            self.start_button.update()
            self.exit_button.update()
            self.play_button.update()
            self.pass_button.update()
            self.hand_cards_row.update()
            self.bottom_cards_row.update()
            
            self._show_message("欢迎来到斗地主！点击\"开始游戏\"按钮开始游戏。")
    
    def _play_cards(self, e):
        """出牌"""
        if not self.game or not self.selected_cards:
            self._show_message("请先选择要出的牌！")
            return
        
        player = self.game.players[self.player_index]
        
        if player != self.game.get_current_player():
            self._show_message("不是你的回合！")
            return
        
        card_type, _ = get_card_type(self.selected_cards)
        if card_type == CardType.INVALID:
            self._show_message("无效的牌型！")
            return
        
        if self.game.last_played_cards and self.game.last_played_player != player:
            if not compare_cards(self.selected_cards, self.game.last_played_cards):
                self._show_message("出的牌打不过上家！")
                return
        
        success, message = self.game.play_cards(player, self.selected_cards)
        
        if success:
            self._show_played_cards_for_player(player, self.selected_cards)
            self._show_message(f"出牌成功: {self.selected_cards}")
            self.selected_cards = []
            self._update_hand_cards()
            self._update_player_info()
            
            if self.game.is_game_over():
                winner = self.game.get_winner()
                self._show_message(f"游戏结束！{winner.name} 获胜！")
                self.play_button.disabled = True
                self.play_button.visible = False
                self.pass_button.disabled = True
                self.pass_button.visible = False
                self.exit_button.visible = False
                self.start_button.visible = True
                self._update_buttons()
                return
            
            self.game.next_turn()
            self._update_player_info()
            self._update_buttons()
            
            if self.page:
                self.page.run_task(self._ai_play)
        else:
            self._show_message(message)
    
    async def _pass_turn_async(self, player: DoudizhuPlayer):
        """异步过牌逻辑"""
        self._show_pass_for_player(player)
        self._show_message("不要")
        self._update_player_info()
        self._update_buttons()
        
        await asyncio.sleep(1)
        
        self.game.next_turn()
        self._update_player_info()
        self._update_buttons()
        
        await self._ai_play()
    
    def _pass_turn(self, e):
        """过牌"""
        if not self.game:
            return
        
        player = self.game.players[self.player_index]
        
        if player != self.game.get_current_player():
            self._show_message("不是你的回合！")
            return
        
        success, message = self.game.pass_turn(player)
        
        if success:
            if self.page:
                self.page.run_task(self._pass_turn_async, player)
        else:
            self._show_message(message)
    
    async def _ai_play(self):
        """AI出牌（异步版本）"""
        if not self.game:
            return
        
        while True:
            current_player = self.game.get_current_player()
            
            if current_player == self.game.players[self.player_index]:
                break
            
            cards_to_play = self._find_best_play(current_player)
            
            if cards_to_play:
                success, message = self.game.play_cards(current_player, cards_to_play)
                if success:
                    self._show_played_cards_for_player(current_player, cards_to_play)
                    self._show_message(f"{current_player.name} 出牌: {cards_to_play}")
                    self._update_player_info()
                    
                    if self.game.is_game_over():
                        winner = self.game.get_winner()
                        self._show_message(f"游戏结束！{winner.name} 获胜！")
                        self.play_button.disabled = True
                        self.play_button.visible = False
                        self.pass_button.disabled = True
                        self.pass_button.visible = False
                        self.exit_button.visible = False
                        self.start_button.visible = True
                        self._update_buttons()
                        return
                else:
                    self._show_message(f"{current_player.name} 出牌失败: {message}")
            else:
                if self.game.last_played_cards and self.game.last_played_player != current_player:
                    success, message = self.game.pass_turn(current_player)
                    if success:
                        self._show_pass_for_player(current_player)
                        self._show_message(f"{current_player.name} 不要")
                        self._update_player_info()
                        await asyncio.sleep(1)
                else:
                    pass
            
            self.game.next_turn()
            self._update_player_info()
            self._update_buttons()
    
    def _find_best_play(self, player: DoudizhuPlayer) -> List[DoudizhuCard]:
        """寻找最佳出牌"""
        if not self.game:
            return []
        
        last_cards = self.game.last_played_cards
        last_player = self.game.last_played_player
        
        if not last_cards or last_player == player:
            return self._find_first_play(player)
        
        return self._find_beat_play(player, last_cards)
    
    def _find_first_play(self, player: DoudizhuPlayer) -> List[DoudizhuCard]:
        """寻找首攻牌"""
        if not player.hand:
            return []
        
        from collections import Counter
        
        value_counts = Counter(card.get_weight() for card in player.hand)
        
        for value, count in sorted(value_counts.items()):
            if count == 1:
                for card in player.hand:
                    if card.get_weight() == value:
                        return [card]
        
        for value, count in sorted(value_counts.items()):
            if count == 2:
                cards = [card for card in player.hand if card.get_weight() == value]
                return cards[:2]
        
        return [player.hand[0]]
    
    def _find_beat_play(self, player: DoudizhuPlayer, last_cards: List[DoudizhuCard]) -> List[DoudizhuCard]:
        """寻找能压过的牌"""
        from collections import Counter
        
        last_type, last_info = get_card_type(last_cards)
        
        if last_type == CardType.INVALID:
            return []
        
        value_counts = Counter(card.get_weight() for card in player.hand)
        
        if last_type == CardType.SINGLE:
            last_value = last_info['value']
            for value in sorted(value_counts.keys()):
                if value > last_value and value_counts[value] >= 1:
                    for card in player.hand:
                        if card.get_weight() == value:
                            return [card]
        
        elif last_type == CardType.PAIR:
            last_value = last_info['value']
            for value in sorted(value_counts.keys()):
                if value > last_value and value_counts[value] >= 2:
                    cards = [card for card in player.hand if card.get_weight() == value]
                    return cards[:2]
        
        elif last_type == CardType.TRIPLE:
            last_value = last_info['value']
            for value in sorted(value_counts.keys()):
                if value > last_value and value_counts[value] >= 3:
                    cards = [card for card in player.hand if card.get_weight() == value]
                    return cards[:3]
        
        elif last_type == CardType.STRAIGHT:
            last_max = last_info['max']
            last_length = last_info['length']
            
            possible_straights = self._find_straights(player.hand, last_length)
            for straight in possible_straights:
                max_val = max(card.get_weight() for card in straight)
                if max_val > last_max:
                    return straight
        
        for value, count in value_counts.items():
            if count == 4:
                if last_type != CardType.BOMB or value > last_info.get('value', 0):
                    cards = [card for card in player.hand if card.get_weight() == value]
                    return cards[:4]
        
        has_small_joker = any(card.get_weight() == 16 for card in player.hand)
        has_big_joker = any(card.get_weight() == 17 for card in player.hand)
        if has_small_joker and has_big_joker:
            return [card for card in player.hand if card.get_weight() in (16, 17)]
        
        return []
    
    def _find_straights(self, cards: List[DoudizhuCard], length: int) -> List[List[DoudizhuCard]]:
        """寻找顺子"""
        from collections import defaultdict
        
        value_to_cards = defaultdict(list)
        for card in cards:
            value = card.get_weight()
            if value < 15:
                value_to_cards[value].append(card)
        
        values = sorted(value_to_cards.keys())
        straights = []
        
        for i in range(len(values)):
            straight = []
            current_value = values[i]
            straight.append(value_to_cards[current_value][0])
            
            for j in range(i + 1, len(values)):
                if values[j] == current_value + 1:
                    current_value = values[j]
                    straight.append(value_to_cards[current_value][0])
                    
                    if len(straight) == length:
                        straights.append(straight.copy())
                        break
                else:
                    break
        
        return straights


class MinesweeperGameUI:
    """扫雷游戏界面"""
    
    def __init__(self, on_exit=None):
        self.game: Optional[MinesweeperGame] = None
        self.page: Optional[ft.Page] = None
        self.on_exit = on_exit
        
        self.cell_buttons: List[List[ft.Container]] = []
        self.status_text: Optional[ft.Text] = None
        self.game_over_score_text: Optional[ft.Text] = None
        
        self.welcome_screen: Optional[ft.Container] = None
        self.game_screen: Optional[ft.Container] = None
        self.game_over_screen: Optional[ft.Container] = None
        
        self.start_button: Optional[ft.Button] = None
        self.restart_button: Optional[ft.Button] = None
        self.back_button: Optional[ft.Button] = None
        self.exit_button: Optional[ft.Button] = None
        self.game_exit_button: Optional[ft.Button] = None
    
    def build(self, page: ft.Page):
        """构建并返回UI控件"""
        self.page = page
        return self._build_ui()
    
    def show(self):
        """显示初始界面"""
        self._show_welcome_screen()
    
    def _get_number_color(self, count: int) -> str:
        """根据数字获取颜色"""
        colors = {
            1: ft.Colors.BLUE,
            2: ft.Colors.GREEN,
            3: ft.Colors.RED,
            4: ft.Colors.PURPLE,
            5: ft.Colors.BROWN,
            6: ft.Colors.CYAN,
            7: ft.Colors.BLACK,
            8: ft.Colors.GREY
        }
        return colors.get(count, ft.Colors.BLACK)
    
    def _build_ui(self):
        """构建UI"""
        self.status_text = ft.Text(
            "剩余: 250 个地雷",
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
        
        self.start_button = ft.Button(
            "开始游戏",
            on_click=self._start_game,
            width=200,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN,
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
                bgcolor=ft.Colors.GREEN,
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
                        color=ft.Colors.YELLOW,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "棋盘大小: 50 × 50",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "地雷数量: 250 个",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "左键: 翻开格子",
                        size=16,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Text(
                        "右键: 标记/取消问号",
                        size=16,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Text(
                        "翻开所有非地雷格子即可获胜",
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
                        [self.status_text, ft.Container(expand=True), self.game_exit_button],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Container(
                        content=ft.Column(
                            [],
                            scroll=ft.ScrollMode.AUTO,
                            spacing=0
                        ),
                        width=800,
                        height=550,
                        bgcolor=ft.Colors.GREY_800,
                        border=ft.Border.all(2, ft.Colors.WHITE),
                        padding=5
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
            self.game_over_screen.content.controls[0].value = "恭喜获胜！"
            self.game_over_screen.content.controls[0].color = ft.Colors.GREEN
            self.game_over_score_text.value = "你成功翻开了所有安全格子！"
        else:
            self.game_over_screen.content.controls[0].value = "游戏结束"
            self.game_over_screen.content.controls[0].color = ft.Colors.RED
            self.game_over_score_text.value = "很遗憾，你踩到了地雷！"
        
        self.welcome_screen.update()
        self.game_screen.update()
        self.game_over_screen.update()
    
    def _start_game(self, e):
        """开始游戏"""
        self.game = MinesweeperGame()
        self.game.init_game()
        self.game.is_running = True
        
        self._build_game_grid()
        self._update_status()
        
        self._show_game_screen()
    
    def _build_game_grid(self):
        """构建游戏网格"""
        if not self.game or not self.game_screen:
            return
        
        grid_container = self.game_screen.content.controls[2]
        column = grid_container.content
        column.controls.clear()
        
        self.cell_buttons = []
        
        cell_size = 10
        
        for y in range(self.game.GRID_HEIGHT):
            row_controls = []
            row_buttons = []
            for x in range(self.game.GRID_WIDTH):
                cell = ft.Container(
                    width=cell_size,
                    height=cell_size,
                    bgcolor=ft.Colors.GREY_500,
                    border=ft.Border.all(1, ft.Colors.GREY_700),
                    alignment=ft.Alignment(0, 0)
                )
                
                gesture = ft.GestureDetector(
                    content=cell,
                    on_tap=lambda e, x=x, y=y: self._on_left_click(x, y),
                    on_secondary_tap=lambda e, x=x, y=y: self._on_right_click(x, y),
                    data={"x": x, "y": y}
                )
                
                row_controls.append(gesture)
                row_buttons.append(cell)
            
            self.cell_buttons.append(row_buttons)
            column.controls.append(
                ft.Row(
                    row_controls,
                    spacing=0,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )
        
        column.update()
    
    def _update_status(self):
        """更新状态显示"""
        if self.game:
            remaining = self.game.MINE_COUNT - self.game.revealed_count
            self.status_text.value = f"已翻开: {self.game.revealed_count} 格"
            self.status_text.update()
    
    def _on_left_click(self, x: int, y: int):
        """左击事件"""
        if not self.game or not self.game.is_running:
            return
        
        continue_game = self.game.left_click(x, y)
        
        self._render_game()
        self._update_status()
        
        if not continue_game:
            if self.game.won:
                self._show_game_over_screen(won=True)
            else:
                self._reveal_all_mines()
                self._show_game_over_screen(won=False)
    
    def _on_right_click(self, x: int, y: int):
        """右击事件"""
        if not self.game or not self.game.is_running:
            return
        
        self.game.right_click(x, y)
        self._render_game()
    
    def _render_game(self):
        """渲染游戏"""
        if not self.game:
            return
        
        for y in range(self.game.GRID_HEIGHT):
            for x in range(self.game.GRID_WIDTH):
                cell = self.cell_buttons[y][x]
                state = self.game.cell_states[x][y]
                
                if state == CellState.HIDDEN:
                    cell.bgcolor = ft.Colors.GREY_500
                    cell.content = None
                elif state == CellState.QUESTIONED:
                    cell.bgcolor = ft.Colors.YELLOW_300
                    cell.content = ft.Text("?", size=8, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)
                elif state == CellState.REVEALED:
                    if self.game.grid[x][y]:
                        cell.bgcolor = ft.Colors.RED
                        cell.content = ft.Text("💣", size=8)
                    else:
                        mine_count = self.game.get_adjacent_mine_count(x, y)
                        cell.bgcolor = ft.Colors.GREY_200
                        if mine_count > 0:
                            cell.content = ft.Text(
                                str(mine_count),
                                size=8,
                                color=self._get_number_color(mine_count),
                                weight=ft.FontWeight.BOLD
                            )
                        else:
                            cell.content = None
                
                cell.update()
    
    def _reveal_all_mines(self):
        """揭示所有地雷"""
        if not self.game:
            return
        
        for y in range(self.game.GRID_HEIGHT):
            for x in range(self.game.GRID_WIDTH):
                cell = self.cell_buttons[y][x]
                
                if self.game.grid[x][y]:
                    cell.bgcolor = ft.Colors.RED
                    cell.content = ft.Text("💣", size=8)
                elif self.game.cell_states[x][y] == CellState.HIDDEN:
                    cell.bgcolor = ft.Colors.GREY_200
                    mine_count = self.game.get_adjacent_mine_count(x, y)
                    if mine_count > 0:
                        cell.content = ft.Text(
                            str(mine_count),
                            size=8,
                            color=self._get_number_color(mine_count),
                            weight=ft.FontWeight.BOLD
                        )
                    else:
                        cell.content = None
                
                cell.update()
    
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


class WhackAMoleGameUI:
    """打地鼠游戏界面"""
    
    def __init__(self, on_exit=None):
        self.game: Optional[WhackAMoleGame] = None
        self.page: Optional[ft.Page] = None
        self.game_task: Optional[asyncio.Task] = None
        self.on_exit = on_exit
        
        self.hole_containers: List[ft.Container] = []
        self.score_text: Optional[ft.Text] = None
        self.time_text: Optional[ft.Text] = None
        self.game_over_score_text: Optional[ft.Text] = None
        
        self.welcome_screen: Optional[ft.Container] = None
        self.game_screen: Optional[ft.Container] = None
        self.game_over_screen: Optional[ft.Container] = None
        
        self.start_button: Optional[ft.Button] = None
        self.restart_button: Optional[ft.Button] = None
        self.back_button: Optional[ft.Button] = None
        self.exit_button: Optional[ft.Button] = None
        self.game_exit_button: Optional[ft.Button] = None
    
    def build(self, page: ft.Page):
        """构建并返回UI控件"""
        self.page = page
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
        
        self.time_text = ft.Text(
            "时间: 20秒",
            size=24,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        self.game_over_score_text = ft.Text(
            "",
            size=24,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        self.start_button = ft.Button(
            "开始游戏",
            on_click=self._start_game,
            width=200,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN,
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
                bgcolor=ft.Colors.GREEN,
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
                        "🐿️ 打地鼠",
                        size=48,
                        color=ft.Colors.AMBER_400,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "16 个地洞，20 秒时间",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "每秒钟从随机 3 个洞出现松鼠",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "松鼠停留 300ms，打中得 1 分",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "达到 20 分即可获胜",
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
                        [self.score_text, ft.Container(expand=True), self.time_text, ft.Container(expand=True), self.game_exit_button],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self._build_holes_grid()
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
    
    def _build_holes_grid(self):
        """构建地洞网格"""
        self.hole_containers = []
        
        grid_rows = []
        hole_size = 100
        spacing = 20
        
        for row in range(4):
            row_controls = []
            for col in range(4):
                hole_index = row * 4 + col
                
                hole_container = ft.Container(
                    width=hole_size,
                    height=hole_size,
                    bgcolor=ft.Colors.BROWN_800,
                    border_radius=hole_size // 2,
                    border=ft.Border.all(4, ft.Colors.BROWN_600),
                    alignment=ft.Alignment(0, 0),
                    on_click=lambda e, idx=hole_index: self._on_hole_click(idx),
                    shadow=ft.BoxShadow(
                        spread_radius=2,
                        blur_radius=8,
                        color=ft.Colors.BLACK54,
                        offset=ft.Offset(0, 4)
                    )
                )
                
                self.hole_containers.append(hole_container)
                row_controls.append(hole_container)
            
            grid_rows.append(
                ft.Row(
                    row_controls,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=spacing
                )
            )
        
        return ft.Container(
            content=ft.Column(
                grid_rows,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=spacing
            ),
            bgcolor=ft.Colors.GREEN_800,
            border_radius=20,
            padding=30,
            border=ft.Border.all(3, ft.Colors.GREEN_600)
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
            self.game_over_score_text.value = f"太棒了！你打中了 {self.game.score} 只松鼠！"
        else:
            self.game_over_screen.content.controls[0].value = "⏰ 时间到！"
            self.game_over_screen.content.controls[0].color = ft.Colors.ORANGE
            self.game_over_score_text.value = f"你的分数: {self.game.score} / 20"
        
        self.welcome_screen.update()
        self.game_screen.update()
        self.game_over_screen.update()
    
    def _start_game(self, e):
        """开始游戏"""
        self.game = WhackAMoleGame()
        self.game.init_game()
        
        self._update_score()
        self._update_time()
        self._clear_all_holes()
        
        self.game.start()
        self._show_game_screen()
        
        if self.page:
            self.game_task = self.page.run_task(self._game_loop)
    
    def _clear_all_holes(self):
        """清空所有地洞的松鼠"""
        for container in self.hole_containers:
            container.content = None
            container.update()
    
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
            self.score_text.update()
    
    def _update_time(self):
        """更新时间显示"""
        if self.game:
            remaining = int(self.game.remaining_time)
            self.time_text.value = f"时间: {remaining}秒"
            
            if remaining <= 5:
                self.time_text.color = ft.Colors.RED
            else:
                self.time_text.color = ft.Colors.WHITE
            
            self.time_text.update()
    
    def _render_hole(self, hole_index: int):
        """渲染单个地洞"""
        if not self.game or not self.hole_containers:
            return
        
        container = self.hole_containers[hole_index]
        state = self.game.hole_states[hole_index]
        
        if state == HoleState.EMPTY:
            container.content = None
        elif state == HoleState.SQUIRREL:
            container.content = ft.Text(
                "🐿️",
                size=50,
                text_align=ft.TextAlign.CENTER
            )
        elif state == HoleState.HIT:
            container.content = ft.Text(
                "💥",
                size=50,
                text_align=ft.TextAlign.CENTER
            )
        
        container.update()
    
    def _on_hole_click(self, hole_index: int):
        """地洞点击事件"""
        if not self.game or not self.game.is_running:
            return
        
        hit = self.game.hit_hole(hole_index)
        
        if hit:
            self._render_hole(hole_index)
            self._update_score()
            
            if self.game.won:
                if self.game_task and not self.game_task.done():
                    self.game_task.cancel()
                self._show_game_over_screen(won=True)
    
    async def _game_loop(self):
        """游戏主循环"""
        if not self.game:
            return
        
        import time
        last_spawn_time = 0
        
        while self.game.is_running:
            self.game.update_time()
            self._update_time()
            
            current_time = time.time()
            if current_time - last_spawn_time >= 1.0:
                new_holes = self.game.spawn_squirrels()
                for hole_idx in new_holes:
                    self._render_hole(hole_idx)
                
                if new_holes:
                    self.page.run_task(self._hide_squirrels_delayed, new_holes.copy())
                    last_spawn_time = current_time
            
            if self.game.game_over:
                self._show_game_over_screen(won=False)
                break
            
            if self.game.won:
                self._show_game_over_screen(won=True)
                break
            
            await asyncio.sleep(0.1)
    
    async def _hide_squirrels_delayed(self, hole_indices: set):
        """延迟隐藏松鼠"""
        await asyncio.sleep(self.game.SQUIRREL_STAY_TIME)
        
        if self.game and self.game.is_running:
            for hole_idx in list(hole_indices):
                if self.game.hole_states[hole_idx] == HoleState.SQUIRREL:
                    self.game.hide_squirrels({hole_idx})
                    self._render_hole(hole_idx)


class GomokuGameUI:
    """五子棋游戏界面"""
    
    CELL_SIZE = 22
    PIECE_SIZE = 18
    BOARD_PADDING = 20
    
    def __init__(self, on_exit=None):
        self.game: Optional[GomokuGame] = None
        self.page: Optional[ft.Page] = None
        self.on_exit = on_exit
        self.ai_task: Optional[asyncio.Task] = None
        
        self.board_canvas: Optional[ft.Canvas] = None
        self.status_text: Optional[ft.Text] = None
        self.game_over_message: Optional[ft.Text] = None
        
        self.welcome_screen: Optional[ft.Container] = None
        self.game_screen: Optional[ft.Container] = None
        self.game_over_screen: Optional[ft.Container] = None
        
        self.start_button: Optional[ft.Button] = None
        self.restart_button: Optional[ft.Button] = None
        self.back_button: Optional[ft.Button] = None
        self.exit_button: Optional[ft.Button] = None
        self.game_exit_button: Optional[ft.Button] = None
    
    def build(self, page: ft.Page):
        """构建并返回UI控件"""
        self.page = page
        return self._build_ui()
    
    def show(self):
        """显示初始界面"""
        self._show_welcome_screen()
    
    def _build_ui(self):
        """构建UI"""
        self.status_text = ft.Text(
            "当前回合: 黑子（玩家）",
            size=22,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
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
                bgcolor=ft.Colors.GREEN,
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
                bgcolor=ft.Colors.GREEN,
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
                        "五子棋游戏",
                        size=48,
                        color=ft.Colors.AMBER,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "棋盘大小: 30 × 30",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "玩家: 黑子（先手）",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "机器人: 白子",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "谁先在横竖斜方向连成5颗相同颜色的棋子算赢",
                        size=16,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Text(
                        "超过5颗不算赢",
                        size=16,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Text(
                        "点击棋盘放置棋子",
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
                        [self.status_text, ft.Container(expand=True), self.game_exit_button],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Container(
                        content=ft.Stack([]),
                        expand=True,
                        alignment=ft.Alignment(0, 0)
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
            self.game_over_screen.content.controls[0].value = "恭喜获胜！"
            self.game_over_screen.content.controls[0].color = ft.Colors.GREEN
            self.game_over_message.value = "你赢了！五子连珠！"
        else:
            self.game_over_screen.content.controls[0].value = "游戏结束"
            self.game_over_screen.content.controls[0].color = ft.Colors.RED
            self.game_over_message.value = "机器人赢了！"
        
        self.welcome_screen.update()
        self.game_screen.update()
        self.game_over_screen.update()
    
    def _start_game(self, e):
        """开始游戏"""
        self.game = GomokuGame()
        self.game.init_game()
        self.game.is_running = True
        
        self._build_game_board()
        self._update_status()
        
        self._show_game_screen()
    
    def _build_game_board(self):
        """构建游戏棋盘"""
        if not self.game or not self.game_screen:
            return
        
        board_container = self.game_screen.content.controls[2]
        stack = board_container.content
        stack.controls.clear()
        
        board_size = self.game.BOARD_SIZE
        total_width = board_size * self.CELL_SIZE + self.BOARD_PADDING * 2
        total_height = board_size * self.CELL_SIZE + self.BOARD_PADDING * 2
        
        board_bg = ft.Container(
            width=total_width,
            height=total_height,
            bgcolor=ft.Colors.AMBER_200,
            border=ft.Border.all(3, ft.Colors.BROWN_800),
            border_radius=5
        )
        stack.controls.append(board_bg)
        
        grid_column = ft.Column(
            [],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        star_points = {
            (3, 3), (3, 15), (3, 27),
            (15, 3), (15, 15), (15, 27),
            (27, 3), (27, 15), (27, 27)
        }
        
        self.cell_buttons: List[List[ft.Container]] = []
        
        for y in range(board_size):
            row_controls = []
            row_buttons = []
            
            for x in range(board_size):
                is_star = (x, y) in star_points
                
                border = ft.Border(
                    top=ft.BorderSide(0.5, ft.Colors.BROWN_600) if y > 0 else ft.BorderSide(0, ft.Colors.TRANSPARENT),
                    bottom=ft.BorderSide(0.5, ft.Colors.BROWN_600) if y < board_size - 1 else ft.BorderSide(0, ft.Colors.TRANSPARENT),
                    left=ft.BorderSide(0.5, ft.Colors.BROWN_600) if x > 0 else ft.BorderSide(0, ft.Colors.TRANSPARENT),
                    right=ft.BorderSide(0.5, ft.Colors.BROWN_600) if x < board_size - 1 else ft.BorderSide(0, ft.Colors.TRANSPARENT)
                )
                
                cell_content = None
                if is_star:
                    cell_content = ft.Container(
                        width=6,
                        height=6,
                        bgcolor=ft.Colors.BROWN_800,
                        border_radius=3
                    )
                
                cell = ft.Container(
                    width=self.CELL_SIZE,
                    height=self.CELL_SIZE,
                    bgcolor=ft.Colors.TRANSPARENT,
                    border=border,
                    alignment=ft.Alignment(0, 0),
                    content=cell_content,
                    on_click=lambda e, x=x, y=y: self._on_cell_click(x, y),
                    data={"x": x, "y": y}
                )
                
                row_controls.append(cell)
                row_buttons.append(cell)
            
            self.cell_buttons.append(row_buttons)
            grid_column.controls.append(
                ft.Row(
                    row_controls,
                    spacing=0,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )
        
        grid_container = ft.Container(
            content=grid_column,
            left=self.BOARD_PADDING,
            top=self.BOARD_PADDING
        )
        stack.controls.append(grid_container)
        
        self.piece_containers: List[List[Optional[ft.Container]]] = [
            [None for _ in range(board_size)] for _ in range(board_size)
        ]
        
        board_container.update()
    
    def _update_status(self):
        """更新状态显示"""
        if self.game:
            if self.game.current_player == PlayerColor.BLACK:
                self.status_text.value = "当前回合: 黑子（玩家）"
                self.status_text.color = ft.Colors.BLACK
            else:
                self.status_text.value = "当前回合: 白子（机器人）"
                self.status_text.color = ft.Colors.WHITE
            self.status_text.update()
    
    def _on_cell_click(self, x: int, y: int):
        """格子点击事件"""
        if not self.game or not self.game.is_running:
            return
        
        if self.game.current_player != PlayerColor.BLACK:
            return
        
        if not self.game.is_valid_move(x, y):
            return
        
        success = self.game.make_move(x, y)
        
        self._draw_piece(x, y, PlayerColor.BLACK)
        self._update_status()
        
        if self.game.is_game_over():
            if self.game.winner == PlayerColor.BLACK:
                self._show_game_over_screen(won=True)
            else:
                self._show_game_over_screen(won=False)
            return
        
        if self.page:
            self.ai_task = self.page.run_task(self._ai_move_delayed)
    
    async def _ai_move_delayed(self):
        """AI延迟走棋"""
        await asyncio.sleep(1)
        
        if not self.game or not self.game.is_running:
            return
        
        if self.game.current_player != PlayerColor.WHITE:
            return
        
        ai_move = self.game.get_ai_move()
        
        if ai_move:
            x, y = ai_move
            success = self.game.make_move(x, y)
            
            self._draw_piece(x, y, PlayerColor.WHITE)
            self._update_status()
            
            if self.game.is_game_over():
                if self.game.winner == PlayerColor.BLACK:
                    self._show_game_over_screen(won=True)
                else:
                    self._show_game_over_screen(won=False)
    
    def _draw_piece(self, x: int, y: int, color: PlayerColor):
        """绘制棋子"""
        if not self.game_screen:
            return
        
        board_container = self.game_screen.content.controls[2]
        stack = board_container.content
        
        if self.piece_containers[y][x]:
            stack.controls.remove(self.piece_containers[y][x])
        
        piece_color = ft.Colors.BLACK if color == PlayerColor.BLACK else ft.Colors.WHITE
        border_color = ft.Colors.WHITE if color == PlayerColor.BLACK else ft.Colors.GREY_400
        
        piece_left = self.BOARD_PADDING + x * self.CELL_SIZE + (self.CELL_SIZE - self.PIECE_SIZE) // 2
        piece_top = self.BOARD_PADDING + y * self.CELL_SIZE + (self.CELL_SIZE - self.PIECE_SIZE) // 2
        
        piece = ft.Container(
            width=self.PIECE_SIZE,
            height=self.PIECE_SIZE,
            bgcolor=piece_color,
            border_radius=self.PIECE_SIZE // 2,
            border=ft.Border.all(1, border_color),
            left=piece_left,
            top=piece_top,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=3,
                color=ft.Colors.BLACK54,
                offset=ft.Offset(1, 1)
            )
        )
        
        self.piece_containers[y][x] = piece
        stack.controls.append(piece)
        
        board_container.update()
    
    def _restart_game(self, e):
        """重新开始游戏"""
        if self.ai_task and not self.ai_task.done():
            self.ai_task.cancel()
        
        self._start_game(e)
    
    def _back_to_welcome(self, e):
        """返回欢迎界面"""
        if self.ai_task and not self.ai_task.done():
            self.ai_task.cancel()
        
        self.game = None
        self._show_welcome_screen()
    
    def _exit_to_selector(self, e):
        """退出到游戏选择页面"""
        if self.ai_task and not self.ai_task.done():
            self.ai_task.cancel()
        
        self.game = None
        if self.on_exit:
            self.on_exit()
    
    def _exit_game_during_play(self, e):
        """游戏进行中退出"""
        if self.ai_task and not self.ai_task.done():
            self.ai_task.cancel()
        
        self.game = None
        self._exit_to_selector(e)


class GameSelector:
    """游戏选择页面"""
    
    def __init__(self):
        self.page: Optional[ft.Page] = None
        self.current_game_ui = None
        self.selector_controls = []
    
    def main(self, page: ft.Page):
        """主入口"""
        self.page = page
        page.title = "小游戏合集"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = ft.Colors.BLUE_GREY_900
        page.padding = 20
        page.window_width = 900
        page.window_height = 700
        page.window_resizable = True
        
        self._show_selector_screen()
    
    def _build_selector_ui(self):
        """构建选择页面UI"""
        title_text = ft.Text(
            "🎮 小游戏合集",
            size=48,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        subtitle_text = ft.Text(
            "请选择你想玩的游戏",
            size=20,
            color=ft.Colors.GREY_400
        )
        
        snake_button = ft.Button(
            "🐍 贪吃蛇",
            on_click=self._start_snake_game,
            width=250,
            height=80,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN_700,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)
            )
        )
        
        doudizhu_button = ft.Button(
            "🃏 斗地主",
            on_click=self._start_doudizhu_game,
            width=250,
            height=80,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.ORANGE_700,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)
            )
        )
        
        snake_desc = ft.Text(
            "使用 WASD 控制方向，吃到 50 个豆子获胜",
            size=14,
            color=ft.Colors.GREY_400
        )
        
        doudizhu_desc = ft.Text(
            "经典斗地主玩法，支持人机对战",
            size=14,
            color=ft.Colors.GREY_400
        )
        
        twentyone_button = ft.Button(
            "🎯 21点",
            on_click=self._start_twentyone_game,
            width=250,
            height=80,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.PURPLE_700,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)
            )
        )
        
        twentyone_desc = ft.Text(
            "用四个数字通过 + - * / 计算出 21",
            size=14,
            color=ft.Colors.GREY_400
        )
        
        minesweeper_button = ft.Button(
            "💣 扫雷",
            on_click=self._start_minesweeper_game,
            width=250,
            height=80,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.YELLOW_700,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)
            )
        )
        
        minesweeper_desc = ft.Text(
            "经典扫雷游戏，50×50 棋盘，250 个地雷",
            size=14,
            color=ft.Colors.GREY_400
        )
        
        whackamole_button = ft.Button(
            "🐿️ 打地鼠",
            on_click=self._start_whackamole_game,
            width=250,
            height=80,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.AMBER_600,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)
            )
        )
        
        whackamole_desc = ft.Text(
            "快速点击地鼠，20秒内打中20只获胜",
            size=14,
            color=ft.Colors.GREY_400
        )
        
        gomoku_button = ft.Button(
            "⚫ 五子棋",
            on_click=self._start_gomoku_game,
            width=250,
            height=80,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BROWN_700,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)
            )
        )
        
        gomoku_desc = ft.Text(
            "经典五子棋，100×100棋盘，人机对战",
            size=14,
            color=ft.Colors.GREY_400
        )
        
        tetris_button = ft.Button(
            "🟦 俄罗斯方块",
            on_click=self._start_tetris_game,
            width=250,
            height=80,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.CYAN_700,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)
            )
        )
        
        tetris_desc = ft.Text(
            "经典俄罗斯方块，消除行得分，达到20分获胜",
            size=14,
            color=ft.Colors.GREY_400
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Divider(height=50, color=ft.Colors.TRANSPARENT),
                    title_text,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    subtitle_text,
                    ft.Divider(height=80, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [
                            ft.Column(
                                [snake_button, snake_desc],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10
                            ),
                            ft.Container(width=40),
                            ft.Column(
                                [doudizhu_button, doudizhu_desc],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10
                            ),
                            ft.Container(width=40),
                            ft.Column(
                                [twentyone_button, twentyone_desc],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [
                            ft.Column(
                                [minesweeper_button, minesweeper_desc],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10
                            ),
                            ft.Container(width=40),
                            ft.Column(
                                [whackamole_button, whackamole_desc],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [
                            ft.Column(
                                [gomoku_button, gomoku_desc],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10
                            ),
                            ft.Container(width=40),
                            ft.Column(
                                [tetris_button, tetris_desc],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            expand=True,
            alignment=ft.Alignment(0, 0)
        )
    
    def _start_tetris_game(self, e):
        """启动俄罗斯方块游戏"""
        if self.page is None:
            return
        
        self.page.clean()
        
        def on_exit():
            self._show_selector_screen()
        
        game_ui = TetrisGameUI(on_exit=on_exit)
        
        self.page.title = "俄罗斯方块游戏"
        self.page.bgcolor = ft.Colors.BLUE_GREY_900
        self.page.window_width = 750
        self.page.window_height = 850
        
        self.current_game_ui = game_ui
        game_content = game_ui.build(self.page)
        self.page.add(game_content)
        game_ui.show()
    
    def _show_selector_screen(self):
        """显示游戏选择页面"""
        if self.page is None:
            return
        
        self.page.clean()
        
        self.page.title = "小游戏合集"
        self.page.bgcolor = ft.Colors.BLUE_GREY_900
        self.page.window_width = 900
        self.page.window_height = 700
        self.page.on_keyboard_event = None
        
        selector_ui = self._build_selector_ui()
        self.page.add(selector_ui)
        
        self.current_game_ui = None
    
    def _start_snake_game(self, e):
        """启动贪吃蛇游戏"""
        if self.page is None:
            return
        
        self.page.clean()
        
        def on_exit():
            self._show_selector_screen()
        
        game_ui = SnakeGameUI(on_exit=on_exit)
        
        self.page.title = "贪吃蛇游戏"
        self.page.bgcolor = ft.Colors.BLACK
        self.page.window_width = 800
        self.page.window_height = 650
        
        self.current_game_ui = game_ui
        game_content = game_ui.build(self.page)
        self.page.add(game_content)
        game_ui.show()
    
    def _start_doudizhu_game(self, e):
        """启动斗地主游戏"""
        if self.page is None:
            return
        
        self.page.clean()
        
        def on_exit():
            self._show_selector_screen()
        
        game_ui = DoudizhuGameUI(on_exit=on_exit)
        
        self.page.title = "斗地主游戏"
        self.page.bgcolor = ft.Colors.GREEN_700
        self.page.window_width = 1000
        self.page.window_height = 700
        
        self.current_game_ui = game_ui
        game_content = game_ui.build(self.page)
        self.page.add(game_content)
        game_ui.show()
    
    def _start_twentyone_game(self, e):
        """启动21点游戏"""
        if self.page is None:
            return
        
        self.page.clean()
        
        def on_exit():
            self._show_selector_screen()
        
        game_ui = TwentyOneGameUI(on_exit=on_exit)
        
        self.page.title = "21点游戏"
        self.page.bgcolor = ft.Colors.PURPLE_900
        self.page.window_width = 800
        self.page.window_height = 600
        
        self.current_game_ui = game_ui
        game_content = game_ui.build(self.page)
        self.page.add(game_content)
        game_ui.show()
    
    def _start_minesweeper_game(self, e):
        """启动扫雷游戏"""
        if self.page is None:
            return
        
        self.page.clean()
        
        def on_exit():
            self._show_selector_screen()
        
        game_ui = MinesweeperGameUI(on_exit=on_exit)
        
        self.page.title = "扫雷游戏"
        self.page.bgcolor = ft.Colors.BLUE_GREY_800
        self.page.window_width = 900
        self.page.window_height = 700
        
        self.current_game_ui = game_ui
        game_content = game_ui.build(self.page)
        self.page.add(game_content)
        game_ui.show()
    
    def _start_whackamole_game(self, e):
        """启动打地鼠游戏"""
        if self.page is None:
            return
        
        self.page.clean()
        
        def on_exit():
            self._show_selector_screen()
        
        game_ui = WhackAMoleGameUI(on_exit=on_exit)
        
        self.page.title = "打地鼠游戏"
        self.page.bgcolor = ft.Colors.GREEN_900
        self.page.window_width = 850
        self.page.window_height = 700
        
        self.current_game_ui = game_ui
        game_content = game_ui.build(self.page)
        self.page.add(game_content)
        game_ui.show()
    
    def _start_gomoku_game(self, e):
        """启动五子棋游戏"""
        if self.page is None:
            return
        
        self.page.clean()
        
        def on_exit():
            self._show_selector_screen()
        
        game_ui = GomokuGameUI(on_exit=on_exit)
        
        self.page.title = "五子棋游戏"
        self.page.bgcolor = ft.Colors.BROWN_900
        self.page.window_width = 900
        self.page.window_height = 800
        
        self.current_game_ui = game_ui
        game_content = game_ui.build(self.page)
        self.page.add(game_content)
        game_ui.show()


def main():
    """主函数"""
    import os
    
    print("=" * 50)
    print("小游戏合集")
    print("=" * 50)
    print(f"Python 版本: {sys.version}")
    print(f"工作目录: {os.getcwd()}")
    print(f"Flet 版本: {ft.__version__}")
    print("=" * 50)
    print("正在启动游戏界面...")
    print("游戏将在浏览器中打开。")
    print("如果浏览器没有自动打开，请手动访问显示的 URL。")
    print("=" * 50)
    
    try:
        game_selector = GameSelector()
        ft.run(game_selector.main, view=ft.AppView.WEB_BROWSER)
    except Exception as e:
        print(f"\n错误: {e}")
        print("\n可能的解决方案:")
        print("1. 如果你在 WSL 中运行，请确保有图形界面支持，或者:")
        print("   - 使用 Windows 本地的 Python 环境运行")
        print("   - 或者安装并配置 X Server (如 VcXsrv)")
        print("2. 检查 Flet 是否正确安装: pip install flet")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
