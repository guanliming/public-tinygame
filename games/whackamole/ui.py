import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import asyncio
from typing import Optional, List
import flet as ft
from games.whackamole.game import WhackAMoleGame, HoleState


class WhackAMoleGameUI:
    """打地鼠游戏界面"""
    
    def __init__(self, on_exit=None):
        self.game: Optional[WhackAMoleGame] = None
        self.page: Optional[ft.Page] = None
        self.game_task: Optional[asyncio.Task] = None
        self.on_exit = on_exit
        
        self.score_text: Optional[ft.Text] = None
        self.time_left_text: Optional[ft.Text] = None
        self.game_over_score_text: Optional[ft.Text] = None
        self.game_grid: Optional[ft.GridView] = None
        
        self.welcome_screen: Optional[ft.Container] = None
        self.game_screen: Optional[ft.Container] = None
        self.game_over_screen: Optional[ft.Container] = None
        
        self.start_button: Optional[ft.Button] = None
        self.restart_button: Optional[ft.Button] = None
        self.back_button: Optional[ft.Button] = None
        self.exit_button: Optional[ft.Button] = None
        self.game_exit_button: Optional[ft.Button] = None
        
        self.hole_buttons: List[ft.ElevatedButton] = []
    
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
            "得分: 0",
            size=24,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        self.time_left_text = ft.Text(
            "时间: 20秒",
            size=24,
            color=ft.Colors.YELLOW,
            weight=ft.FontWeight.BOLD
        )
        
        self.game_over_score_text = ft.Text(
            "得分: 0",
            size=24,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        self.game_grid = ft.GridView(
            width=300,
            height=300,
            runs_count=4,
            spacing=10,
            run_spacing=10
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
                        "打地鼠游戏",
                        size=48,
                        color=ft.Colors.GREEN,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        f"{WhackAMoleGame.GAME_DURATION}秒内尽可能多地打地鼠",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        f"打中 {WhackAMoleGame.WIN_SCORE} 只即可获胜",
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
                        [self.score_text, self.time_left_text, ft.Container(expand=True), self.game_exit_button],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [self.game_grid],
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
    
    def _show_game_over_screen(self):
        """显示游戏结束界面"""
        self.welcome_screen.visible = False
        self.game_screen.visible = False
        self.game_over_screen.visible = True
        
        self.welcome_screen.update()
        self.game_screen.update()
        self.game_over_screen.update()
    
    def _start_game(self, e):
        """开始游戏"""
        self.game = WhackAMoleGame()
        self.game.init_game()
        self.game.is_running = True
        
        self._update_score()
        self._update_time_left()
        self._render_board()
        
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
            score_text = f"得分: {self.game.score}"
            self.score_text.value = score_text
            self.game_over_score_text.value = score_text
            self.score_text.update()
            self.game_over_score_text.update()
    
    def _update_time_left(self):
        """更新时间显示"""
        if self.game:
            self.time_left_text.value = f"时间: {int(self.game.remaining_time)}秒"
            self.time_left_text.update()
    
    def _render_board(self):
        """渲染游戏面板"""
        if not self.game or not self.game_grid:
            return
        
        self.game_grid.controls.clear()
        self.hole_buttons = []
        
        for i in range(self.game.HOLES_COUNT):
            btn = self._create_hole_button(i)
            self.hole_buttons.append(btn)
            self.game_grid.controls.append(btn)
        
        self.game_grid.update()
    
    def _create_hole_button(self, index: int) -> ft.ElevatedButton:
        """创建地洞按钮"""
        btn = ft.ElevatedButton(
            text="",
            width=65,
            height=65,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BROWN_700,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=32, weight=ft.FontWeight.BOLD)
            ),
            on_click=lambda e, idx=index: self._on_hole_click(idx)
        )
        
        return btn
    
    def _update_hole_display(self, index: int):
        """更新地洞显示"""
        if not self.game or index >= len(self.hole_buttons):
            return
        
        hole_state = self.game.hole_states[index]
        btn = self.hole_buttons[index]
        
        if hole_state == HoleState.SQUIRREL:
            btn.text = "🐿️"
            btn.style = ft.ButtonStyle(
                bgcolor=ft.Colors.BROWN_300,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=32, weight=ft.FontWeight.BOLD)
            )
        elif hole_state == HoleState.HIT:
            btn.text = "💥"
            btn.style = ft.ButtonStyle(
                bgcolor=ft.Colors.YELLOW,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=32, weight=ft.FontWeight.BOLD)
            )
        else:
            btn.text = ""
            btn.style = ft.ButtonStyle(
                bgcolor=ft.Colors.BROWN_700,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=32, weight=ft.FontWeight.BOLD)
            )
        
        btn.update()
    
    def _on_hole_click(self, index: int):
        """地洞点击事件"""
        if not self.game:
            return
        
        hit = self.game.hit_hole(index)
        if hit:
            self._update_score()
            self._update_hole_display(index)
    
    async def _game_loop(self):
        """游戏主循环"""
        if not self.game:
            return
        
        while self.game.is_running:
            await asyncio.sleep(0.3)
            
            if not self.game.is_running:
                break
            
            self.game.spawn_squirrels()
            self.game.update_time()
            
            self._update_time_left()
            
            for i in range(self.game.HOLES_COUNT):
                self._update_hole_display(i)
            
            if self.game.is_game_over():
                self._show_game_over_screen()
                break
