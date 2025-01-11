"""ゲーム画面を提供するモジュール"""

import pygame
from ...core.constants import (
    CELL_SIZE, BUTTON_WIDTH, WHITE, BLACK, GRAY, BLUE,
    RED, LIGHT_RED, GREEN
)
from ..fonts import create_font

class GameScreen:
    """数独ゲーム画面"""
    
    def __init__(self, screen, window_size, button_height):
        self.screen = screen
        self.window_size = window_size
        self.button_height = button_height
        self.cell_size = CELL_SIZE
    
    def draw(self, game, game_state):
        """ゲーム画面を描画する"""
        self.screen.fill(WHITE)
        self._draw_grid()
        self._draw_numbers(game, game_state)
        self._draw_selected_cell(game, game_state)
        self._draw_buttons(game_state)
    
    def _draw_grid(self):
        """グリッド線を描画する"""
        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, BLACK, 
                           (i * self.cell_size, 0), 
                           (i * self.cell_size, self.window_size), 
                           line_width)
            pygame.draw.line(self.screen, BLACK, 
                           (0, i * self.cell_size), 
                           (self.window_size, i * self.cell_size), 
                           line_width)
    
    def _draw_numbers(self, game, game_state):
        """数字を描画する"""
        # 不正解のセルの背景を描画
        for row, col in game.board.incorrect_cells:
            pygame.draw.rect(self.screen, LIGHT_RED,
                           (col * self.cell_size, row * self.cell_size, 
                            self.cell_size, self.cell_size))
        
        # 数字を描画
        number_font = create_font(50)
        for i in range(9):
            for j in range(9):
                num = game.board.solution[i][j] if game_state.show_solution and not game.board.is_initial_cell(i, j) else game.board.board[i][j]
                if num != 0:
                    color = self._get_number_color(game, game_state, i, j)
                    num_surface = number_font.render(str(num), True, color)
                    x = j * self.cell_size + (self.cell_size - num_surface.get_width()) // 2
                    y = i * self.cell_size + (self.cell_size - num_surface.get_height()) // 2
                    self.screen.blit(num_surface, (x, y))
    
    def _draw_selected_cell(self, game, game_state):
        """選択されたセルを強調表示する"""
        if game_state.selected and not game_state.game_cleared and not game_state.show_solution:
            row, col = game_state.selected
            color = RED if game.board.is_initial_cell(row, col) else BLUE
            pygame.draw.rect(self.screen, color, 
                           (col * self.cell_size, row * self.cell_size, 
                            self.cell_size, self.cell_size), 3)
    
    def _get_number_color(self, game, game_state, row, col):
        """数字の色を取得する"""
        if game_state.show_solution and not game.board.is_initial_cell(row, col):
            return RED
        if game.board.is_initial_cell(row, col):
            return BLACK
        return BLUE if not game_state.checking else BLACK
    
    def _draw_buttons(self, game_state):
        """ボタンを描画する"""
        button_width = BUTTON_WIDTH
        
        # 答え合わせボタン
        check_color = GREEN if game_state.game_cleared else BLUE
        check_text = "ゲームクリア！" if game_state.game_cleared else "答え合わせ"
        pygame.draw.rect(self.screen, check_color, 
                        (0, self.window_size, button_width, self.button_height))
        
        # やめるボタン
        quit_color = RED if game_state.show_solution else BLUE
        quit_text = "解答表示中" if game_state.show_solution else "やめる"
        pygame.draw.rect(self.screen, quit_color, 
                        (button_width + 20, self.window_size, button_width, self.button_height))
        
        # ボタンのテキスト描画
        button_font = create_font(30)
        
        check_surface = button_font.render(check_text, True, WHITE)
        check_rect = check_surface.get_rect(
            center=(button_width // 2, self.window_size + self.button_height // 2))
        self.screen.blit(check_surface, check_rect)
        
        quit_surface = button_font.render(quit_text, True, WHITE)
        quit_rect = quit_surface.get_rect(
            center=(button_width + 20 + button_width // 2, 
                   self.window_size + self.button_height // 2))
        self.screen.blit(quit_surface, quit_rect) 