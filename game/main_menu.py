import pygame
from .constants import *
import random

class MainMenu:
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.options = ["Facile", "Moyen", "Difficile", "Sandbox", "Record"]
        self.selected_option = None
        
        self.font_title = pygame.font.Font(None, 60) 
        self.font_buttons = pygame.font.Font(None, 40)
        
        # Glitch effect variables
        self.glitch_timer = 0
        self.glitch_interval = 30
        
        # Load background image
        try:
            # Adjust the path to where your background image is located
            background_path = os.path.join('assets', 'background.png')
            self.background = pygame.image.load(background_path).convert()
            
            # Resize background to fit the display
            self.background = pygame.transform.scale(self.background, 
                                                     (self.gameDisplay.get_width(), 
                                                      self.gameDisplay.get_height()))
        except Exception as e:
            print(f"Could not load background image: {e}")
            self.background = None


    def draw(self):
        if self.background:
            self.gameDisplay.blit(self.background, (0, 0))
        else:
            # Fallback to original background
            self.gameDisplay.fill(BG_COLOR)
            self._draw_circuit_background()
        
        # Glitchy title
        self._draw_glitchy_title()

        # Cyberpunk buttons
        button_width, button_height = 250, 60
        for idx, option in enumerate(self.options):
            button_rect = pygame.Rect(
                self.gameDisplay.get_width() // 2 - button_width // 2,
                250 + idx * 80, button_width, button_height
            )
            
            # Slightly darken the background behind buttons for readability
            s = pygame.Surface((button_width, button_height))
            s.set_alpha(128)  # Transparency level
            s.fill((0, 0, 0))
            self.gameDisplay.blit(s, button_rect.topleft)
            
            # Cyberpunk button design
            pygame.draw.rect(self.gameDisplay, BUTTON_COLOR, button_rect)
            pygame.draw.rect(self.gameDisplay, ACCENT_COLOR, button_rect, 2)
            
            # Hover effect
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.gameDisplay, BUTTON_HOVER_COLOR, button_rect, 3)
            
            # Button text
            option_text = self.font_buttons.render(option, True, TEXT_COLOR)
            text_rect = option_text.get_rect(center=button_rect.center)
            self.gameDisplay.blit(option_text, text_rect)

        pygame.display.update()

    def _draw_circuit_background(self):
        # Draw grid-like circuit background
        for x in range(0, self.gameDisplay.get_width(), 30):
            pygame.draw.line(self.gameDisplay, (20, 40, 60), (x, 0), (x, self.gameDisplay.get_height()), 1)
        for y in range(0, self.gameDisplay.get_height(), 30):
            pygame.draw.line(self.gameDisplay, (20, 40, 60), (0, y), (self.gameDisplay.get_width(), y), 1)

    def _draw_glitchy_title(self):
        # Glitch effect for title
        self.glitch_timer += 1
        title_text = self.font_title.render("Cyber Minesweeper", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(
            self.gameDisplay.get_width() // 2,
            150
        ))
        
        # Occasional glitch effect
        if self.glitch_timer % self.glitch_interval == 0:
            offset_x = pygame.math.Vector2(title_rect.topleft).x + (random.randint(-10, 10))
            offset_y = pygame.math.Vector2(title_rect.topleft).y + (random.randint(-5, 5))
            
            # Draw glitchy duplicates
            glitch_text1 = self.font_title.render("Cyber Minesweeper", True, (0, 255, 100))
            glitch_text2 = self.font_title.render("Cyber Minesweeper", True, (255, 0, 100))
            
            self.gameDisplay.blit(glitch_text1, (offset_x-2, offset_y-2))
            self.gameDisplay.blit(glitch_text2, (offset_x+2, offset_y+2))
        
        # Draw main title
        self.gameDisplay.blit(title_text, title_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for idx, option in enumerate(self.options):
                button_rect = pygame.Rect(
                    self.gameDisplay.get_width() // 2 - 250 // 2,
                    250 + idx * 80, 250, 60
                )
                if button_rect.collidepoint(event.pos):
                    return option  # Return selected option

        return None  # No option selected

    def draw_text(self, text, size, y_offset=0):
        font = pygame.font.SysFont("Calibri", size, True)
        screen_text = font.render(text, True, BLACK)
        rect = screen_text.get_rect()
        rect.center = (
            self.gameDisplay.get_width() // 2,
            self.gameDisplay.get_height() // 2 + y_offset
        )
        self.gameDisplay.blit(screen_text, rect)
