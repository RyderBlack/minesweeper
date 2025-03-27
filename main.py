import pygame
import os
import sys
from game.core import GameCore
from game.menu import Menu
from game.hall_of_fame import HallOfFame
from game.constants import *

def load_sprites():
    sprites = {}
    for name in SPRITE_NAMES:
        try:
            sprites[name] = pygame.image.load(os.path.join(SPRITES_DIR, f"{name}.png"))
        except Exception as e:
            sprites[name] = pygame.Surface((GRID_SIZE, GRID_SIZE))
            sprites[name].fill((255, 0, 255))  # Magenta placeholder
    return sprites

def main():
    pygame.init()
    
    gameDisplay = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Minesweeper")
    
    sprites = load_sprites()
    
    menu = Menu(gameDisplay)
    game = GameCore()
    hall_of_fame = HallOfFame(gameDisplay)
    
    clock = pygame.time.Clock()
    in_menu = True
    in_hall_of_fame = False
    # Ajout pour le Hall of Fame : État pour la saisie du pseudo après une victoire
    entering_name = False
    # Ajout pour le Hall of Fame : Variable pour stocker le pseudo saisi
    player_name = ""
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if in_menu:
                result = menu.handle_event(event)
                if result:
                    if result == "hall_of_fame":
                        in_menu = False
                        in_hall_of_fame = True
                    elif isinstance(result, tuple):
                        width, height, mines = result
                        game.initialize_grid(width, height, mines)
                        gameDisplay = pygame.display.set_mode((
                            GRID_SIZE * width + BORDER * 2,
                            GRID_SIZE * height + BORDER + TOP_BORDER
                        ))
                        menu.gameDisplay = gameDisplay
                        hall_of_fame.gameDisplay = gameDisplay
                        in_menu = False
            elif in_hall_of_fame:
                result = hall_of_fame.handle_event(event)
                if result == "menu":
                    in_hall_of_fame = False
                    in_menu = True
                    gameDisplay = pygame.display.set_mode((600, 400))
                    menu.gameDisplay = gameDisplay
                    hall_of_fame.gameDisplay = gameDisplay
            # Ajout pour le Hall of Fame : Gestion de l'état de saisie du pseudo
            elif entering_name:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and player_name.strip():
                        # Ajout pour le Hall of Fame : Enregistrement du score avec le pseudo
                        hall_of_fame.add_score(game.t // 15, game.game_width, game.game_height, game.num_mine, player_name)
                        entering_name = False
                        in_menu = True
                        gameDisplay = pygame.display.set_mode((600, 400))
                        menu.gameDisplay = gameDisplay
                        hall_of_fame.gameDisplay = gameDisplay
                        player_name = ""
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.unicode.isalnum() or event.unicode == " ":
                        if len(player_name) < 15:
                            player_name += event.unicode
            else:  # En jeu
                if game.game_state in ["Game Over", "Win"]:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            in_menu = True
                            gameDisplay = pygame.display.set_mode((600, 400))
                            menu.gameDisplay = gameDisplay
                            hall_of_fame.gameDisplay = gameDisplay
                        # Ajout pour le Hall of Fame : Déclencher la saisie du pseudo après une victoire
                        elif game.game_state == "Win" and event.key == pygame.K_RETURN:
                            entering_name = True
                # Modification pour le Hall of Fame : Changé de MOUSEBUTTONUP à MOUSEBUTTONDOWN (non spécifique au HoF mais ajusté pour cohérence)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game.handle_click(event.pos, event.button, gameDisplay)
                    if game.check_win():
                        game.game_state = "Win"
        
        if in_menu:
            menu.draw()
        elif in_hall_of_fame:
            hall_of_fame.draw()
        # Ajout pour le Hall of Fame : Affichage de l’écran de saisie du pseudo
        elif entering_name:
            gameDisplay.fill(BG_COLOR)
            font = pygame.font.SysFont("Calibri", 40, True)
            prompt_text = font.render("Enter your name:", True, BLACK)
            name_text = font.render(player_name, True, BLACK)
            instruction_text = pygame.font.SysFont("Calibri", 25).render("Press Enter to submit", True, BLACK)
            
            gameDisplay.blit(prompt_text, (gameDisplay.get_width() // 2 - prompt_text.get_width() // 2, 150))
            gameDisplay.blit(name_text, (gameDisplay.get_width() // 2 - name_text.get_width() // 2, 200))
            gameDisplay.blit(instruction_text, (gameDisplay.get_width() // 2 - instruction_text.get_width() // 2, 300))
            pygame.display.update()
        else:
            gameDisplay.fill(BG_COLOR)
            game.draw(gameDisplay, sprites)
            pygame.display.update()
        
        clock.tick(15)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()