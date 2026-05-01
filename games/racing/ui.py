import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import asyncio
from typing import Optional
import flet as ft
from games.racing.game import RacingGame


class RacingGameUI:
    """赛车游戏界面"""
    
    def __init__(self, on_exit=None):
        self.game: Optional[RacingGame] = None
        self.page: Optional[ft.Page] = None
        self.game_task: Optional[asyncio.Task] = None
        self.on_exit = on_exit
        
        self.game_container: Optional[ft.Container] = None
        self.score_text: Optional[ft.Text] = None
        self.hp_text: Optional[ft.Text] = None
        
        self.welcome_screen: Optional[ft.Container] = None
        self.game_screen: Optional[ft.Container] = None
        
        self.start_button: Optional[ft.Button] = None
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
        self.score_text = ft.Text(
            "分数: 0",
            size=24,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        self.hp_text = ft.Text(
            "生命: ❤️❤️❤️",
            size=24,
            color=ft.Colors.RED,
            weight=ft.FontWeight.BOLD
        )
        
        self.game_container = ft.Container(
            width=200,
            height=500,
            bgcolor=ft.Colors.GREY_800,
            border=ft.Border.all(5, ft.Colors.WHITE),
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
                        "赛车游戏",
                        size=48,
                        color=ft.Colors.CYAN,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "使用 A/D 键左右移动",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "躲避障碍物，获得更高分数",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "碰到障碍物会减少生命",
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
                        [self.score_text, ft.Container(expand=True), self.hp_text, self.game_exit_button],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [self.game_container],
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
        self.game = RacingGame()
        self.game.init_game()
        self.game.is_running = True
        
        self._update_score()
        self._update_hp()
        self._render_game()
        
        self._show_game_screen()
        
        if self.page:
            self.game_task = self.page.run_task(self._game_loop)
    
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
            self.score_text.value = f"分数: {self.game.score}"
            self.score_text.update()
    
    def _update_hp(self):
        """更新生命显示"""
        if self.game:
            hearts = "❤️" * self.game.player_hp + "🖤" * (self.game.max_hp - self.game.player_hp)
            self.hp_text.value = f"生命: {hearts}"
            self.hp_text.update()
    
    def _render_game(self):
        """渲染游戏"""
        if not self.game or not self.game_container:
            return
        
        stack = self.game_container.content
        stack.controls.clear()
        
        player_size = 40
        player_x = self.game.player_x * 66
        player_y = self.game.GAME_HEIGHT - player_size - 10
        
        player = ft.Container(
            width=player_size,
            height=player_size,
            bgcolor=ft.Colors.RED,
            left=player_x,
            top=player_y,
            border_radius=5,
            content=ft.Text(
                "🚗",
                size=30,
                text_align=ft.TextAlign.CENTER
            )
        )
        stack.controls.append(player)
        
        for obs in self.game.obstacles:
            obs_size = 40
            obs_x = obs.x * 66
            obs_y = obs.y
            
            obstacle = ft.Container(
                width=obs_size,
                height=obs_size,
                bgcolor=ft.Colors.YELLOW,
                left=obs_x,
                top=obs_y,
                border_radius=5,
                content=ft.Text(
                    "🚧",
                    size=30,
                    text_align=ft.TextAlign.CENTER
                )
            )
            stack.controls.append(obstacle)
        
        self.game_container.update()
    
    def _on_keyboard_event(self, e):
        """键盘事件处理"""
        if not self.game or not self.game.is_running:
            return
        
        key = e.key.lower()
        
        if key == 'a':
            self.game.move_left()
            self._render_game()
        elif key == 'd':
            self.game.move_right()
            self._render_game()
    
    async def _game_loop(self):
        """游戏循环"""
        if not self.game:
            return
        
        while self.game.is_running:
            await asyncio.sleep(self.game.move_speed)
            
            if not self.game.is_running:
                break
            
            if self.game.check_collision():
                self.game.player_hp -= 1
                self._update_hp()
                
                if self.game.player_hp <= 0:
                    self.game.is_running = False
                    self._show_game_over_message()
                    break
            
            self.game.update_obstacles()
            self.game.score += 1
            self._update_score()
            self._render_game()
    
    def _show_game_over_message(self):
        """显示游戏结束消息"""
        import flet as ft
        
        content_col = self.game_screen.content
        
        if len(content_col.controls) > 3:
            content_col.controls = content_col.controls[:3]
        
        result_text = ft.Text(
            "游戏结束",
            size=36,
            color=ft.Colors.RED,
            weight=ft.FontWeight.BOLD
        )
        
        message_text = ft.Text(
            f"最终分数: {self.game.score}",
            size=24,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        restart_button = ft.Button(
            "再来一局",
            on_click=self._start_game,
            width=200,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
            )
        )
        
        buttons_row = ft.Row(
            [restart_button, self.exit_button],
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
