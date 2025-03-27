import pygame

class Grid:
    def __init__(self, xGrid, yGrid, type, game):
        self.xGrid = xGrid  # Position X dans la grille
        self.yGrid = yGrid  # Position Y dans la grille
        self.game = game    # Référence au jeu principal
        self.clicked = False
        self.mineClicked = False
        self.mineFalse = False
        self.flag = False
        self.question = False
        self.val = type  # -1 pour mine, 0-8 pour nombre de mines adjacentes
        
        # Rectangle pour la détection de collision et le dessin
        self.rect = pygame.Rect(
            self.game.border + self.xGrid * self.game.grid_size,
            self.game.top_border + self.yGrid * self.game.grid_size,
            self.game.grid_size,
            self.game.grid_size
        )

    def draw(self):
        """Dessine la cellule selon son état"""
        if self.mineFalse:
            self.game.gameDisplay.blit(self.game.spr_mineFalse, self.rect)
        elif self.clicked:
            self.draw_revealed()
        else:
            self.draw_hidden()

    def draw_revealed(self):
        """Dessine une cellule révélée"""
        if self.val == -1:  # Mine
            if self.mineClicked:
                self.game.gameDisplay.blit(self.game.spr_mineClicked, self.rect)
            else:
                self.game.gameDisplay.blit(self.game.spr_mine, self.rect)
        else:  # Nombre ou vide
            sprite = getattr(self.game, f"spr_grid{self.val}" if self.val > 0 else "spr_emptyGrid")
            self.game.gameDisplay.blit(sprite, self.rect)

    def draw_hidden(self):
        """Dessine une cellule cachée"""
        if self.flag:
            self.game.gameDisplay.blit(self.game.spr_flag, self.rect)
        elif self.question:
            self.game.gameDisplay.blit(self.game.spr_question, self.rect)
        else:
            self.game.gameDisplay.blit(self.game.spr_grid, self.rect)

    def reveal(self):
        """Révèle la cellule"""
        if self.clicked or (self.flag and not self.question):
            return
            
        self.clicked = True
        
        # Si c'est un drapeau, le retirer
        if self.flag:
            self.game.mineLeft += 1
            self.flag = False
        
        # Si c'est une mine, fin du jeu
        if self.val == -1:
            return
            
        # Révélation automatique des cases vides
        if self.val == 0:
            self.reveal_adjacent()
            
    def reveal_adjacent(self):
        """Révèle automatiquement les cases adjacentes"""
        for x in range(-1, 2):
            if 0 <= self.xGrid + x < self.game.game_width:
                for y in range(-1, 2):
                    if 0 <= self.yGrid + y < self.game.game_height:
                        adj_cell = self.game.grid[self.yGrid + y][self.xGrid + x]
                        if not adj_cell.clicked:
                            adj_cell.reveal()

    def toggle_mark(self):
        """Change l'état de marquage (drapeau/question/rien)"""
        if not self.flag and not self.question:
            self.flag = True
            self.game.mineLeft -= 1
        elif self.flag and not self.question:
            self.flag = False
            self.question = True
            self.game.mineLeft += 1
        elif not self.flag and self.question:
            self.question = False

    def update_value(self):
        """Met à jour la valeur de la cellule (nombre de mines adjacentes)"""
        if self.val == -1:
            return
            
        for x in range(-1, 2):
            if 0 <= self.xGrid + x < self.game.game_width:
                for y in range(-1, 2):
                    if 0 <= self.yGrid + y < self.game.game_height:
                        if self.game.grid[self.yGrid + y][self.xGrid + x].val == -1:
                            self.val += 1