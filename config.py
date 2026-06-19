# ============================================================
# FILE: config.py
# ============================================================
"""
Configuration settings for the Memory Card Matching Game.
"""
import os

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (50, 150, 255)
GREEN = (50, 200, 50)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
PURPLE = (150, 50, 200)
ORANGE = (255, 150, 50)
CYAN = (50, 200, 200)
PINK = (255, 100, 150)

# Card settings
CARD_WIDTH = 80
CARD_HEIGHT = 100
CARD_MARGIN = 15
CARD_ROWS = 4
CARD_COLS = 4
TOTAL_CARDS = CARD_ROWS * CARD_COLS  # Must be even

# Game settings
FPS = 60
FLIP_DELAY = 800  # milliseconds

# Asset paths
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
IMAGE_SIZE = (64, 64)

# Symbols for cards (emojis / simple shapes)
SYMBOLS = [
    '★', '●', '▲', '◆', '♥', '♦', '♣', '♠',
    '✿', '☀', '☁', '☂', '☃', '☄', '★', '●'
][:TOTAL_CARDS // 2]
