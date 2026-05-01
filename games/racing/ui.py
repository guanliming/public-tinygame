import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import asyncio
from typing import Optional
import flet as ft
from games.racing.game import RacingGame, DifficultyLevel


class RacingGameUI:
    """赛车游戏界面"""

    GAME_WIDTH = 300
    GAME_HEIGHT = 600
    PLAYER_WIDTH = 40
    PLAYER_HEIGHT = 60
    LANE_WIDTH = GAME_WIDTH // RacingGame.LANE_COUNT

    def __init__(self, on_exit=None):
        self.game: Optional[RacingGame] = None
        self.page: Optional[ft.Page] = None
        self.game_task: Optional[asyncio.Task] = None
        self.on_exit = on_exit
        self.selected_difficulty: DifficultyLevel = DifficultyLevel.HARD

        self.game_container: Optional[ft.Container] = None
        self.speed_text: Optional[ft.Text] = None
        self.time_text: Optional[ft.Text] = None
        self.difficulty_text: Optional[ft.Text] = None
        self.game_over_message: Optional[ft.Text] = None

        self.welcome_screen: Optional[ft.Container] = None
        self.game_screen: Optional[ft.Container] = None
        self.game_over_screen: Optional[ft.Container] = None

        self.medium_button: Optional[ft.Button] = None
        self.hard_button: Optional[ft.Button] = None
        self.restart_button: Optional[ft.Button] = None
        self.back_button: Optional[ft.Button] = None
        self.exit_button: Optional[ft.Button] = None
        self.game_exit_button: Optional[ft.Button] = None

        self.keys_pressed = set()
        self.last_update_time = 0

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
        self.speed_text = ft.Text(
            "速度: 0 km/h",
            size=20,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )

        self.time_text = ft.Text(
            "时间: 0.0 / 30.0 秒",
            size=20,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )

        self.difficulty_text = ft.Text(
            "难度: 最高难度",
            size=18,
            color=ft.Colors.ORANGE_400,
            weight=ft.FontWeight.BOLD
        )

        self.game_over_message = ft.Text(
            "",
            size=26,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )

        self.medium_button = ft.Button(
            "中等难度",
            on_click=lambda e: self._select_difficulty(DifficultyLevel.MEDIUM),
            width=200,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN_700,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
            )
        )

        self.hard_button = ft.Button(
            "最高难度",
            on_click=lambda e: self._select_difficulty(DifficultyLevel.HARD),
            width=200,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.RED_700,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
            )
        )

        self.restart_button = ft.Button(
            "再来一局",
            on_click=self._restart_game,
            width=200,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_700,
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
                        "🏎️ 极速赛车",
                        size=48,
                        color=ft.Colors.BLUE_400,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "选择难度",
                        size=22,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [self.medium_button, self.hard_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=30
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "中等难度：速度较慢，障碍物较少",
                        size=14,
                        color=ft.Colors.GREEN_400
                    ),
                    ft.Text(
                        "最高难度：速度较快，障碍物更多",
                        size=14,
                        color=ft.Colors.RED_400
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "操作说明",
                        size=16,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(
                        "A 键向左移动 | D 键向右移动 | J 键加速",
                        size=14,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "坚持 30 秒即可获胜",
                        size=16,
                        color=ft.Colors.BLUE_400
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [self.exit_button],
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

        self.game_container = ft.Container(
            width=self.GAME_WIDTH,
            height=self.GAME_HEIGHT,
            bgcolor=ft.Colors.GREY_800,
            border=ft.Border.all(3, ft.Colors.WHITE),
            content=ft.Stack([])
        )

        self.game_screen = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [self.speed_text, ft.Container(expand=True), self.time_text, ft.Container(expand=True), self.game_exit_button],
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
        print("[DEBUG Racing] _show_welcome_screen called")
        print(f"[DEBUG Racing] self.page is None: {self.page is None}")
        print(f"[DEBUG Racing] welcome_screen visible before: {self.welcome_screen.visible}")
        print(f"[DEBUG Racing] game_screen visible before: {self.game_screen.visible}")
        print(f"[DEBUG Racing] game_over_screen visible before: {self.game_over_screen.visible}")
        
        self.welcome_screen.visible = True
        self.game_screen.visible = False
        self.game_over_screen.visible = False
        
        print(f"[DEBUG Racing] welcome_screen visible after: {self.welcome_screen.visible}")
        print(f"[DEBUG Racing] game_screen visible after: {self.game_screen.visible}")
        print(f"[DEBUG Racing] game_over_screen visible after: {self.game_over_screen.visible}")
        
        if self.page:
            print("[DEBUG Racing] Calling page.update()...")
            self.page.update()
            print("[DEBUG Racing] page.update() completed")
        else:
            print("[DEBUG Racing] self.page is None, cannot update")

    def _show_game_screen(self):
        """显示游戏界面"""
        print("[DEBUG Racing] _show_game_screen called")
        print(f"[DEBUG Racing] self.page is None: {self.page is None}")
        
        self.welcome_screen.visible = False
        self.game_screen.visible = True
        self.game_over_screen.visible = False
        
        print(f"[DEBUG Racing] welcome_screen visible: {self.welcome_screen.visible}")
        print(f"[DEBUG Racing] game_screen visible: {self.game_screen.visible}")
        print(f"[DEBUG Racing] game_over_screen visible: {self.game_over_screen.visible}")
        
        if self.page:
            print("[DEBUG Racing] Calling page.update()...")
            self.page.update()
            print("[DEBUG Racing] page.update() completed")
        else:
            print("[DEBUG Racing] self.page is None, cannot update")

    def _show_game_over_screen(self, won: bool = False):
        """显示游戏结束界面"""
        print("[DEBUG Racing] _show_game_over_screen called")
        print(f"[DEBUG Racing] self.page is None: {self.page is None}")
        
        self.welcome_screen.visible = False
        self.game_screen.visible = False
        self.game_over_screen.visible = True

        if won:
            self.game_over_screen.content.controls[0].value = "🏆 恭喜获胜！"
            self.game_over_screen.content.controls[0].color = ft.Colors.GREEN
            self.game_over_message.value = f"太棒了！您坚持了 {self.game.game_time:.1f} 秒"
        else:
            self.game_over_screen.content.controls[0].value = "💥 游戏结束"
            self.game_over_screen.content.controls[0].color = ft.Colors.RED
            self.game_over_message.value = f"很遗憾！您坚持了 {self.game.game_time:.1f} 秒"

        print(f"[DEBUG Racing] welcome_screen visible: {self.welcome_screen.visible}")
        print(f"[DEBUG Racing] game_screen visible: {self.game_screen.visible}")
        print(f"[DEBUG Racing] game_over_screen visible: {self.game_over_screen.visible}")
        
        if self.page:
            print("[DEBUG Racing] Calling page.update()...")
            self.page.update()
            print("[DEBUG Racing] page.update() completed")
        else:
            print("[DEBUG Racing] self.page is None, cannot update")

    def _select_difficulty(self, difficulty: DifficultyLevel):
        """选择难度并开始游戏"""
        import time
        self.selected_difficulty = difficulty
        self.game = RacingGame(difficulty)
        self.game.init_game()
        self.game.is_running = True
        self.keys_pressed = set()
        self.last_update_time = time.time()

        self._update_speed()
        self._update_time()

        self._show_game_screen()

        if self.page:
            self.game_task = self.page.run_task(self._game_loop)

    def _start_game(self, e):
        """开始游戏（保留此方法以兼容旧代码）"""
        self._select_difficulty(self.selected_difficulty)

    def _on_keyboard_event(self, e):
        """键盘事件处理"""
        if not self.game or not self.game.is_running:
            return

        key = e.key.lower()
        is_pressed = not hasattr(e, 'type') or e.type != 'keyup'

        if is_pressed:
            self.keys_pressed.add(key)
        else:
            self.keys_pressed.discard(key)

        if key == 'a' and is_pressed:
            self.game.move_left()
        elif key == 'd' and is_pressed:
            self.game.move_right()
        elif key == 'j':
            self.game.set_accelerating(is_pressed)

    def _update_speed(self):
        """更新速度显示"""
        if self.game:
            speed_text = f"速度: {int(self.game.speed)} km/h"
            self.speed_text.value = speed_text

            if self.game.speed >= 120:
                self.speed_text.color = ft.Colors.RED
            elif self.game.speed >= 80:
                self.speed_text.color = ft.Colors.ORANGE
            else:
                self.speed_text.color = ft.Colors.WHITE

            self.speed_text.update()

    def _update_time(self):
        """更新时间显示"""
        if self.game:
            remaining = RacingGame.WIN_TIME - self.game.game_time
            time_text = f"时间: {self.game.game_time:.1f} / {RacingGame.WIN_TIME} 秒"
            self.time_text.value = time_text

            if remaining <= 5:
                self.time_text.color = ft.Colors.GREEN
            else:
                self.time_text.color = ft.Colors.WHITE

            self.time_text.update()

    def _render_game(self):
        """渲染游戏"""
        if not self.game or not self.game_container:
            return

        stack = self.game_container.content
        stack.controls.clear()

        road_bg = ft.Container(
            width=self.GAME_WIDTH,
            height=self.GAME_HEIGHT,
            bgcolor=ft.Colors.GREY_700
        )
        stack.controls.append(road_bg)

        for i in range(1, RacingGame.LANE_COUNT):
            lane_x = i * self.LANE_WIDTH
            lane_line = ft.Container(
                width=2,
                height=self.GAME_HEIGHT,
                bgcolor=ft.Colors.WHITE30,
                left=lane_x - 1
            )
            stack.controls.append(lane_line)

        for line in self.game.road_lines:
            for i in range(1, RacingGame.LANE_COUNT):
                lane_x = i * self.LANE_WIDTH - 3
                line_rect = ft.Container(
                    width=6,
                    height=line.height,
                    bgcolor=ft.Colors.WHITE,
                    left=lane_x,
                    top=line.y
                )
                stack.controls.append(line_rect)

        left_border = ft.Container(
            width=4,
            height=self.GAME_HEIGHT,
            bgcolor=ft.Colors.WHITE,
            left=0
        )
        right_border = ft.Container(
            width=4,
            height=self.GAME_HEIGHT,
            bgcolor=ft.Colors.WHITE,
            left=self.GAME_WIDTH - 4
        )
        stack.controls.append(left_border)
        stack.controls.append(right_border)

        for obstacle in self.game.obstacles:
            obs_x = obstacle.lane * self.LANE_WIDTH + (self.LANE_WIDTH - obstacle.width) // 2

            obs = ft.Container(
                width=obstacle.width,
                height=obstacle.height,
                bgcolor=ft.Colors.TRANSPARENT,
                left=obs_x,
                top=obstacle.y,
                content=ft.Stack([
                    ft.Container(
                        width=obstacle.width,
                        height=obstacle.height,
                        bgcolor=ft.Colors.RED_600,
                        border_radius=ft.BorderRadius(8, 8, 12, 12),
                        border=ft.Border.all(2, ft.Colors.RED_800)
                    ),
                    ft.Container(
                        width=obstacle.width - 12,
                        height=18,
                        bgcolor=ft.Colors.LIGHT_BLUE_200,
                        left=6,
                        top=8,
                        border_radius=3
                    ),
                    ft.Container(
                        width=8,
                        height=10,
                        bgcolor=ft.Colors.RED_900,
                        left=4,
                        top=obstacle.height - 4,
                        border_radius=2
                    ),
                    ft.Container(
                        width=8,
                        height=10,
                        bgcolor=ft.Colors.RED_900,
                        right=4,
                        top=obstacle.height - 4,
                        border_radius=2
                    )
                ]),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=6,
                    color=ft.Colors.BLACK54,
                    offset=ft.Offset(2, 2)
                )
            )

            stack.controls.append(obs)

        player_x = self.game.get_player_x()

        player = ft.Container(
            width=self.PLAYER_WIDTH,
            height=self.PLAYER_HEIGHT,
            bgcolor=ft.Colors.TRANSPARENT,
            left=player_x,
            top=self.game.player_y,
            content=ft.Stack([
                ft.Container(
                    width=self.PLAYER_WIDTH,
                    height=self.PLAYER_HEIGHT,
                    bgcolor=ft.Colors.BLUE_500,
                    border_radius=ft.BorderRadius(12, 12, 8, 8),
                    border=ft.Border.all(2, ft.Colors.BLUE_700)
                ),
                ft.Container(
                    width=self.PLAYER_WIDTH - 12,
                    height=18,
                    bgcolor=ft.Colors.LIGHT_BLUE_200,
                    left=6,
                    top=self.PLAYER_HEIGHT - 28,
                    border_radius=3
                ),
                ft.Container(
                    width=10,
                    height=10,
                    bgcolor=ft.Colors.YELLOW,
                    left=5,
                    top=5,
                    border_radius=2
                ),
                ft.Container(
                    width=10,
                    height=10,
                    bgcolor=ft.Colors.YELLOW,
                    right=5,
                    top=5,
                    border_radius=2
                )
            ]),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=6,
                color=ft.Colors.BLACK54,
                offset=ft.Offset(2, 2)
            )
        )

        stack.controls.append(player)
        stack.update()

    async def _game_loop(self):
        """游戏循环"""
        if not self.game:
            return

        import time

        while self.game.is_running:
            current_time = time.time()
            delta_time = current_time - self.last_update_time
            self.last_update_time = current_time

            continue_game = self.game.update(delta_time)

            self._update_speed()
            self._update_time()
            self._render_game()

            if not continue_game:
                if self.game.won:
                    self._show_game_over_screen(won=True)
                else:
                    self._show_game_over_screen(won=False)
                break

            await asyncio.sleep(0.016)

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
