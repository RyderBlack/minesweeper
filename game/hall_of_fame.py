import pygame
import json
import os
from game.constants import *

# Ajout pour le Hall of Fame : Définition du chemin pour sauvegarder les scores
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCORES_FILE = os.path.join(BASE_DIR, "hall_of_fame.json")

# Ajout pour le Hall of Fame : Classe complète pour gérer le Hall of Fame
class HallOfFame:
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.scores = self.load_scores()
        self.scroll_y = 0
        self.max_display = 50
        self.line_height = 20
        self.max_scroll = max(0, len(self.scores) * self.line_height - 250)

    # Ajout pour le Hall of Fame : Chargement des scores depuis le fichier JSON
    def load_scores(self):
        try:
            if os.path.exists(SCORES_FILE):
                with open(SCORES_FILE, 'r') as f:
                    return json.load(f)
            return []
        except Exception:
            return []

    # Ajout pour le Hall of Fame : Sauvegarde des scores dans le fichier JSON
    def save_scores(self):
        try:
            with open(SCORES_FILE, 'w') as f:
                json.dump(self.scores, f)
        except Exception:
            pass

    # Ajout pour le Hall of Fame : Ajout d’un score avec pseudo
    def add_score(self, time, width, height, mines, name="Anonymous"):
        difficulty = f"{width}x{height}, {mines} mines"
        score_entry = {"time": time, "difficulty": difficulty, "name": str(name)}
        self.scores.append(score_entry)
        self.scores = sorted(self.scores, key=lambda x: x["time"])[:self.max_display]
        self.save_scores()
        self.update_scroll_limit()

    # Ajout pour le Hall of Fame : Mise à jour de la limite de défilement
    def update_scroll_limit(self):
        self.max_scroll = max(0, len(self.scores) * self.line_height - 250)

    # Ajout pour le Hall of Fame : Gestion des événements (défilement et clic sur "Back")
    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_y -= event.y * 20
            self.scroll_y = max(0, min(self.scroll_y, self.max_scroll))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            result = self.handle_mouse_click(event.pos)
            return result
        return None

    # Ajout pour le Hall of Fame : Détection du clic sur le bouton "Back"
    def handle_mouse_click(self, pos):
        back_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - 80,
            350, 160, 40
        )
        if back_box.collidepoint(pos):
            return "menu"
        return None

    # Ajout pour le Hall of Fame : Affichage du Hall of Fame
    def draw(self):
        self.gameDisplay.fill(BG_COLOR)
        
        score_area = pygame.Rect(
            50, 50, 500, 250
        )
        pygame.draw.rect(self.gameDisplay, (255, 255, 255), score_area)
        pygame.draw.rect(self.gameDisplay, BLACK, score_area, 2)

        self.draw_text("Hall of Fame", 40, score_area.x + score_area.width // 2, 30, center=True)

        y_start = score_area.y + 40 - self.scroll_y
        for i, score in enumerate(self.scores):
            y_pos = y_start + i * self.line_height
            if score_area.y + 40 <= y_pos < score_area.y + score_area.height - self.line_height:
                time = score.get("time", 0)
                name = score.get("name", "Anonymous")
                difficulty = score.get("difficulty", "Unknown")
                text = f"{i + 1}. {time}s - {name} - {difficulty}"
                self.draw_text(text, 20, score_area.x + 10, y_pos, center=False)

        if self.max_scroll > 0:
            scrollbar_height = max(30, score_area.height * score_area.height // max(1, len(self.scores) * self.line_height))
            scrollbar_y = score_area.y + (self.scroll_y * (score_area.height - scrollbar_height) // self.max_scroll)
            scrollbar = pygame.Rect(
                score_area.x + score_area.width - 15,
                scrollbar_y, 10, scrollbar_height
            )
            pygame.draw.rect(self.gameDisplay, (150, 150, 150), scrollbar)

        back_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - 80,
            350, 160, 40
        )
        pygame.draw.rect(self.gameDisplay, (200, 0, 0), back_box)
        back_text = pygame.font.SysFont("Calibri", 25).render("Back", True, (255, 255, 255))
        self.gameDisplay.blit(back_text, (back_box.x + 50, back_box.y + 10))

        pygame.display.update()

    # Ajout pour le Hall of Fame : Méthode utilitaire pour dessiner le texte
    def draw_text(self, text, size, x, y, center=False):
        font = pygame.font.SysFont("Calibri", size, True)
        screen_text = font.render(text, True, BLACK)
        rect = screen_text.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.gameDisplay.blit(screen_text, rect)