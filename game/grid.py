import pygame
from .constants import *

class Grid:
    def __init__(self, xGrid, yGrid, type):
        self.xGrid = xGrid
        self.yGrid = yGrid
        self.clicked = False
        self.mineClicked = False
        self.mineFalse = False
        self.flag = False
        self.question = False
        self.rect = pygame.Rect(
            BORDER + self.xGrid * GRID_SIZE,
            TOP_BORDER + self.yGrid * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        self.val = type

    def drawGrid(self, gameDisplay, sprites):
        if self.mineFalse:
            gameDisplay.blit(sprites["mineFalse"], self.rect)
        else:
            if self.clicked:
                if self.val == -1:
                    if self.mineClicked:
                        gameDisplay.blit(sprites["mineClicked"], self.rect)
                    else:
                        gameDisplay.blit(sprites["mine"], self.rect)
                else:
                    if self.val == 0:
                        gameDisplay.blit(sprites["empty"], self.rect)
                    else:
                        gameDisplay.blit(sprites[f"grid{self.val}"], self.rect)
            else:
                if self.flag:
                    gameDisplay.blit(sprites["flag"], self.rect)
                elif self.question:
                    gameDisplay.blit(sprites["question_mark"], self.rect)
                else:
                    gameDisplay.blit(sprites["Grid"], self.rect)

    def revealGrid(self, grid, game_width, game_height):
        self.clicked = True
        if self.val == 0:
            for x in range(-1, 2):
                if 0 <= self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if 0 <= self.yGrid + y < game_height:
                            if not grid[self.yGrid + y][self.xGrid + x].clicked:
                                grid[self.yGrid + y][self.xGrid + x].revealGrid(grid, game_width, game_height)

    def updateValue(self, grid, game_width, game_height):
        if self.val != -1:
            for x in range(-1, 2):
                if 0 <= self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if 0 <= self.yGrid + y < game_height:
                            if grid[self.yGrid + y][self.xGrid + x].val == -1:
                                self.val += 1