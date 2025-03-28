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
        
        
        # Cyberpunk fonts
        self.title_font = pygame.font.Font(None, 60)
        self.header_font = pygame.font.Font(None, 35)
        self.row_font = pygame.font.Font(None, 30)

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

    def draw(self):
        self.gameDisplay.fill(BG_COLOR)
        
        # Circuit background
        self._draw_circuit_background()
        
        # Title with glitch effect
        title_text = self.title_font.render("Hall of Fame", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(
            self.gameDisplay.get_width() // 2,
            50
        ))
        self.gameDisplay.blit(title_text, title_rect)
        
        # Scores display area
        score_area = pygame.Rect(
            50, 120, 
            self.gameDisplay.get_width() - 100, 
            self.gameDisplay.get_height() - 200
        )
        pygame.draw.rect(self.gameDisplay, BUTTON_COLOR, score_area)
        pygame.draw.rect(self.gameDisplay, ACCENT_COLOR, score_area, 2)
        
        # Column headers
        headers = ["Rank", "Time", "Name", "Difficulty"]
        for i, header in enumerate(headers):
            x = score_area.x + 10 + i * (score_area.width // 4)
            header_text = self.header_font.render(header, True, ACCENT_COLOR)
            self.gameDisplay.blit(header_text, (x, score_area.y + 10))
        
        # Display scores
        y_pos = score_area.y + 50
        for idx, score in enumerate(self.scores[:20]):  # Show top 20
            # Alternating row colors for better readability
            row_color = TEXT_COLOR if idx % 2 == 0 else (0, 200, 255)
            
            # Rank
            rank_text = self.row_font.render(f"{idx + 1}.", True, row_color)
            self.gameDisplay.blit(rank_text, (score_area.x + 20, y_pos))
            
            # Time
            time_text = self.row_font.render(f"{score['time']}s", True, row_color)
            self.gameDisplay.blit(time_text, (score_area.x + 100, y_pos))
            
            # Name
            name_text = self.row_font.render(score['name'], True, row_color)
            self.gameDisplay.blit(name_text, (score_area.x + 250, y_pos))
            
            # Difficulty
            diff_text = self.row_font.render(score['difficulty'], True, row_color)
            self.gameDisplay.blit(diff_text, (score_area.x + 400, y_pos))
            
            y_pos += 30
        
        # Back button with cyberpunk style
        back_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - 100,
            self.gameDisplay.get_height() - 80, 
            200, 50
        )
        pygame.draw.rect(self.gameDisplay, BUTTON_COLOR, back_box)
        pygame.draw.rect(self.gameDisplay, ACCENT_COLOR, back_box, 2)
        
        back_text = self.row_font.render("Back to Menu", True, TEXT_COLOR)
        back_text_rect = back_text.get_rect(center=back_box.center)
        self.gameDisplay.blit(back_text, back_text_rect)
        
        pygame.display.update()

    def _draw_circuit_background(self):
        # Draw grid-like circuit background
        for x in range(0, self.gameDisplay.get_width(), 30):
            pygame.draw.line(self.gameDisplay, (20, 40, 60), (x, 0), (x, self.gameDisplay.get_height()), 1)
        for y in range(0, self.gameDisplay.get_height(), 30):
            pygame.draw.line(self.gameDisplay, (20, 40, 60), (0, y), (self.gameDisplay.get_width(), y), 1)

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