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
    
    # Initialize display with default size
    gameDisplay = pygame.display.set_mode((
        GRID_SIZE * DEFAULT_WIDTH + BORDER * 2,
        GRID_SIZE * DEFAULT_HEIGHT + BORDER + TOP_BORDER
    ))
    pygame.display.set_caption("Minesweeper")
    
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
                if result:  # User clicked START with valid inputs
                    width, height, mines = result
                    game.initialize_grid(width, height, mines)
                    
                    # Resize display
                    gameDisplay = pygame.display.set_mode((
                        GRID_SIZE * width + BORDER * 2,
                        GRID_SIZE * height + BORDER + TOP_BORDER
                    ))
                    menu.gameDisplay = gameDisplay
                    in_menu = False
            else:
                if game.game_state in ["Game Over", "Win"]:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
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