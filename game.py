import pygame
import random
import os
from grid import Grid

class Game:
    def __init__(self):
        # Initialisation des paramètres de base
        self.bg_color = (192, 192, 192)
        self.grid_size = 32  # Taille d'une cellule
        self.border = 16  # Bordure latérale
        self.top_border = 100  # Bordure supérieure
        
        # Paramètres par défaut (peuvent être modifiés dans le menu)
        self.game_width = 10
        self.game_height = 10
        self.numMine = 9
        
        # Initialisation de l'affichage
        self.display_width = self.grid_size * self.game_width + self.border * 2
        self.display_height = self.grid_size * self.game_height + self.border + self.top_border
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Minesweeper")
        
        # Variables d'état
        self.gameState = "Menu"
        self.timer = pygame.time.Clock()
        self.t = 0
        self.mineLeft = 0
        self.grid = []
        self.mines = []
        
        # Chargement des ressources
        self.load_assets()

    def load_assets(self):
        """Charge toutes les images nécessaires"""
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
        assets_path = os.path.join(BASE_DIR, "assets/Sprites")
        
        self.spr_emptyGrid = pygame.image.load(os.path.join(assets_path, "empty.png"))
        self.spr_flag = pygame.image.load(os.path.join(assets_path, "flag.png"))
        self.spr_grid = pygame.image.load(os.path.join(assets_path, "Grid.png"))
        self.spr_grid1 = pygame.image.load(os.path.join(assets_path, "grid1.png"))
        self.spr_grid2 = pygame.image.load(os.path.join(assets_path, "grid2.png"))
        self.spr_grid3 = pygame.image.load(os.path.join(assets_path, "grid3.png"))
        self.spr_grid4 = pygame.image.load(os.path.join(assets_path, "grid4.png"))
        self.spr_grid5 = pygame.image.load(os.path.join(assets_path, "grid5.png"))
        self.spr_grid6 = pygame.image.load(os.path.join(assets_path, "grid6.png"))
        self.spr_grid7 = pygame.image.load(os.path.join(assets_path, "grid7.png"))
        self.spr_grid8 = pygame.image.load(os.path.join(assets_path, "grid8.png"))
        self.spr_mine = pygame.image.load(os.path.join(assets_path, "mine.png"))
        self.spr_question = pygame.image.load(os.path.join(assets_path, "question_mark.png"))
        self.spr_mineClicked = pygame.image.load(os.path.join(assets_path, "mineClicked.png"))
        self.spr_mineFalse = pygame.image.load(os.path.join(assets_path, "mineFalse.png"))

    def init_game(self):
        """Initialise une nouvelle partie"""
        self.gameState = "Playing"
        self.mineLeft = self.numMine
        self.grid = []
        self.mines = []
        self.t = 0
        
        # Génération des mines
        self.generate_mines()
        
        # Création de la grille
        self.create_grid()
        
        # Mise à jour des valeurs des cellules
        self.update_grid_values()

    def generate_mines(self):
        """Génère les positions des mines"""
        self.mines = [[random.randrange(0, self.game_width),
                      random.randrange(0, self.game_height)]]

        for c in range(self.numMine - 1):
            pos = [random.randrange(0, self.game_width),
                   random.randrange(0, self.game_height)]
            same = True
            while same:
                for i in range(len(self.mines)):
                    if pos == self.mines[i]:
                        pos = [random.randrange(0, self.game_width), 
                               random.randrange(0, self.game_height)]
                        break
                    if i == len(self.mines) - 1:
                        same = False
            self.mines.append(pos)

    def create_grid(self):
        """Crée la grille de jeu"""
        for j in range(self.game_height):
            line = []
            for i in range(self.game_width):
                if [i, j] in self.mines:
                    line.append(Grid(i, j, -1, self))
                else:
                    line.append(Grid(i, j, 0, self))
            self.grid.append(line)

    def update_grid_values(self):
        """Met à jour les valeurs des cellules (nombre de mines adjacentes)"""
        for row in self.grid:
            for cell in row:
                cell.update_value()

    def handle_events(self):
        """Gère les événements d'entrée"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameState = "Exit"
                
            if self.gameState == "Game Over" or self.gameState == "Win":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.init_game()
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    for row in self.grid:
                        for cell in row:
                            if cell.rect.collidepoint(event.pos):
                                if event.button == 1:  # Clic gauche
                                    cell.reveal()
                                    if cell.val == -1:
                                        self.gameState = "Game Over"
                                        cell.mineClicked = True
                                elif event.button == 3:  # Clic droit
                                    if not cell.clicked:
                                        cell.toggle_mark()

    def check_win(self):
        """Vérifie si le joueur a gagné"""
        for row in self.grid:
            for cell in row:
                if cell.val != -1 and not cell.clicked:
                    return False
        if self.gameState != "Exit":
            self.gameState = "Win"
        return True

    def draw(self):
        """Dessine l'état actuel du jeu"""
        self.gameDisplay.fill(self.bg_color)
        
        # Dessiner la grille
        for row in self.grid:
            for cell in row:
                cell.draw()
        
        # Dessiner le texte et l'interface
        if self.gameState == "Game Over":
            self.draw_text("Game Over!", 50)
            self.draw_text("R to restart", 35, 50)
            for row in self.grid:
                for cell in row:
                    if cell.flag and cell.val != -1:
                        cell.mineFalse = True
        elif self.gameState == "Win":
            self.draw_text("You WON!", 50)
            self.draw_text("R to restart", 35, 50)
        
        # Mettre à jour le temps et les mines restantes
        if self.gameState == "Playing":
            self.t += 1
        
        # Afficher le temps et le nombre de mines
        self.draw_time()
        self.draw_mines_left()

        pygame.display.update()

    def draw_text(self, txt, size, yOff=0):
        """Dessine du texte centré"""
        screen_text = pygame.font.SysFont("Calibri", size, True).render(txt, True, (0, 0, 0))
        rect = screen_text.get_rect()
        rect.center = (self.game_width * self.grid_size / 2 + self.border, 
                       self.game_height * self.grid_size / 2 + self.top_border + yOff)
        self.gameDisplay.blit(screen_text, rect)

    def draw_time(self):
        """Affiche le temps écoulé"""
        s = str(self.t // 15)
        screen_text = pygame.font.SysFont("Calibri", 50).render(s, True, (0, 0, 0))
        self.gameDisplay.blit(screen_text, (self.border, self.border))

    def draw_mines_left(self):
        """Affiche le nombre de mines restantes"""
        screen_text = pygame.font.SysFont("Calibri", 50).render(str(self.mineLeft), True, (0, 0, 0))
        self.gameDisplay.blit(screen_text, (self.display_width - self.border - 50, self.border))

    def run(self):
        """Boucle principale du jeu"""
        self.init_game()
        
        while self.gameState != "Exit":
            self.handle_events()
            
            if self.gameState == "Playing":
                self.check_win()
            
            self.draw()
            self.timer.tick(15)