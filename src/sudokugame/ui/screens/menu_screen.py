"""メニュー画面を提供するモジュール"""

import pygame
from ...core.constants import (
    DIFFICULTY_LEVELS, DIFFICULTY_BUTTON_HEIGHT, DIFFICULTY_BUTTON_WIDTH,
    DIFFICULTY_BUTTON_MARGIN, WHITE, BLACK, BLUE, LIGHT_BLUE
)
from ..fonts import create_font

class MenuScreen:
    """難易度選択メニュー画面"""
    
    def __init__(self, screen):
        self.screen = screen
        self.difficulties = DIFFICULTY_LEVELS
        self.button_height = DIFFICULTY_BUTTON_HEIGHT
        self.button_width = DIFFICULTY_BUTTON_WIDTH
        self.margin = DIFFICULTY_BUTTON_MARGIN
        self.selected = None
        
    def draw(self):
        """画面を描画する"""
        self.screen.fill(WHITE)
        
        # タイトルの描画
        title_font = create_font(60)
        title = title_font.render("難易度選択", True, BLACK)
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title, title_rect)
        
        # 難易度選択ボタンの描画
        button_font = create_font(36)
        start_y = 120  # タイトルの下から固定の位置に配置
        
        for i, diff in enumerate(self.difficulties):
            button_rect = self._get_button_rect(i, start_y)
            color = LIGHT_BLUE if self.is_mouse_over_button(i) else BLUE
            pygame.draw.rect(self.screen, color, button_rect, border_radius=15)
            
            text = button_font.render(diff, True, WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)
    
    def is_mouse_over_button(self, index):
        """指定されたボタンの上にマウスがあるかどうかを判定する"""
        mouse_pos = pygame.mouse.get_pos()
        button_rect = self._get_button_rect(index, 120)
        return button_rect.collidepoint(mouse_pos)
    
    def handle_click(self, pos):
        """クリックイベントを処理する"""
        for i in range(len(self.difficulties)):
            button_rect = self._get_button_rect(i, 120)
            if button_rect.collidepoint(pos):
                return i
        return None
    
    def _get_button_rect(self, index, start_y):
        """指定されたインデックスのボタンの矩形を取得する"""
        return pygame.Rect(
            (self.screen.get_width() - self.button_width) // 2,
            start_y + index * (self.button_height + self.margin),
            self.button_width,
            self.button_height
        ) 