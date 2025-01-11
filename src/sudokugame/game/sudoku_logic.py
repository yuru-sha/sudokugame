from .board import Board

class SudokuGame:
    def __init__(self, difficulty):
        self.board = Board()
        self.board.generate_puzzle(difficulty)

    def check_answer(self):
        if not self.board.is_board_filled():
            return False
        
        self.board.incorrect_cells.clear()
        
        # すべてのセルをチェック
        for i in range(9):
            for j in range(9):
                if not self.board.is_initial_cell(i, j):  # プレイヤーが入力したセルのみチェック
                    num = self.board.board[i][j]
                    if not self.board.is_valid_number(i, j, num):
                        self.board.incorrect_cells.add((i, j))
        
        # すべてのセルが正しければTrue
        return len(self.board.incorrect_cells) == 0

    def handle_input(self, row, col, num):
        if num == 0:
            return self.board.clear_number(row, col)
        return self.board.set_number(row, col, num)
