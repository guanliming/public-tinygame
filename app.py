import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import flet as ft
from typing import Optional

from games import (
    HuarongdaoGameUI,
    SudokuGameUI,
    TetrisGameUI,
    TwentyOneGameUI,
    SnakeGameUI,
    DoudizhuGameUI,
    MinesweeperGameUI,
    WhackAMoleGameUI,
    GomokuGameUI,
    JunqiGameUI,
    RacingGameUI
)


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
        
        sudoku_button = ft.Button(
            "🧩 数独",
            on_click=self._start_sudoku_game,
            width=250,
            height=80,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.DEEP_ORANGE_700,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)
            )
        )
        
        sudoku_desc = ft.Text(
            "经典数独游戏，9×9棋盘，每行每列每宫格1-9不重复",
            size=14,
            color=ft.Colors.GREY_400
        )
        
        junqi_button = ft.Button(
            "🚩 军旗",
            on_click=self._start_junqi_game,
            width=250,
            height=80,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.RED_700,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)
            )
        )
        
        junqi_desc = ft.Text(
            "经典军旗游戏，人机对战，夺取对方军旗获胜",
            size=14,
            color=ft.Colors.GREY_400
        )
        
        huarongdao_button = ft.Button(
            "🧩 华容道",
            on_click=self._start_huarongdao_game,
            width=250,
            height=80,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.TEAL_700,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)
            )
        )
        
        huarongdao_desc = ft.Text(
            "5×5数字拼图，拖动数字块完成排列",
            size=14,
            color=ft.Colors.GREY_400
        )
        
        racing_button = ft.Button(
            "🏎️ 极速赛车",
            on_click=self._start_racing_game,
            width=250,
            height=80,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)
            )
        )
        
        racing_desc = ft.Text(
            "A/D 左右移动，J 加速，躲避障碍物坚持30秒获胜",
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
                            ),
                            ft.Container(width=40),
                            ft.Column(
                                [racing_button, racing_desc],
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
                            ),
                            ft.Container(width=40),
                            ft.Column(
                                [sudoku_button, sudoku_desc],
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
                                [junqi_button, junqi_desc],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10
                            ),
                            ft.Container(width=40),
                            ft.Column(
                                [huarongdao_button, huarongdao_desc],
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
    
    def _start_sudoku_game(self, e):
        """启动数独游戏"""
        if self.page is None:
            return
        
        self.page.clean()
        
        def on_exit():
            self._show_selector_screen()
        
        game_ui = SudokuGameUI(on_exit=on_exit)
        
        self.page.title = "数独游戏"
        self.page.bgcolor = ft.Colors.DEEP_ORANGE_900
        self.page.window_width = 700
        self.page.window_height = 800
        
        self.current_game_ui = game_ui
        game_content = game_ui.build(self.page)
        self.page.add(game_content)
        game_ui.show()
    
    def _start_junqi_game(self, e):
        """启动军旗游戏"""
        if self.page is None:
            return
        
        self.page.clean()
        
        def on_exit():
            self._show_selector_screen()
        
        game_ui = JunqiGameUI(on_exit=on_exit)
        
        self.page.title = "军旗游戏"
        self.page.bgcolor = ft.Colors.BROWN_900
        self.page.window_width = 900
        self.page.window_height = 850
        
        self.current_game_ui = game_ui
        game_content = game_ui.build(self.page)
        self.page.add(game_content)
        game_ui.show()
    
    def _start_huarongdao_game(self, e):
        """启动华容道游戏"""
        if self.page is None:
            return
        
        self.page.clean()
        
        def on_exit():
            self._show_selector_screen()
        
        game_ui = HuarongdaoGameUI(on_exit=on_exit)
        
        self.page.title = "华容道游戏"
        self.page.bgcolor = ft.Colors.BLUE_GREY_900
        self.page.window_width = 800
        self.page.window_height = 850
        
        self.current_game_ui = game_ui
        game_content = game_ui.build(self.page)
        self.page.add(game_content)
        game_ui.show()
    
    def _start_racing_game(self, e):
        """启动赛车游戏"""
        if self.page is None:
            return
        
        self.page.clean()
        
        def on_exit():
            self._show_selector_screen()
        
        game_ui = RacingGameUI(on_exit=on_exit)
        
        self.page.title = "极速赛车游戏"
        self.page.bgcolor = ft.Colors.BLUE_GREY_900
        self.page.window_width = 500
        self.page.window_height = 750
        
        self.current_game_ui = game_ui
        game_content = game_ui.build(self.page)
        self.page.add(game_content)
        game_ui.show()


def main():
    """主函数"""
    import os
    import socket

    print("=" * 50)
    print("小游戏合集")
    print("=" * 50)
    print(f"Python 版本: {sys.version}")
    print(f"工作目录: {os.getcwd()}")
    print(f"Flet 版本: {ft.__version__}")
    print("=" * 50)
    print("正在启动游戏界面...")

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    print(f"\n游戏界面访问地址:")
    print(f"  - 本地访问: http://localhost:8000")
    print(f"  - 局域网访问: http://{local_ip}:8000")
    print(f"\n游戏将在浏览器中打开。")
    print(f"如果浏览器没有自动打开，请手动访问上述 URL。")
    print("=" * 50)

    try:
        game_selector = GameSelector()
        ft.run(game_selector.main, view=ft.AppView.WEB_BROWSER, port=8000)
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
