import random
import pygame
from .constants import BLACK, BORDER, GRID_SIZE, TOP_BORDER
from .grid import Grid

class GameCore:
    def __init__(self):
        self.grid = []
        self.mines = []
        self.game_state = "Playing"
        self.mine_left = 0
        self.first_click = True
        self.game_width = 0
        self.game_height = 0
        self.num_mine = 0
        self.t = 0

    def initialize_grid(self, width, height, mines):
        self.game_width = width
        self.game_height = height
        self.num_mine = mines
        self.mine_left = mines
        self.grid = []
        self.mines = []
        self.first_click = True
        self.t = 0
        
        for j in range(height):
            line = []
            for i in range(width):
                line.append(Grid(i, j, 0))
            self.grid.append(line)

    def generate_mines(self, first_x, first_y):
        self.mines = []
        safe_zone = [(first_x + dx, first_y + dy) for dx in range(-1, 2) for dy in range(-1, 2)]
        
        while len(self.mines) < self.num_mine:
            x = random.randrange(0, self.game_width)
            y = random.randrange(0, self.game_height)
            
            if (x, y) not in safe_zone and [x, y] not in self.mines:
                self.mines.append([x, y])
                self.grid[y][x].val = -1
        
        for row in self.grid:
            for cell in row:
                cell.updateValue(self.grid, self.game_width, self.game_height)

    def handle_click(self, pos, button, gameDisplay):
        for row in self.grid:
            for cell in row:
                if cell.rect.collidepoint(pos):
                    if button == 1 and not cell.flag and not cell.question:
                        if self.first_click:
                            self.first_click = False
                            self.generate_mines(cell.xGrid, cell.yGrid)
                        
                        cell.revealGrid(self.grid, self.game_width, self.game_height)
                        
                        if cell.val == -1:
                            self.game_state = "Game Over"
                            cell.mineClicked = True
                            
                    elif button == 3 and not cell.clicked:
                        if not cell.flag and not cell.question:
                            cell.flag = True
                            self.mine_left -= 1
                        elif cell.flag and not cell.question:
                            cell.flag = False
                            cell.question = True
                            self.mine_left += 1
                        elif not cell.flag and cell.question:
                            cell.question = False

    def check_win(self):
        if self.game_state == "Playing":
            for row in self.grid:
                for cell in row:
                    if cell.val != -1 and not cell.clicked:
                        return False
            # Modification pour le Hall of Fame : Ne met plus game_state à "Win" ici, délégué à main.py
            return True
        return False

    def draw(self, gameDisplay, sprites):
        for row in self.grid:
            for cell in row:
                cell.drawGrid(gameDisplay, sprites)
        
        if self.game_state == "Game Over":
            self.draw_text(gameDisplay, "Game Over!", 50)
            self.draw_text(gameDisplay, "R to restart", 35, 50)
            for row in self.grid:
                for cell in row:
                    if cell.flag and cell.val != -1:
                        cell.mineFalse = True
        elif self.game_state == "Win":
            self.draw_text(gameDisplay, "You WON!", 50)
            # Modification pour le Hall of Fame : Instruction pour sauvegarder le score
            self.draw_text(gameDisplay, "Press Enter to save your score", 35, 50)
        
        if self.game_state == "Playing":
            self.t += 1
        
        time_text = str(self.t // 15)
        self.draw_text(gameDisplay, time_text, 50, x=BORDER, y=BORDER, center=False)
        mine_text = str(self.mine_left)
        self.draw_text(gameDisplay, mine_text, 50, 
                      x=gameDisplay.get_width() - BORDER - 50, 
                      y=BORDER, center=False)

    def draw_text(self, gameDisplay, text, size, y_offset=0, x=None, y=None, center=True):
        font = pygame.font.SysFont("Calibri", size, True)
        screen_text = font.render(text, True, BLACK)
        rect = screen_text.get_rect()
        
        if center:
            rect.center = (self.game_width * GRID_SIZE / 2 + BORDER, 
                          self.game_height * GRID_SIZE / 2 + TOP_BORDER + y_offset)
        else:
            rect.topleft = (x, y)
        
        gameDisplay.blit(screen_text, rect)