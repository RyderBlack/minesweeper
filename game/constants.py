import os
import pygame

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITES_DIR = os.path.join(BASE_DIR, "assets", "Sprites")

# Cyberpunk Color Scheme
BG_COLOR = (15, 15, 30)  # Deep dark blue-black
BLACK = (0, 255, 255)  # Bright cyan instead of black
ACCENT_COLOR = (0, 255, 150)  # Bright green-cyan
BUTTON_COLOR = (30, 50, 80)  # Deep blue-gray
BUTTON_HOVER_COLOR = (50, 80, 120)  # Lighter blue-gray
TEXT_COLOR = (0, 255, 255)  # Bright cyan
GRID_COLOR = (30, 50, 80)  # Dark blue-gray for grid elements

# Game settings
GRID_SIZE = 32
BORDER = 24
TOP_BORDER = 100

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