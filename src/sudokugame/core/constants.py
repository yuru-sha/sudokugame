"""ゲーム全体で使用する定数を定義するモジュール"""

# ウィンドウサイズ関連
WINDOW_SIZE = 540
BUTTON_HEIGHT = 40
CELL_SIZE = WINDOW_SIZE // 9

# 難易度設定
DIFFICULTY_LEVELS = ["簡単", "普通", "難しい", "エキスパート"]
CELLS_TO_REMOVE = {
    0: 40,  # 簡単: 41マス残す
    1: 50,  # 普通: 31マス残す
    2: 55,  # 難しい: 26マス残す
    3: 60   # エキスパート: 21マス残す
}

# UI関連
BUTTON_WIDTH = WINDOW_SIZE // 2 - 10
DIFFICULTY_BUTTON_HEIGHT = 70
DIFFICULTY_BUTTON_WIDTH = 300
DIFFICULTY_BUTTON_MARGIN = 40

# 色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LIGHT_RED = (255, 200, 200)
GREEN = (0, 255, 0)
LIGHT_BLUE = (100, 100, 255) 