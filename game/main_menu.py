import pygame
from .constants import *

class MainMenu:
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.options = ["Facile", "Moyen", "Difficile", "Sandbox", "Record"]
        self.selected_option = None

    def draw(self):
        self.gameDisplay.fill(BG_COLOR)
        self.draw_text("Démineur", 40, -300)

        # Dessiner les boutons
        button_width, button_height = 200, 50
        for idx, option in enumerate(self.options):
            button_rect = pygame.Rect(
                self.gameDisplay.get_width() // 2 - button_width // 2,
                200 + idx * 80, button_width, button_height
            )
            pygame.draw.rect(self.gameDisplay, (0, 200, 0), button_rect)
            option_text = pygame.font.SysFont("Calibri", 30).render(option, True, (255, 255, 255))
            self.gameDisplay.blit(option_text, (button_rect.x + 50, button_rect.y + 10))

        pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for idx, option in enumerate(self.options):
                button_rect = pygame.Rect(
                    self.gameDisplay.get_width() // 2 - 200 // 2,
                    200 + idx * 80, 200, 50
                )
                if button_rect.collidepoint(event.pos):
                    print(f"Option sélectionnée : {option}")
                    self.selected_option = option
                    return option  # Renvoie l'option sélectionnée

        return None  # Aucune option sélectionnée

    def draw_text(self, text, size, y_offset=0):
        font = pygame.font.SysFont("Calibri", size, True)
        screen_text = font.render(text, True, BLACK)
        rect = screen_text.get_rect()
        rect.center = (
            self.gameDisplay.get_width() // 2,
            self.gameDisplay.get_height() // 2 + y_offset
        )
        self.gameDisplay.blit(screen_text, rect)
