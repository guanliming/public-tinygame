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


class SnakeGameUI:
    """贪吃蛇游戏界面"""
    
    def __init__(self):
        self.game: Optional[SnakeGame] = None
        self.page: Optional[ft.Page] = None
        self.game_task: Optional[asyncio.Task] = None
        
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
    
    def main(self, page: ft.Page):
        """主入口"""
        self.page = page
        page.title = "贪吃蛇游戏"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = ft.Colors.BLACK
        page.padding = 20
        page.window_width = 800
        page.window_height = 650
        page.window_resizable = False
        
        page.on_keyboard_event = self._on_keyboard_event
        
        page.add(self._build_ui())
        
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
                    self.start_button
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
                        [self.game_score_text],
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
                        [self.restart_button, self.back_button],
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
    
    def __init__(self):
        self.game: Optional[DoudizhuGame] = None
        self.player_index = 0
        self.selected_cards: List[DoudizhuCard] = []
        self.card_widgets: List[CardWidget] = []
        
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
    
    def main(self, page: ft.Page):
        """主入口"""
        self.page = page
        page.title = "斗地主游戏"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = ft.Colors.GREEN_700
        page.padding = 20
        page.window_width = 1000
        page.window_height = 700
        page.window_resizable = True
        
        page.add(self._build_ui())
        
        self._show_message("欢迎来到斗地主！点击\"开始游戏\"按钮开始游戏。")
    
    def _build_ui(self):
        """构建UI"""
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
        
        west_player_container = ft.Column(
            [
                self.player_info_widgets[2],
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                self.played_cards_widgets[2]
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=1
        )
        
        east_player_container = ft.Column(
            [
                self.player_info_widgets[1],
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                self.played_cards_widgets[1]
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
        
        return ft.Column(
            [
                ft.Row(
                    [
                        top_left_container,
                        ft.Container(expand=True)
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Row(
                    [
                        west_player_container,
                        center_container,
                        east_player_container
                    ],
                    expand=True
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    [south_player_container],
                    alignment=ft.MainAxisAlignment.CENTER
                )
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
        self.pass_button.disabled = not self.game.last_played_cards
        
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


def main():
    """主函数"""
    import os
    
    print("=" * 50)
    print("贪吃蛇游戏")
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
        game_ui = SnakeGameUI()
        ft.run(game_ui.main, view=ft.AppView.WEB_BROWSER)
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
