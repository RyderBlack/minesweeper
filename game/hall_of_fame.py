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
    # In hall_of_fame.py, modify the draw method:
    def draw(self):
        self.gameDisplay.fill(BG_COLOR)
        
        # Title
        self.draw_text("Hall of Fame", 40, self.gameDisplay.get_width() // 2, 30, center=True)
        
        # Difficulty filter buttons
        buttons = [
            ("All", 50, 80),
            ("Facile", 150, 80),
            ("Moyen", 250, 80),
            ("Difficile", 350, 80),
            ("Sandbox", 450, 80)
        ]
        
        for text, x, y in buttons:
            button_rect = pygame.Rect(x, y, 80, 30)
            pygame.draw.rect(self.gameDisplay, (200, 200, 200), button_rect)
            self.draw_text(text, 20, x + 40, y + 15, center=True)
        
        # Scores display area
        score_area = pygame.Rect(
            50, 120, 
            self.gameDisplay.get_width() - 100, 
            self.gameDisplay.get_height() - 180
        )
        pygame.draw.rect(self.gameDisplay, (255, 255, 255), score_area)
        pygame.draw.rect(self.gameDisplay, BLACK, score_area, 2)
        
        # Column headers
        headers = ["Rank", "Time", "Name", "Difficulty"]
        for i, header in enumerate(headers):
            x = score_area.x + 10 + i * 150
            self.draw_text(header, 20, x, score_area.y + 10, center=False)
        
        # Display scores
        y_pos = score_area.y + 40
        for idx, score in enumerate(self.scores[:20]):  # Show top 20
            # Rank
            self.draw_text(f"{idx + 1}.", 18, score_area.x + 20, y_pos, center=False)
            # Time
            self.draw_text(f"{score['time']}s", 18, score_area.x + 100, y_pos, center=False)
            # Name
            self.draw_text(score['name'], 18, score_area.x + 250, y_pos, center=False)
            # Difficulty
            self.draw_text(score['difficulty'], 18, score_area.x + 400, y_pos, center=False)
            
            y_pos += 30
        
        # Back button
        back_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - 80,
            self.gameDisplay.get_height() - 50, 
            160, 40
        )
        pygame.draw.rect(self.gameDisplay, (200, 0, 0), back_box)
        self.draw_text("Back to Menu", 25, back_box.x + 80, back_box.y + 20, center=True)
        
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