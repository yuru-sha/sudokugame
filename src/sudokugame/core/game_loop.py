import pygame
import sys
from ..game.sudoku_logic import SudokuGame
from ..ui.screens.game_screen import GameScreen
from ..ui.screens.menu_screen import MenuScreen
from ..game.states.game_state import GameState
from .constants import WINDOW_SIZE, BUTTON_HEIGHT, BUTTON_WIDTH

class GameLoop:
    def __init__(self):
        pygame.init()
        
        # 画面設定
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + BUTTON_HEIGHT))
        pygame.display.set_caption("数独ゲーム")
        
        # コンポーネントの初期化
        self.game_state = GameState()
        self.game_screen = GameScreen(self.screen, WINDOW_SIZE, BUTTON_HEIGHT)
        self.menu_screen = MenuScreen(self.screen)
        self.game = None
    
    def run(self):
        while True:
            if not self.game_state.in_game:
                self.handle_menu_events()
                self.menu_screen.draw()
            else:
                self.handle_game_events()
                self.game_screen.draw(self.game, self.game_state)
            
            pygame.display.flip()
    
    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                difficulty = self.menu_screen.handle_click(event.pos)
                if difficulty is not None:
                    self.game = SudokuGame(difficulty)
                    self.game_state.start_game(difficulty)
    
    def handle_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < WINDOW_SIZE:  # グリッド内をクリック
                    if not self.game_state.show_solution:  # 解答表示中はクリック無効
                        col = x // (WINDOW_SIZE // 9)
                        row = y // (WINDOW_SIZE // 9)
                        self.game_state.selected = (row, col)
                elif WINDOW_SIZE <= y <= WINDOW_SIZE + BUTTON_HEIGHT:  # ボタンをクリック
                    if x <= BUTTON_WIDTH:  # 答え合わせボタン
                        if not self.game_state.game_cleared and not self.game_state.show_solution:
                            self.game_state.game_cleared = self.game.check_answer()
                    elif x >= BUTTON_WIDTH + 20:  # やめるボタン
                        self.game_state.return_to_menu()
                        self.game = None
            
            elif event.type == pygame.KEYDOWN and self.game_state.selected and not self.game_state.game_cleared and not self.game_state.show_solution:
                row, col = self.game_state.selected
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                               pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    num = int(event.unicode)
                    self.game.handle_input(row, col, num)
                    self.game_state.checking = False
                elif event.key == pygame.K_BACKSPACE:
                    self.game.handle_input(row, col, 0)
                    self.game_state.checking = False
