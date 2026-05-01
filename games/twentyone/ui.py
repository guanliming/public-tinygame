import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import Optional
import flet as ft
from games.twentyone.game import TwentyOneGame


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
