import pygame
from .constants import *

class Menu:
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.input_width = str(0)
        self.input_height = str(0)
        self.input_mines = str(0)
        self.active_input = None
        self.error_message = ""

    def draw(self):
        self.gameDisplay.fill(BG_COLOR)
        
        # Draw text labels
        self.draw_text("Set Grid Size", 40, -340)
        self.draw_text("Width:", 30, -295)
        self.draw_text("Height:", 30, -195)
        self.draw_text("Mines:", 30, -95)

        # Draw input boxes
        box_width, box_height = 140, 40
        width_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - box_width // 2,
            180, box_width, box_height
        )
        height_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - box_width // 2,
            280, box_width, box_height
        )
        mines_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - box_width // 2,
            380, box_width, box_height
        )
        start_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - 100,
            460, 200, 50
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
        
        # Render text
        start_text = pygame.font.SysFont("Calibri", 30).render("START", True, (255, 255, 255))
        self.gameDisplay.blit(start_text, (start_box.x + 70, start_box.y + 15))

        # Render user input
        for box, text in [(width_box, self.input_width), 
                         (height_box, self.input_height), 
                         (mines_box, self.input_mines)]:
            screen_text = pygame.font.SysFont("Calibri", 30).render(text, True, BLACK)
            self.gameDisplay.blit(screen_text, (box.x + 10, box.y + 5))

        # Error message
        if self.error_message:
            self.draw_text(self.error_message, 25, 200)

        pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            result = self.handle_mouse_click(event.pos)
            print(f"Returned from handle_mouse_click: {result}") 
            return result  # Directly return the result from handle_mouse_click !!
        elif event.type == pygame.KEYDOWN and self.active_input:
            self.handle_key_input(event)
        
        return None  # Only return None if no valid result !!!!!!!!!


    def handle_mouse_click(self, pos):
        box_width, box_height = 140, 40
        width_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - box_width // 2,
            180, box_width, box_height
        )
        height_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - box_width // 2,
            280, box_width, box_height
        )
        mines_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - box_width // 2,
            380, box_width, box_height
        )
        start_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - 100,
            460, 200, 50
        )

        self.active_input = None
        if width_box.collidepoint(pos):
            self.active_input = "width"
        elif height_box.collidepoint(pos):
            self.active_input = "height"
        elif mines_box.collidepoint(pos):
            self.active_input = "mines"
        elif start_box.collidepoint(pos):
            print("work")  # This shows we're clicking START
            result = self.validate_inputs()
            print(f"Validation result: {result}")  
            return result

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
            
            print(f"[DEBUG] Validating: Width={w}, Height={h}, Mines={m}")
            
            if w < 3 or h < 3 or m < 3:
                print("[DEBUG] Validation failed: Negative values")
                self.error_message = "Values must be superior or equal to 3 also not be negative"
                return None
            elif m >= w * h:
                print("[DEBUG] Validation failed: Too many mines")
                self.error_message = "Too many mines"
                return None
            else:
                print("[DEBUG] Validation successful!")
                return w, h, m
        except ValueError:
            print("[DEBUG] Validation failed: Invalid numbers")
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