import pygame
import sys
import random
import os

# 初期化
pygame.init()

# 定数
WINDOW_SIZE = 540
CELL_SIZE = WINDOW_SIZE // 9
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LIGHT_RED = (255, 200, 200)
GREEN = (0, 255, 0)
LIGHT_BLUE = (100, 100, 255)

# フォント設定
def get_font(size):
    if sys.platform == "darwin":  # macOS
        return pygame.font.Font("/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc", size)
    else:  # Windows & Linux
        return pygame.font.Font(None, size)

# ウィンドウ設定
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + BUTTON_HEIGHT))
pygame.display.set_caption("数独ゲーム")

class DifficultySelector:
    def __init__(self):
        self.difficulties = ["簡単", "普通", "難しい", "エキスパート"]
        self.button_height = 80
        self.button_width = 300
        self.margin = 30
        self.selected = None
        
    def draw(self):
        screen.fill(WHITE)
        title_font = get_font(60)
        title = title_font.render("難易度選択", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 4))
        screen.blit(title, title_rect)
        
        button_font = get_font(36)
        total_height = len(self.difficulties) * (self.button_height + self.margin)
        start_y = (WINDOW_SIZE - total_height) // 2 + 50  # タイトルとボタンの間隔を調整
        
        for i, diff in enumerate(self.difficulties):
            button_rect = pygame.Rect(
                (WINDOW_SIZE - self.button_width) // 2,
                start_y + i * (self.button_height + self.margin),
                self.button_width,
                self.button_height
            )
            
            color = LIGHT_BLUE if self.is_mouse_over_button(i) else BLUE
            pygame.draw.rect(screen, color, button_rect, border_radius=15)
            
            text = button_font.render(diff, True, WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)
    
    def is_mouse_over_button(self, index):
        mouse_pos = pygame.mouse.get_pos()
        total_height = len(self.difficulties) * (self.button_height + self.margin)
        start_y = (WINDOW_SIZE - total_height) // 2 + 50  # タイトルとボタンの間隔を調整
        button_rect = pygame.Rect(
            (WINDOW_SIZE - self.button_width) // 2,
            start_y + index * (self.button_height + self.margin),
            self.button_width,
            self.button_height
        )
        return button_rect.collidepoint(mouse_pos)
    
    def handle_click(self, pos):
        for i in range(len(self.difficulties)):
            total_height = len(self.difficulties) * (self.button_height + self.margin)
            start_y = (WINDOW_SIZE - total_height) // 2 + 50  # タイトルとボタンの間隔を調整
            button_rect = pygame.Rect(
                (WINDOW_SIZE - self.button_width) // 2,
                start_y + i * (self.button_height + self.margin),
                self.button_width,
                self.button_height
            )
            if button_rect.collidepoint(pos):
                return i
        return None

class SudokuGame:
    def __init__(self, difficulty):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.initial_board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.incorrect_cells = set()
        self.selected = None
        self.game_cleared = False
        self.checking = False
        self.show_solution = False
        self.difficulty = difficulty
        self.generate_puzzle()

    def is_valid_for_generation(self, board, row, col, num):
        # 行チェック
        for x in range(9):
            if board[row][x] == num:
                return False
        
        # 列チェック
        for x in range(9):
            if board[x][col] == num:
                return False
        
        # 3x3ボックスチェック
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        
        return True

    def solve_board(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True
        
        row, col = empty
        for num in range(1, 10):
            if self.is_valid_for_generation(board, row, col, num):
                board[row][col] = num
                if self.solve_board(board):
                    return True
                board[row][col] = 0
        
        return False

    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def generate_puzzle(self):
        # 空の盤面から開始
        board = [[0 for _ in range(9)] for _ in range(9)]
        
        # 最初の数字をランダムに配置
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                board[i][j] = nums[i * 3 + j]
        
        # 盤面を解く
        self.solve_board(board)
        
        # 解答を保存
        self.solution = [row[:] for row in board]
        
        # 難易度に応じてマスを削除
        cells_to_remove = {
            0: 40,  # 簡単: 41マス残す
            1: 50,  # 普通: 31マス残す
            2: 55,  # 難しい: 26マス残す
            3: 60   # エキスパート: 21マス残す
        }
        
        # マスをランダムに削除
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        for i, j in positions[:cells_to_remove[self.difficulty]]:
            board[i][j] = 0
        
        self.board = [row[:] for row in board]
        self.initial_board = [row[:] for row in board]

    def is_initial_cell(self, row, col):
        return self.initial_board[row][col] != 0

    def is_valid_number(self, row, col, num):
        # 一時的に数字を取り除いてチェック
        original = self.board[row][col]
        self.board[row][col] = 0
        
        # 行チェック
        if num in self.board[row]:
            self.board[row][col] = original
            return False
        
        # 列チェック
        if num in [self.board[i][col] for i in range(9)]:
            self.board[row][col] = original
            return False
        
        # 3x3ボックスチェック
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num:
                    self.board[row][col] = original
                    return False
        
        self.board[row][col] = original
        return True

    def get_number_color(self, row, col):
        if self.show_solution and not self.initial_board[row][col]:
            return RED  # 解答表示時は赤色
        if self.initial_board[row][col] != 0:
            return BLACK
        return BLUE if not self.checking else BLACK

    def is_board_filled(self):
        return all(all(num != 0 for num in row) for row in self.board)

    def check_answer(self):
        if not self.is_board_filled():
            return False
        
        self.incorrect_cells.clear()
        self.checking = True
        
        # すべてのセルをチェック
        for i in range(9):
            for j in range(9):
                if not self.initial_board[i][j]:  # プレイヤーが入力したセルのみチェック
                    num = self.board[i][j]
                    if not self.is_valid_number(i, j, num):
                        self.incorrect_cells.add((i, j))
        
        # すべてのセルが正しければゲームクリア
        if not self.incorrect_cells:
            self.game_cleared = True
            return True
        return False

    def draw(self):
        screen.fill(WHITE)
        
        # グリッド線を描画
        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), line_width)
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), line_width)
        
        # セルの背景を描画
        for row, col in self.incorrect_cells:
            pygame.draw.rect(screen, LIGHT_RED,
                           (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # 数字を描画
        number_font = get_font(50)
        for i in range(9):
            for j in range(9):
                num = self.solution[i][j] if self.show_solution and not self.initial_board[i][j] else self.board[i][j]
                if num != 0:
                    color = self.get_number_color(i, j)
                    num_surface = number_font.render(str(num), True, color)
                    x = j * CELL_SIZE + (CELL_SIZE - num_surface.get_width()) // 2
                    y = i * CELL_SIZE + (CELL_SIZE - num_surface.get_height()) // 2
                    screen.blit(num_surface, (x, y))
        
        # 選択されたセルを強調表示
        if self.selected and not self.game_cleared and not self.show_solution:
            row, col = self.selected
            color = RED if self.is_initial_cell(row, col) else BLUE
            pygame.draw.rect(screen, color, 
                           (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
        
        # ボタンを描画
        button_width = WINDOW_SIZE // 2 - 10
        
        # 答え合わせボタン
        check_color = GREEN if self.game_cleared else BLUE
        check_text = "ゲームクリア！" if self.game_cleared else "答え合わせ"
        pygame.draw.rect(screen, check_color, (0, WINDOW_SIZE, button_width, BUTTON_HEIGHT))
        
        # やめるボタン
        quit_color = RED if self.show_solution else BLUE
        quit_text = "解答表示中" if self.show_solution else "やめる"
        pygame.draw.rect(screen, quit_color, (button_width + 20, WINDOW_SIZE, button_width, BUTTON_HEIGHT))
        
        # ボタンのテキスト描画
        button_font = get_font(30)
        
        check_surface = button_font.render(check_text, True, WHITE)
        check_rect = check_surface.get_rect(center=(button_width // 2, WINDOW_SIZE + BUTTON_HEIGHT // 2))
        screen.blit(check_surface, check_rect)
        
        quit_surface = button_font.render(quit_text, True, WHITE)
        quit_rect = quit_surface.get_rect(center=(button_width + 20 + button_width // 2, WINDOW_SIZE + BUTTON_HEIGHT // 2))
        screen.blit(quit_surface, quit_rect)

def main():
    while True:  # メインループを追加
        # 難易度選択画面
        difficulty_selector = DifficultySelector()
        selected_difficulty = None
        
        # 難易度選択ループ
        while selected_difficulty is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    selected_difficulty = difficulty_selector.handle_click(event.pos)
            
            difficulty_selector.draw()
            pygame.display.flip()
        
        # ゲーム開始
        game = SudokuGame(selected_difficulty)
        game_running = True
        
        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if y < WINDOW_SIZE:  # グリッド内をクリック
                        if not game.show_solution:  # 解答表示中はクリック無効
                            col = x // CELL_SIZE
                            row = y // CELL_SIZE
                            game.selected = (row, col)
                    elif WINDOW_SIZE <= y <= WINDOW_SIZE + BUTTON_HEIGHT:  # ボタンをクリック
                        button_width = WINDOW_SIZE // 2 - 10
                        if x <= button_width:  # 答え合わせボタン
                            if not game.game_cleared and not game.show_solution:
                                game.check_answer()
                        elif x >= button_width + 20:  # やめるボタン
                            game_running = False  # ゲームループを終了して難易度選択に戻る
                
                elif event.type == pygame.KEYDOWN and game.selected and not game.game_cleared and not game.show_solution:
                    row, col = game.selected
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                                   pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        if not game.is_initial_cell(row, col):
                            num = int(event.unicode)
                            game.board[row][col] = num
                            game.checking = False
                            game.incorrect_cells.clear()
                    elif event.key == pygame.K_BACKSPACE:
                        if not game.is_initial_cell(row, col):
                            game.board[row][col] = 0
                            game.checking = False
                            game.incorrect_cells.clear()
                
            game.draw()
            pygame.display.flip()

if __name__ == "__main__":
    main() 