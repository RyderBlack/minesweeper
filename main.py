import pygame
import os
import sys
from game.core import GameCore
from game.menu import Menu
from game.main_menu import MainMenu
from game.constants import *
from game.hall_of_fame import *
# Presets pour les niveaux de difficulté
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
    
    # Initialize display with default size
    gameDisplay = pygame.display.set_mode((
        GRID_SIZE * DEFAULT_WIDTH + BORDER * 2,
        GRID_SIZE * DEFAULT_HEIGHT + BORDER + TOP_BORDER
    ))
    pygame.display.set_caption("Minesweeper")
    
    # Load sprites
    sprites = load_sprites()
    
    # Game objects
    main_menu = MainMenu(gameDisplay)
    menu = Menu(gameDisplay)
    game = GameCore()
    hall_of_fame = HallOfFame(gameDisplay)  # Add Hall of Fame instance
    clock = pygame.time.Clock()
    current_screen = "main_menu"  # Default screen is the Main Menu
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if current_screen == "main_menu":
                selected_option = main_menu.handle_event(event)
                if selected_option == "Sandbox":
                    current_screen = "sandbox_menu"
                elif selected_option in DIFFICULTY_PRESETS:
                # Utiliser les préréglages pour initialiser la grille
                    preset = DIFFICULTY_PRESETS[selected_option]
                    game.initialize_grid(preset["width"], preset["height"], preset["mines"])
                    
                    # Redimensionner l'affichage
                    gameDisplay = pygame.display.set_mode((
                        GRID_SIZE * preset["width"] + BORDER * 2,
                        GRID_SIZE * preset["height"] + BORDER + TOP_BORDER
                    ))
                    current_screen = "game"  # Passer à l'écran du jeu
                elif selected_option == "Record":  # Switch to Hall of Fame
                    current_screen = "hall_of_fame"

            elif current_screen == "sandbox_menu":
                result = menu.handle_event(event)
                print(f"Menu handle_event returned: {result}")
                if result:  # User clicked START with valid inputs
                    width, height, mines = result
                    print(f"\n[DEBUG MAIN] Starting game with: {width}x{height}, {mines} mines") 
                    game.initialize_grid(width, height, mines)
                    
                    # Resize display
                    gameDisplay = pygame.display.set_mode((
                        GRID_SIZE * width + BORDER * 2,
                        GRID_SIZE * height + BORDER + TOP_BORDER
                    ))
                    menu.gameDisplay = gameDisplay
                    current_screen = "game"
            elif current_screen == "game":
                if game.game_state in ["Game Over", "Win"]:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game.game_state = "Playing"
                            current_screen = "main_menu"
                else:
                    if event.type == pygame.MOUSEBUTTONUP:
                        game.handle_click(event.pos, event.button, gameDisplay)
                        game.check_win()
            elif current_screen == "hall_of_fame":
                result = hall_of_fame.handle_event(event)

                if result == "menu":  # Go back to Main Menu
                    current_screen = "main_menu"
        # Drawing
        if current_screen == "main_menu":
            main_menu.draw()
        elif current_screen == "sandbox_menu":
            menu.draw()
        elif current_screen == "game":
            gameDisplay.fill(BG_COLOR)
            game.draw(gameDisplay, sprites)
            pygame.display.update()
        elif current_screen == "hall_of_fame":
            hall_of_fame.draw()
        clock.tick(15)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
