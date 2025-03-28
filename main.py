import pygame
import os
import sys
from game.core import GameCore
from game.menu import Menu
from game.constants import *

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
    MENU_HEIGHT = 600
    
    # Initialize display with default size
    gameDisplay = pygame.display.set_mode((MENU_WIDTH,MENU_HEIGHT))
    pygame.display.set_caption("Cyber Minesweeper")
    
    # Load sprites
    sprites = load_sprites()
    
    # Game objects
    menu = Menu(gameDisplay)
    game = GameCore()
    
    clock = pygame.time.Clock()
    in_menu = True
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if in_menu:
                result = menu.handle_event(event)
                # print(f"Menu handle_event returned: {result}")  # Menu handle_event returned: None if not
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
                    in_menu = False
                    print("Game started!") 
            else:
                # print("[DEBUG] Game start failed - invalid result")
                if game.game_state in ["Game Over", "Win"]:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game.game_state = "Playing"
                            gameDisplay = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                            menu.gameDisplay = gameDisplay
                            in_menu = True
                else:
                    if event.type == pygame.MOUSEBUTTONUP:
                        game.handle_click(event.pos, event.button, gameDisplay)
                        game.check_win()
        
        # Drawing
        if in_menu:
            menu.draw()
        else:
            gameDisplay.fill(BG_COLOR)
            game.draw(gameDisplay, sprites)
            pygame.display.update()
        
        clock.tick(15)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()