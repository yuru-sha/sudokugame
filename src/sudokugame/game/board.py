import random
from ..core.constants import CELLS_TO_REMOVE

class Board:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.initial_board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.incorrect_cells = set()

    def is_initial_cell(self, row, col):
        return self.initial_board[row][col] != 0

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

    def generate_puzzle(self, difficulty):
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
        
        # マスをランダムに削除
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        for i, j in positions[:CELLS_TO_REMOVE[difficulty]]:
            board[i][j] = 0
        
        self.board = [row[:] for row in board]
        self.initial_board = [row[:] for row in board]

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

    def is_board_filled(self):
        return all(all(num != 0 for num in row) for row in self.board)

    def set_number(self, row, col, num):
        if not self.is_initial_cell(row, col):
            self.board[row][col] = num
            self.incorrect_cells.clear()
            return True
        return False

    def clear_number(self, row, col):
        if not self.is_initial_cell(row, col):
            self.board[row][col] = 0
            self.incorrect_cells.clear()
            return True
        return False
