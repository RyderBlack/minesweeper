import pygame
from .constants import *


class Menu:
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.input_width = ""
        self.input_height = ""
        self.input_mines = ""
        self.active_input = None
        self.error_message = ""
        self.font_title = pygame.font.Font(None, 50)
        self.font_labels = pygame.font.Font(None, 35)
        self.font_input = pygame.font.Font(None, 40)

    def draw(self):
        self.gameDisplay.fill(BG_COLOR)
        
        # Circuit background
        self._draw_circuit_background()
        
        # Draw cyberpunk title
        title_text = self.font_title.render("Grid Configuration", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(
            self.gameDisplay.get_width() // 2,
            100
        ))
        self.gameDisplay.blit(title_text, title_rect)

        # Draw input labels and boxes
        labels = [
            ("Width", 180, "width", 1, 30),
            ("Height", 280, "height", 1, 3),
            ("Mines", 380, "mines", 3, None)
        ]

        for label, y_pos, input_type, min_val, max_val in labels:
            # Label
            label_text = self.font_labels.render(label, True, TEXT_COLOR)
            label_rect = label_text.get_rect(center=(
                self.gameDisplay.get_width() // 2 - 100,
                y_pos
            ))
            self.gameDisplay.blit(label_text, label_rect)

            # Input box
            box_width, box_height = 200, 50
            box_rect = pygame.Rect(
                self.gameDisplay.get_width() // 2 - box_width // 2,
                y_pos + 30, box_width, box_height
            )
            
            # Cyberpunk input box
            pygame.draw.rect(self.gameDisplay, BUTTON_COLOR, box_rect)
            border_color = ACCENT_COLOR if self.active_input == input_type else (50, 80, 120)
            pygame.draw.rect(self.gameDisplay, border_color, box_rect, 2)

            # Input text
            input_text = getattr(self, f"input_{input_type}")
            rendered_text = self.font_input.render(input_text, True, TEXT_COLOR)
            text_rect = rendered_text.get_rect(center=box_rect.center)
            self.gameDisplay.blit(rendered_text, text_rect)

        # Start button - moved lower
        start_box = pygame.Rect(
            self.gameDisplay.get_width() // 2 - 125,
            520, 250, 60  # Moved lower
        )
        pygame.draw.rect(self.gameDisplay, BUTTON_COLOR, start_box)
        pygame.draw.rect(self.gameDisplay, ACCENT_COLOR, start_box, 2)
        
        start_text = self.font_input.render("START", True, TEXT_COLOR)
        start_text_rect = start_text.get_rect(center=start_box.center)
        self.gameDisplay.blit(start_text, start_text_rect)

        # Error message
        if self.error_message:
            error_text = self.font_labels.render(self.error_message, True, (255, 50, 50))
            error_rect = error_text.get_rect(center=(
                self.gameDisplay.get_width() // 2,
                590  # Adjusted to be below start button
            ))
            self.gameDisplay.blit(error_text, error_rect)

        pygame.display.update()

    def _draw_circuit_background(self):
        # Draw grid-like circuit background
        for x in range(0, self.gameDisplay.get_width(), 30):
            pygame.draw.line(self.gameDisplay, (20, 40, 60), (x, 0), (x, self.gameDisplay.get_height()), 1)
        for y in range(0, self.gameDisplay.get_height(), 30):
            pygame.draw.line(self.gameDisplay, (20, 40, 60), (0, y), (self.gameDisplay.get_width(), y), 1)


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
            
            if w < 1 or w > 30 or h < 1 or h > 30:
                self.error_message = "Width/Height between 1-30"
                return None
            
            if m < 3:
                self.error_message = "Minimum 3 mines"
                return None
            
            if m >= w * h:
                self.error_message = "Too many mines"
                return None
            
            return w, h, m
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