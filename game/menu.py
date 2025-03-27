import pygame
from .constants import *

class Menu:
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.input_width = str(DEFAULT_WIDTH)
        self.input_height = str(DEFAULT_HEIGHT)
        self.input_mines = str(DEFAULT_MINES)
        self.active_input = None
        self.error_message = ""

    def draw(self):
        self.gameDisplay.fill(BG_COLOR)
        
        self.draw_text("Set Grid Size", 40, -200)
        self.draw_text("Width:", 30, -150)
        self.draw_text("Height:", 30, -100)
        self.draw_text("Mines:", 30, -50)

        box_width, box_height = 100, 30
        width_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - box_width // 2,
            150, box_width, box_height
        )
        height_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - box_width // 2,
            200, box_width, box_height
        )
        mines_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - box_width // 2,
            250, box_width, box_height
        )
        start_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - 80,
            300, 160, 40
        )
        # Ajout pour le Hall of Fame : Bouton pour accéder au Hall of Fame
        hof_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - 80,
            350, 160, 40
        )

        pygame.draw.rect(self.gameDisplay, (255, 255, 255), width_box, 2 if self.active_input == "width" else 1)
        pygame.draw.rect(self.gameDisplay, (255, 255, 255), height_box, 2 if self.active_input == "height" else 1)
        pygame.draw.rect(self.gameDisplay, (255, 255, 255), mines_box, 2 if self.active_input == "mines" else 1)
        pygame.draw.rect(self.gameDisplay, (0, 200, 0), start_box)
        # Ajout pour le Hall of Fame : Dessin du bouton Hall of Fame
        pygame.draw.rect(self.gameDisplay, (0, 150, 200), hof_box)
        
        start_text = pygame.font.SysFont("Calibri", 25).render("START", True, (255, 255, 255))
        # Ajout pour le Hall of Fame : Texte du bouton Hall of Fame
        hof_text = pygame.font.SysFont("Calibri", 25).render("Hall of Fame", True, (255, 255, 255))
        self.gameDisplay.blit(start_text, (start_box.x + 50, start_box.y + 10))
        # Ajout pour le Hall of Fame : Positionnement du texte Hall of Fame
        self.gameDisplay.blit(hof_text, (hof_box.x + 20, hof_box.y + 10))

        for box, text in [(width_box, self.input_width), 
                         (height_box, self.input_height), 
                         (mines_box, self.input_mines)]:
            screen_text = pygame.font.SysFont("Calibri", 25).render(text, True, BLACK)
            self.gameDisplay.blit(screen_text, (box.x + 10, box.y + 5))

        if self.error_message:
            self.draw_text(self.error_message, 20, 100)

        pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            result = self.handle_mouse_click(event.pos)
            return result
        elif event.type == pygame.KEYDOWN and self.active_input:
            self.handle_key_input(event)
        return None

    def handle_mouse_click(self, pos):
        box_width, box_height = 100, 30
        width_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - box_width // 2,
            150, box_width, box_height
        )
        height_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - box_width // 2,
            200, box_width, box_height
        )
        mines_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - box_width // 2,
            250, box_width, box_height
        )
        start_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - 80,
            300, 160, 40
        )
        # Ajout pour le Hall of Fame : Définition de la zone cliquable pour le bouton Hall of Fame
        hof_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - 80,
            350, 160, 40
        )

        self.active_input = None
        if width_box.collidepoint(pos):
            self.active_input = "width"
        elif height_box.collidepoint(pos):
            self.active_input = "height"
        elif mines_box.collidepoint(pos):
            self.active_input = "mines"
        elif start_box.collidepoint(pos):
            result = self.validate_inputs()
            return result
        # Ajout pour le Hall of Fame : Détection du clic sur le bouton Hall of Fame et renvoi d'un signal
        elif hof_box.collidepoint(pos):
            return "hall_of_fame"

        return None    

    def handle_key_input(self, event):
        if event.key == pygame.K_BACKSPACE:
            if self.active_input == "width":
                self.input_width = self.input_width[:-1]
            elif self.active_input == "height":
                self.input_height = self.input_height[:-1]
            elif self.active_input == "mines":
                self.input_mines = self.input_mines[:-1]
        elif event.unicode.isdigit():
            if self.active_input == "width":
                self.input_width += event.unicode
            elif self.active_input == "height":
                self.input_height += event.unicode
            elif self.active_input == "mines":
                self.input_mines += event.unicode

    def validate_inputs(self):
        try:
            w = int(self.input_width)
            h = int(self.input_height)
            m = int(self.input_mines)
            
            if w < 1 or h < 1 or m < 1:
                self.error_message = "Values must be positive"
                return None
            elif m >= w * h:
                self.error_message = "Too many mines"
                return None
            else:
                self.error_message = ""
                return (w, h, m)
        except ValueError:
            self.error_message = "Invalid numbers"
            return None

    def draw_text(self, text, size, y_offset=0):
        font = pygame.font.SysFont("Calibri", size, True)
        screen_text = font.render(text, True, BLACK)
        rect = screen_text.get_rect()
        rect.center = (
            self.gameDisplay.get_width() // 2,
            self.gameDisplay.get_height() // 2 + y_offset
        )
        self.gameDisplay.blit(screen_text, rect)