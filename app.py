import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import flet as ft
from typing import Optional, List
from games.doudizhu import (
    DoudizhuGame, DoudizhuPlayer, PlayerRole, DoudizhuCard,
    get_card_type, compare_cards, CardType
)


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
        self.animate_offset = ft.animation.Animation(200, ft.AnimationCurve.EASE_OUT)
        
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
        self.border = ft.border.all(2, ft.Colors.BLACK12)
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=3,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 2)
        )
        
        if self.selected:
            self.offset = ft.Offset(0, -20)
            self.border = ft.border.all(3, ft.Colors.BLUE)
        else:
            self.offset = ft.Offset(0, 0)
        
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
                border=ft.border.all(3, border_color),
                alignment=ft.alignment.center
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


class DoudizhuGameUI:
    """斗地主游戏界面"""
    
    def __init__(self):
        self.game: Optional[DoudizhuGame] = None
        self.player_index = 0
        self.selected_cards: List[DoudizhuCard] = []
        self.card_widgets: List[CardWidget] = []
        
        self.page: Optional[ft.Page] = None
        self.player_info_widgets: List[PlayerInfoWidget] = []
        self.hand_cards_row: Optional[ft.Row] = None
        self.message_text: Optional[ft.Text] = None
        self.last_played_cards_row: Optional[ft.Row] = None
        self.start_button: Optional[ft.ElevatedButton] = None
        self.play_button: Optional[ft.ElevatedButton] = None
        self.pass_button: Optional[ft.ElevatedButton] = None
        self.bottom_cards_row: Optional[ft.Row] = None
    
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
        self.start_button = ft.ElevatedButton(
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
        
        self.play_button = ft.ElevatedButton(
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
        
        self.pass_button = ft.ElevatedButton(
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
        
        self.message_text = ft.Text(
            "",
            size=16,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        
        self.bottom_cards_row = ft.Row(
            [],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=2
        )
        
        self.last_played_cards_row = ft.Row(
            [],
            alignment=ft.MainAxisAlignment.CENTER,
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
        
        return ft.Column(
            [
                ft.Row(
                    [self.player_info_widgets[1]],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    [
                        ft.Column(
                            [self.player_info_widgets[2]],
                            alignment=ft.MainAxisAlignment.CENTER,
                            expand=1
                        ),
                        ft.Column(
                            [
                                ft.Row(
                                    [ft.Text("底牌:", size=14, color=ft.Colors.WHITE), self.bottom_cards_row],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                                ft.Row(
                                    [ft.Text("当前出牌:", size=14, color=ft.Colors.WHITE)],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                self.last_played_cards_row,
                                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                                self.message_text,
                                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                                ft.Row(
                                    [self.start_button, self.play_button, self.pass_button],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=20
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            expand=2
                        ),
                        ft.Column(
                            [self.player_info_widgets[0]],
                            alignment=ft.MainAxisAlignment.CENTER,
                            expand=1
                        )
                    ],
                    expand=True
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("我的手牌:", size=14, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                self.hand_cards_row
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ],
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
    
    def _update_last_played_cards(self):
        """更新最后出牌显示"""
        if not self.game:
            return
        
        self.last_played_cards_row.controls.clear()
        
        if self.game.last_played_cards:
            for card in self.game.last_played_cards:
                card_widget = CardWidget(card)
                card_widget.width = 50
                card_widget.height = 75
                self.last_played_cards_row.controls.append(card_widget)
        
        self.last_played_cards_row.update()
    
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
        self._update_last_played_cards()
        self._update_bottom_cards()
        
        self.start_button.disabled = True
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
            
            if self.game.last_played_cards and self.game.last_played_player != current_player:
                self.pass_button.disabled = False
            else:
                self.pass_button.disabled = True
        else:
            self.play_button.disabled = True
            self.pass_button.disabled = True
        
        self.play_button.update()
        self.pass_button.update()
        self.start_button.update()
    
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
            self._show_message(f"出牌成功: {self.selected_cards}")
            self.selected_cards = []
            self._update_hand_cards()
            self._update_last_played_cards()
            self._update_player_info()
            
            if self.game.is_game_over():
                winner = self.game.get_winner()
                self._show_message(f"游戏结束！{winner.name} 获胜！")
                self.play_button.disabled = True
                self.pass_button.disabled = True
                self.start_button.disabled = False
                self._update_buttons()
                return
            
            self.game.next_turn()
            self._update_player_info()
            self._update_buttons()
            
            self._ai_play()
        else:
            self._show_message(message)
    
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
            self._show_message("不要")
            self._update_player_info()
            self._update_buttons()
            
            self.game.next_turn()
            self._update_player_info()
            self._update_buttons()
            
            self._ai_play()
        else:
            self._show_message(message)
    
    def _ai_play(self):
        """AI出牌"""
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
                    self._show_message(f"{current_player.name} 出牌: {cards_to_play}")
                    self._update_last_played_cards()
                    self._update_player_info()
                    
                    if self.game.is_game_over():
                        winner = self.game.get_winner()
                        self._show_message(f"游戏结束！{winner.name} 获胜！")
                        self.play_button.disabled = True
                        self.pass_button.disabled = True
                        self.start_button.disabled = False
                        self._update_buttons()
                        return
                else:
                    self._show_message(f"{current_player.name} 出牌失败: {message}")
            else:
                if self.game.last_played_cards and self.game.last_played_player != current_player:
                    success, message = self.game.pass_turn(current_player)
                    if success:
                        self._show_message(f"{current_player.name} 不要")
                        self._update_player_info()
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
    print("斗地主游戏")
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
        game_ui = DoudizhuGameUI()
        ft.app(target=game_ui.main, view=ft.AppView.WEB_BROWSER)
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
