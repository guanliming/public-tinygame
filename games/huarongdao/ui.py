import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import asyncio
from typing import Optional, List, Tuple
import flet as ft
from games.huarongdao.game import HuarongdaoGame


class HuarongdaoGameUI:
    """华容道数字拼图游戏界面"""
    
    CELL_SIZE = 100
    BOARD_PADDING = 30
    
    def __init__(self, on_exit=None):
        self.game: Optional[HuarongdaoGame] = None
        self.page: Optional[ft.Page] = None
        self.game_task: Optional[asyncio.Task] = None
        self.on_exit = on_exit
        
        self.cell_containers: List[List[Optional[ft.Container]]] = []
        self.time_text: Optional[ft.Text] = None
        self.moves_text: Optional[ft.Text] = None
        self.game_over_message: Optional[ft.Text] = None
        
        self.welcome_screen: Optional[ft.Container] = None
        self.game_screen: Optional[ft.Container] = None
        self.game_over_screen: Optional[ft.Container] = None
        self.main_stack: Optional[ft.Stack] = None
        
        self.start_button: Optional[ft.Button] = None
        self.restart_button: Optional[ft.Button] = None
        self.back_button: Optional[ft.Button] = None
        self.exit_button: Optional[ft.Button] = None
        self.game_exit_button: Optional[ft.Button] = None
        
        self.board_stack: Optional[ft.Stack] = None
        self.dragging_cell: Optional[Tuple[int, int]] = None
        self.drag_start_global_x: float = 0
        self.drag_start_global_y: float = 0
        self.drag_accumulated_x: float = 0
        self.drag_accumulated_y: float = 0
        self.original_left: float = 0
        self.original_top: float = 0
    
    def build(self, page: ft.Page):
        """构建并返回UI控件"""
        self.page = page
        page.on_keyboard_event = None
        return self._build_ui()
    
    def show(self):
        """显示初始界面"""
        self._show_welcome_screen()
    
    def _get_number_color(self, num: int) -> str:
        """根据数字获取颜色"""
        colors = [
            ft.Colors.RED_500,
            ft.Colors.PINK_500,
            ft.Colors.PURPLE_500,
            ft.Colors.DEEP_PURPLE_500,
            ft.Colors.INDIGO_500,
            ft.Colors.BLUE_500,
            ft.Colors.LIGHT_BLUE_500,
            ft.Colors.CYAN_500,
            ft.Colors.TEAL_500,
            ft.Colors.GREEN_500,
            ft.Colors.LIGHT_GREEN_500,
            ft.Colors.LIME_500,
            ft.Colors.YELLOW_500,
            ft.Colors.AMBER_500,
            ft.Colors.ORANGE_500,
            ft.Colors.DEEP_ORANGE_500,
            ft.Colors.BROWN_500,
            ft.Colors.BLUE_GREY_500,
            ft.Colors.RED_600,
            ft.Colors.PINK_600,
            ft.Colors.PURPLE_600,
            ft.Colors.DEEP_PURPLE_600,
            ft.Colors.INDIGO_600,
            ft.Colors.BLUE_600,
        ]
        return colors[(num - 1) % len(colors)]
    
    def _build_ui(self):
        """构建UI"""
        self.time_text = ft.Text(
            "时间: 00:00",
            size=24,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        
        self.moves_text = ft.Text(
            "步数: 0",
            size=24,
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
                bgcolor=ft.Colors.TEAL_700,
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
                bgcolor=ft.Colors.TEAL_700,
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
                        "🧩 华容道",
                        size=48,
                        color=ft.Colors.TEAL_400,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "棋盘大小: 5 × 5",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "数字: 1 - 24",
                        size=18,
                        color=ft.Colors.WHITE
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "通过移动数字，将 1-24 按顺序排列",
                        size=16,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Text(
                        "可以拖动数字块或点击相邻数字移动",
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
                        [self.time_text, ft.Container(expand=True), self.moves_text, ft.Container(expand=True), self.game_exit_button],
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
        
        self.main_stack = ft.Stack(
            [
                self.welcome_screen,
                self.game_screen,
                self.game_over_screen
            ],
            expand=True
        )
        return self.main_stack
    
    def _show_welcome_screen(self):
        """显示欢迎界面"""
        print("[DEBUG Huarongdao] _show_welcome_screen called")
        print(f"[DEBUG Huarongdao] self.page is None: {self.page is None}")
        print(f"[DEBUG Huarongdao] welcome_screen visible before: {self.welcome_screen.visible if self.welcome_screen else 'None'}")
        print(f"[DEBUG Huarongdao] game_screen visible before: {self.game_screen.visible if self.game_screen else 'None'}")
        print(f"[DEBUG Huarongdao] game_over_screen visible before: {self.game_over_screen.visible if self.game_over_screen else 'None'}")
        
        self.welcome_screen.visible = True
        self.game_screen.visible = False
        self.game_over_screen.visible = False
        
        print(f"[DEBUG Huarongdao] welcome_screen visible after: {self.welcome_screen.visible}")
        print(f"[DEBUG Huarongdao] game_screen visible after: {self.game_screen.visible}")
        print(f"[DEBUG Huarongdao] game_over_screen visible after: {self.game_over_screen.visible}")
        
        if self.page:
            print("[DEBUG Huarongdao] Calling page.update()...")
            self.page.update()
            print("[DEBUG Huarongdao] page.update() completed")
        else:
            print("[DEBUG Huarongdao] self.page is None, cannot update")
    
    def _show_game_screen(self):
        """显示游戏界面"""
        self.welcome_screen.visible = False
        self.game_screen.visible = True
        self.game_over_screen.visible = False
        
        if self.page:
            self.page.update()
    
    def _show_game_over_screen(self, won: bool = False):
        """显示游戏结束界面"""
        self.welcome_screen.visible = False
        self.game_screen.visible = False
        self.game_over_screen.visible = True
        
        if won:
            self.game_over_screen.content.controls[0].value = "🎉 恭喜获胜！"
            self.game_over_screen.content.controls[0].color = ft.Colors.GREEN
            self.game_over_message.value = f"用时: {self.game.get_time_display()} | 步数: {self.game.move_count}"
        else:
            self.game_over_screen.content.controls[0].value = "游戏结束"
            self.game_over_screen.content.controls[0].color = ft.Colors.RED
        
        if self.page:
            self.page.update()
    
    def _start_game(self, e):
        """开始游戏"""
        self.game = HuarongdaoGame()
        self.game.init_game()
        self.game.start()
        
        self._build_game_board()
        self._update_time_display()
        self._update_moves_display()
        
        self._show_game_screen()
        
        if self.page:
            self.game_task = self.page.run_task(self._game_loop)
    
    def _calculate_cell_size(self):
        """根据屏幕尺寸计算单元格大小"""
        if not self.page:
            return self.CELL_SIZE
        
        available_width = self.page.width - 100
        available_height = self.page.height - 200
        
        max_cell_width = available_width // self.game.GRID_SIZE
        max_cell_height = available_height // self.game.GRID_SIZE
        
        cell_size = min(max_cell_width, max_cell_height, self.CELL_SIZE)
        return max(60, cell_size)
    
    def _build_game_board(self):
        """构建游戏棋盘"""
        if not self.game or not self.game_screen:
            return
        
        board_container = self.game_screen.content.controls[2]
        self.board_stack = board_container.content
        self.board_stack.controls.clear()
        
        cell_size = self._calculate_cell_size()
        grid_size = self.game.GRID_SIZE
        
        board_width = grid_size * cell_size + self.BOARD_PADDING * 2
        board_height = grid_size * cell_size + self.BOARD_PADDING * 2
        
        board_bg = ft.Container(
            width=board_width,
            height=board_height,
            bgcolor=ft.Colors.BLUE_GREY_800,
            border=ft.Border.all(5, ft.Colors.BLUE_GREY_600),
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=5,
                blur_radius=20,
                color=ft.Colors.BLACK54,
                offset=ft.Offset(0, 10)
            )
        )
        self.board_stack.controls.append(board_bg)
        
        self.cell_containers = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        
        for i in range(grid_size):
            for j in range(grid_size):
                value = self.game.board[i][j]
                
                if value == 0:
                    continue
                
                cell_color = self._get_number_color(value)
                
                cell = ft.Container(
                    width=cell_size - 4,
                    height=cell_size - 4,
                    bgcolor=cell_color,
                    border_radius=10,
                    border=ft.Border.all(2, ft.Colors.WHITE30),
                    alignment=ft.Alignment(0, 0),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=5,
                        color=ft.Colors.BLACK54,
                        offset=ft.Offset(2, 2)
                    ),
                    animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                    data={"row": i, "col": j}
                )
                
                cell.content = ft.Text(
                    str(value),
                    size=int(cell_size * 0.4),
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD
                )
                
                cell_left = self.BOARD_PADDING + j * cell_size + 2
                cell_top = self.BOARD_PADDING + i * cell_size + 2
                
                gesture = ft.GestureDetector(
                    content=cell,
                    on_tap=lambda e, row=i, col=j: self._on_cell_click(e, row, col),
                    on_pan_start=lambda e, row=i, col=j: self._on_pan_start(e, row, col),
                    on_pan_update=lambda e: self._on_pan_update(e),
                    on_pan_end=lambda e: self._on_pan_end(e),
                    data={"row": i, "col": j}
                )
                
                cell_wrapper = ft.Container(
                    content=gesture,
                    left=cell_left,
                    top=cell_top
                )
                
                self.cell_containers[i][j] = cell_wrapper
                self.board_stack.controls.append(cell_wrapper)
        
        board_container.update()
    
    def _on_cell_click(self, e, row: int, col: int):
        """格子点击事件"""
        if not self.game or not self.game.is_running:
            return
        
        try:
            if hasattr(e, 'control') and hasattr(e.control, 'data') and e.control.data:
                row = e.control.data.get('row', row)
                col = e.control.data.get('col', col)
        except (AttributeError, TypeError):
            pass
        
        if not self.game.can_move(row, col):
            return
        
        empty_pos = self.game._get_adjacent_empty_pos(row, col)
        if empty_pos is None:
            return
        
        empty_row, empty_col = empty_pos
        
        self.game.move(row, col)
        
        wrapper = self.cell_containers[row][col]
        if wrapper:
            cell_size = self._calculate_cell_size()
            new_left = self.BOARD_PADDING + empty_col * cell_size + 2
            new_top = self.BOARD_PADDING + empty_row * cell_size + 2
            
            wrapper.left = new_left
            wrapper.top = new_top
            
            try:
                if hasattr(wrapper, 'content') and hasattr(wrapper.content, 'data'):
                    wrapper.content.data = {'row': empty_row, 'col': empty_col}
            except (AttributeError, TypeError):
                pass
            
            wrapper.update()
            
            self.cell_containers[empty_row][empty_col] = wrapper
            self.cell_containers[row][col] = None
        
        self._update_moves_display()
        
        if self.game.won:
            if self.game_task and not self.game_task.done():
                self.game_task.cancel()
            self._show_game_over_screen(won=True)
    
    def _on_pan_start(self, e, row: int, col: int):
        """拖动开始"""
        if not self.game or not self.game.is_running:
            return
        
        try:
            if hasattr(e, 'control'):
                if hasattr(e.control, 'data') and e.control.data:
                    if isinstance(e.control.data, dict):
                        row = e.control.data.get('row', row)
                        col = e.control.data.get('col', col)
        except (AttributeError, TypeError):
            pass
        
        if not self.game.can_move(row, col):
            return
        
        self.dragging_cell = (row, col)
        self.drag_accumulated_x = 0
        self.drag_accumulated_y = 0
        
        wrapper = self.cell_containers[row][col]
        if wrapper:
            self.original_left = wrapper.left
            self.original_top = wrapper.top
    
    def _on_pan_update(self, e):
        """拖动更新"""
        if not self.dragging_cell:
            return
        
        row, col = self.dragging_cell
        wrapper = self.cell_containers[row][col]
        
        if wrapper:
            empty_pos = self.game._get_adjacent_empty_pos(row, col)
            if empty_pos is None:
                return
            
            empty_row, empty_col = empty_pos
            cell_size = self._calculate_cell_size()
            
            try:
                if hasattr(e, 'local_delta') and e.local_delta is not None:
                    delta_x = e.local_delta.x
                    delta_y = e.local_delta.y
                    self.drag_accumulated_x += delta_x
                    self.drag_accumulated_y += delta_y
                elif hasattr(e, 'delta_x'):
                    delta_x = e.delta_x
                    delta_y = e.delta_y
                    self.drag_accumulated_x += delta_x
                    self.drag_accumulated_y += delta_y
                elif hasattr(e, 'global_x'):
                    current_x = e.global_x
                    current_y = e.global_y
                    if self.drag_accumulated_x == 0 and self.drag_accumulated_y == 0:
                        self.drag_start_global_x = current_x
                        self.drag_start_global_y = current_y
                    self.drag_accumulated_x = current_x - self.drag_start_global_x
                    self.drag_accumulated_y = current_y - self.drag_start_global_y
                else:
                    return
            except (AttributeError, TypeError):
                return
            
            is_horizontal = row == empty_row
            is_vertical = col == empty_col
            
            if is_horizontal:
                max_move = cell_size * abs(empty_col - col)
                
                if empty_col > col:
                    new_left = max(self.original_left + self.drag_accumulated_x, self.original_left - max_move)
                    new_left = min(new_left, self.original_left + max_move)
                else:
                    new_left = max(self.original_left + self.drag_accumulated_x, self.original_left - max_move)
                    new_left = min(new_left, self.original_left + max_move)
                
                wrapper.left = new_left
            elif is_vertical:
                max_move = cell_size * abs(empty_row - row)
                
                if empty_row > row:
                    new_top = max(self.original_top + self.drag_accumulated_y, self.original_top - max_move)
                    new_top = min(new_top, self.original_top + max_move)
                else:
                    new_top = max(self.original_top + self.drag_accumulated_y, self.original_top - max_move)
                    new_top = min(new_top, self.original_top + max_move)
                
                wrapper.top = new_top
            
            wrapper.update()
    
    def _on_pan_end(self, e):
        """拖动结束"""
        if not self.dragging_cell:
            return
        
        row, col = self.dragging_cell
        wrapper = self.cell_containers[row][col]
        
        if wrapper:
            cell_size = self._calculate_cell_size()
            
            empty_pos = self.game._get_adjacent_empty_pos(row, col)
            if empty_pos is None:
                wrapper.left = self.original_left
                wrapper.top = self.original_top
                wrapper.update()
                self.dragging_cell = None
                return
            
            empty_row, empty_col = empty_pos
            is_horizontal = row == empty_row
            is_vertical = col == empty_col
            
            should_move = False
            
            if is_horizontal:
                if empty_col > col:
                    if self.drag_accumulated_x > cell_size * 0.5:
                        should_move = True
                else:
                    if self.drag_accumulated_x < -cell_size * 0.5:
                        should_move = True
            elif is_vertical:
                if empty_row > row:
                    if self.drag_accumulated_y > cell_size * 0.5:
                        should_move = True
                else:
                    if self.drag_accumulated_y < -cell_size * 0.5:
                        should_move = True
            
            if should_move:
                self.game.move(row, col)
                
                new_left = self.BOARD_PADDING + empty_col * cell_size + 2
                new_top = self.BOARD_PADDING + empty_row * cell_size + 2
                
                wrapper.left = new_left
                wrapper.top = new_top
                
                try:
                    if hasattr(wrapper, 'content') and hasattr(wrapper.content, 'data'):
                        wrapper.content.data = {'row': empty_row, 'col': empty_col}
                except (AttributeError, TypeError):
                    pass
                
                wrapper.update()
                
                self.cell_containers[empty_row][empty_col] = wrapper
                self.cell_containers[row][col] = None
                
                self._update_moves_display()
                
                if self.game.won:
                    if self.game_task and not self.game_task.done():
                        self.game_task.cancel()
                    self._show_game_over_screen(won=True)
            else:
                wrapper.left = self.original_left
                wrapper.top = self.original_top
                wrapper.update()
        
        self.dragging_cell = None
    
    def _update_board_display(self):
        """更新棋盘显示"""
        if not self.game or not self.board_stack:
            return
        
        cell_size = self._calculate_cell_size()
        grid_size = self.game.GRID_SIZE
        
        for i in range(grid_size):
            for j in range(grid_size):
                value = self.game.board[i][j]
                wrapper = self.cell_containers[i][j]
                
                if value == 0:
                    if wrapper and wrapper in self.board_stack.controls:
                        self.board_stack.controls.remove(wrapper)
                        self.cell_containers[i][j] = None
                else:
                    if wrapper is None:
                        for old_i in range(grid_size):
                            for old_j in range(grid_size):
                                old_wrapper = self.cell_containers[old_i][old_j]
                                if old_wrapper:
                                    gesture = old_wrapper.content
                                    cell = gesture.content
                                    if cell.data["row"] == i and cell.data["col"] == j:
                                        continue
                                    if str(cell.content.value) == str(value):
                                        self.cell_containers[i][j] = old_wrapper
                                        self.cell_containers[old_i][old_j] = None
                                        wrapper = old_wrapper
                                        break
                            if wrapper:
                                break
                    
                    if wrapper:
                        new_left = self.BOARD_PADDING + j * cell_size + 2
                        new_top = self.BOARD_PADDING + i * cell_size + 2
                        
                        wrapper.left = new_left
                        wrapper.top = new_top
                        wrapper.update()
        
        self.board_stack.update()
    
    def _update_time_display(self):
        """更新时间显示"""
        if self.game and self.time_text:
            self.game.update_time()
            self.time_text.value = f"时间: {self.game.get_time_display()}"
            self.time_text.update()
    
    def _update_moves_display(self):
        """更新步数显示"""
        if self.game and self.moves_text:
            self.moves_text.value = f"步数: {self.game.move_count}"
            self.moves_text.update()
    
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
    
    async def _game_loop(self):
        """游戏主循环"""
        if not self.game:
            return
        
        while self.game.is_running:
            self._update_time_display()
            await asyncio.sleep(1)
