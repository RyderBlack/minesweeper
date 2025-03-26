import pygame
from settings import *

# type list:
# "." > tile_unknown
# "x" > tile_mine
# "C" > clue
# "/" > empty

class Tile:
    def __init__(self, x, y, image, type, revealed=False, flagged=False):
        self.x, self.y = x * TILESIZE, y * TILESIZE
        self.image = image
        self.type = type
        self.revealed = revealed
        self.flagged = flagged
        
    def __repr__(self):
        return self.type
    
class Board:
    def __init__(self):
        self.board_surface = pygame.Surface((WIDTH, HEIGHT))
        self.board_list = [[Tile(col,row,tile_empty, ".") for row in range(ROWS)]  for col in range(COLS)]
    
    def display_board(self):
        for row in self.board_list:
            print(row)