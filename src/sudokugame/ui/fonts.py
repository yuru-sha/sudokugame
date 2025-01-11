"""フォント関連の機能を提供するモジュール"""

import sys
import pygame

def get_font_path(size: int) -> str:
    """システムに応じたフォントパスを返す"""
    if sys.platform == "darwin":  # macOS
        return "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc"
    else:  # Windows & Linux
        return None

def create_font(size: int) -> pygame.font.Font:
    """フォントオブジェクトを作成する"""
    font_path = get_font_path(size)
    return pygame.font.Font(font_path, size) 