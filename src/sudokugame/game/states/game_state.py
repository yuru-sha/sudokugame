"""ゲーム状態を管理するモジュール"""

class GameState:
    """ゲームの状態を管理するクラス"""
    
    def __init__(self):
        # 選択されたセルの位置 (row, col)
        self.selected = None
        
        # ゲームの状態フラグ
        self.game_cleared = False  # ゲームクリア状態
        self.checking = False      # 答え合わせ中
        self.show_solution = False # 解答表示中
        
        # 現在の状態
        self.difficulty = None  # 選択された難易度
        self.in_game = False   # ゲーム中かメニュー画面か
    
    def start_game(self, difficulty):
        """ゲームを開始する"""
        self.difficulty = difficulty
        self.in_game = True
        self.reset_game_state()
    
    def return_to_menu(self):
        """メニュー画面に戻る"""
        self.in_game = False
        self.difficulty = None
        self.reset_game_state()
    
    def reset_game_state(self):
        """ゲーム状態をリセットする"""
        self.game_cleared = False
        self.checking = False
        self.show_solution = False
        self.selected = None 