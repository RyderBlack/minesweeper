import pygame
import os
import sys
import time
from game.core import GameCore
from game.menu import Menu
from game.main_menu import MainMenu
from game.constants import *
from game.hall_of_fame import *

#Difficulty settings
DIFFICULTY_PRESETS = {
    "Facile": {"width": 10, "height": 10, "mines": 10},
    "Moyen": {"width": 16, "height": 16, "mines": 32},
    "Difficile": {"width": 20, "height": 20, "mines": 100}
}


def load_sprites():
    sprites = {}
    for name in SPRITE_NAMES:
        try:
            sprites[name] = pygame.image.load(os.path.join(SPRITES_DIR, f"{name}.png"))
        except:
            print(f"Warning: Could not load sprite {name}")
            # Create a placeholder surface if sprite is missing
            sprites[name] = pygame.Surface((GRID_SIZE, GRID_SIZE))
            sprites[name].fill((255, 0, 255))  # Magenta placeholder
    return sprites

def main():
    pygame.init()
    
    MENU_WIDTH = 600 
    MENU_HEIGHT = 800
    
    # Initialize display with default size
    gameDisplay = pygame.display.set_mode((MENU_WIDTH,MENU_HEIGHT))
    pygame.display.set_caption("Cyber Minesweeper")
    
    # Load sprites
    sprites = load_sprites()
    
    # Game objects
    main_menu = MainMenu(gameDisplay)
    menu = Menu(gameDisplay)
    game = GameCore()
    hall_of_fame = HallOfFame(gameDisplay)
    game.hall_of_fame = hall_of_fame  
    
    clock = pygame.time.Clock()
    current_screen = "main_menu"
    running = True
    player_name = "Anonymous"
    game_start_time = 0 
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            
            if current_screen == "main_menu":
                selected_option = main_menu.handle_event(event)
                if selected_option == "Sandbox":
                    current_screen = "sandbox_menu"
                elif selected_option in DIFFICULTY_PRESETS:
                    preset = DIFFICULTY_PRESETS[selected_option]
                    game.initialize_grid(preset["width"], preset["height"], preset["mines"])
                    
                    # Improved display size calculation
                    new_width = preset["width"] * GRID_SIZE + 2 * BORDER
                    new_height = preset["height"] * GRID_SIZE + TOP_BORDER + BORDER
                    gameDisplay = pygame.display.set_mode((new_width, new_height))
                    
                    current_screen = "game"  
                    game_start_time = time.time() 
                elif selected_option == "Record":
                    current_screen = "hall_of_fame"

            elif current_screen == "sandbox_menu":
                result = menu.handle_event(event)
                if result:
                    width, height, mines = result
                    game.initialize_grid(width, height, mines)
                    new_width = width * GRID_SIZE + 2 * BORDER
                    new_height = height * GRID_SIZE + TOP_BORDER + BORDER
                    gameDisplay = pygame.display.set_mode((new_width, new_height))
                    
                    current_screen = "game"
                    game_start_time = time.time()
                    
            elif current_screen == "game":
                if game.game_state in ["Game Over", "Win"]:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game.game_state = "Playing"
                            current_screen = "main_menu"
                            gameDisplay = pygame.display.set_mode((MENU_WIDTH,MENU_HEIGHT))
                        # Handle name input when player wins
                        elif game.game_state == "Win" and event.key != pygame.K_RETURN:
                            if event.key == pygame.K_BACKSPACE:
                                player_name = player_name[:-1]
                            elif len(player_name) < 10 and event.unicode.isalnum():
                                player_name += event.unicode
                            game.player_name = player_name  # Update name in game core
                else:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if time.time() - game_start_time > 0.5:
                            game.handle_click(event.pos, event.button, gameDisplay)
                            game.check_win()  # Now no arguments needed
                        
            elif current_screen == "hall_of_fame":
                result = hall_of_fame.handle_event(event)
                if result == "menu":
                    current_screen = "main_menu"
            
        
        # Drawing
        if current_screen == "main_menu":
            main_menu.draw()
        elif current_screen == "sandbox_menu":
            menu.draw()
        elif current_screen == "game":
            gameDisplay.fill(BG_COLOR)
            game.draw(gameDisplay, sprites)
            # Show name input when player wins
            if game.game_state == "Win":
                font = pygame.font.SysFont("Calibri", 30)
                name_text = font.render(f"Name: {player_name}", True, BLACK)
                gameDisplay.blit(name_text, (gameDisplay.get_width()//2 - 100, gameDisplay.get_height()//2 + 100))
                info_text = font.render("Press R to return to menu", True, BLACK)
                gameDisplay.blit(info_text, (gameDisplay.get_width()//2 - 150, gameDisplay.get_height()//2 + 140))
            pygame.display.update()
        elif current_screen == "hall_of_fame":
            hall_of_fame.draw()
        
        clock.tick(15)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()