import os
import pygame

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITES_DIR = os.path.join(BASE_DIR, "assets", "Sprites")

# Game settings
GRID_SIZE = 32
BORDER = 16
TOP_BORDER = 100

# Colors
BG_COLOR = (192, 192, 192)
BLACK = (0, 0, 0)

# Default configuration
DEFAULT_WIDTH = 30
DEFAULT_HEIGHT = 25
DEFAULT_MINES = 9

# Sprite names
SPRITE_NAMES = [
    "empty", "flag", "Grid", "grid1", "grid2", "grid3",
    "grid4", "grid5", "grid6", "grid7", "grid8",
    "mine", "question_mark", "mineClicked", "mineFalse"
]