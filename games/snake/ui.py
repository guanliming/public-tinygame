import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import asyncio
from typing import Optional
import flet as ft
from games.snake.game import SnakeGame, Direction, Position


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
