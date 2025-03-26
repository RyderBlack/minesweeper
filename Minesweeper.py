import pygame
import random
pygame.init()
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
image_path = os.path.join(BASE_DIR, "assets/Sprites", "empty.png")

bg_color = (192, 192, 192)
grid_color = (128, 128, 128)

game_width = 10  # Change this to increase size
game_height = 10  # Change this to increase size
numMine = 9  # Number of mines
grid_size = 32  # Size of grid (WARNING: macke sure to change the images dimension as well)
border = 16  # Top border
top_border = 100  # Left, Right, Bottom border
display_width = grid_size * game_width + border * 2  # Display width
display_height = grid_size * game_height + border + top_border  # Display height
gameDisplay = pygame.display.set_mode((display_width, display_height))  # Create display
timer = pygame.time.Clock()  # Create timer
pygame.display.set_caption("Minesweeper")  # S Set the caption of window

# Import files
spr_emptyGrid = pygame.image.load("assets/Sprites/empty.png")
spr_flag = pygame.image.load("assets/Sprites/flag.png")
spr_grid = pygame.image.load("assets/Sprites/Grid.png")
spr_grid1 = pygame.image.load("assets/Sprites/grid1.png")
spr_grid2 = pygame.image.load("assets/Sprites/grid2.png")
spr_grid3 = pygame.image.load("assets/Sprites/grid3.png")
spr_grid4 = pygame.image.load("assets/Sprites/grid4.png")
spr_grid5 = pygame.image.load("assets/Sprites/grid5.png")
spr_grid6 = pygame.image.load("assets/Sprites/grid6.png")
spr_grid7 = pygame.image.load("assets/Sprites/grid7.png")
spr_grid8 = pygame.image.load("assets/Sprites/grid8.png")
spr_grid7 = pygame.image.load("assets/Sprites/grid7.png")
spr_mine = pygame.image.load("assets/Sprites/mine.png")
spr_question = pygame.image.load("assets/Sprites/question_mark.png")
spr_mineClicked = pygame.image.load("assets/Sprites/mineClicked.png")
spr_mineFalse = pygame.image.load("assets/Sprites/mineFalse.png")


# Create global values
grid = []  # The main grid
mines = []  # Pos of the mines


# Create funtion to draw texts
def drawText(txt, s, yOff=0):
    screen_text = pygame.font.SysFont("Calibri", s, True).render(txt, True, (0, 0, 0))
    rect = screen_text.get_rect()
    rect.center = (game_width * grid_size / 2 + border, game_height * grid_size / 2 + top_border + yOff)
    gameDisplay.blit(screen_text, rect)


# Create class grid
class Grid:
    def __init__(self, xGrid, yGrid, type):
        self.xGrid = xGrid  # X pos of grid
        self.yGrid = yGrid  # Y pos of grid
        self.clicked = False  # Boolean var to check if the grid has been clicked
        self.mineClicked = False  # Bool var to check if the grid is clicked and its a mine
        self.mineFalse = False  # Bool var to check if the player flagged the wrong grid
        self.flag = False  # Bool var to check if player flagged the grid
        self.question = False #Bool var to check if player questioned the grid 
        # Create rectObject to handle drawing and collisions
        self.rect = pygame.Rect(border + self.xGrid * grid_size, top_border + self.yGrid * grid_size, grid_size, grid_size)
        self.val = type  # Value of the grid, -1 is mine

    def drawGrid(self):
        # Draw the grid according to bool variables and value of grid
        if self.mineFalse:
            gameDisplay.blit(spr_mineFalse, self.rect)
        else:
            if self.clicked:
                if self.val == -1:
                    if self.mineClicked:
                        gameDisplay.blit(spr_mineClicked, self.rect)
                    else:
                        gameDisplay.blit(spr_mine, self.rect)
                else:
                    if self.val == 0:
                        gameDisplay.blit(spr_emptyGrid, self.rect)
                    elif self.val == 1:
                        gameDisplay.blit(spr_grid1, self.rect)
                    elif self.val == 2:
                        gameDisplay.blit(spr_grid2, self.rect)
                    elif self.val == 3:
                        gameDisplay.blit(spr_grid3, self.rect)
                    elif self.val == 4:
                        gameDisplay.blit(spr_grid4, self.rect)
                    elif self.val == 5:
                        gameDisplay.blit(spr_grid5, self.rect)
                    elif self.val == 6:
                        gameDisplay.blit(spr_grid6, self.rect)
                    elif self.val == 7:
                        gameDisplay.blit(spr_grid7, self.rect)
                    elif self.val == 8:
                        gameDisplay.blit(spr_grid8, self.rect)

            else:
                if self.flag:
                    gameDisplay.blit(spr_flag, self.rect)
                elif self.question:
                    gameDisplay.blit(spr_question, self.rect)
                else:
                    gameDisplay.blit(spr_grid, self.rect)

    def revealGrid(self):
        self.clicked = True
        # Auto reveal if it's a 0
        if self.val == 0:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if not grid[self.yGrid + y][self.xGrid + x].clicked:
                                grid[self.yGrid + y][self.xGrid + x].revealGrid()
        elif self.val == -1:
            # Auto reveal all mines if it's a mine
            for m in mines:
                if not grid[m[1]][m[0]].clicked:
                    grid[m[1]][m[0]].revealGrid()

    def updateValue(self):
        # Update the value when all grid is generated
        if self.val != -1:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if grid[self.yGrid + y][self.xGrid + x].val == -1:
                                self.val += 1


def gameLoop():
    gameState = "Playing"  # Game state
    mineLeft = numMine  # Number of mine left
    global grid  # Access global var
    grid = []
    global mines
    t = 0  # Set time to 0

    # Generating mines
    mines = [[random.randrange(0, game_width),
              random.randrange(0, game_height)]]

    for c in range(numMine - 1):
        pos = [random.randrange(0, game_width),
               random.randrange(0, game_height)]
        same = True
        while same:
            for i in range(len(mines)):
                if pos == mines[i]:
                    pos = [random.randrange(0, game_width), random.randrange(0, game_height)]
                    break
                if i == len(mines) - 1:
                    same = False
        mines.append(pos)

    # Generating entire grid
    for j in range(game_height):
        line = []
        for i in range(game_width):
            if [i, j] in mines:
                line.append(Grid(i, j, -1))
            else:
                line.append(Grid(i, j, 0))
        grid.append(line)

    # Update of the grid
    for i in grid:
        for j in i:
            j.updateValue()

    # Main Loop
    while gameState != "Exit":
        # Reset screen
        gameDisplay.fill(bg_color)

        # User inputs
        for event in pygame.event.get():
            # Check if player close window
            if event.type == pygame.QUIT:
                gameState = "Exit"
            # Check if play restart
            if gameState == "Game Over" or gameState == "Win":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        gameLoop()
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    for i in grid:
                        for j in i:
                            if j.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    # If player left clicked of the grid
                                    j.revealGrid()
                                    # Toggle flag off
                                    if j.flag:
                                        mineLeft += 1
                                        j.flag = False
                                    # If it's a mine
                                    if j.val == -1:
                                        gameState = "Game Over"
                                        j.mineClicked = True
                                elif event.button == 3:
                                    if not j.clicked:
                                        if not j.flag and not j.question:
                                            j.flag = True
                                            mineLeft -= 1
                                        elif j.flag and not j.question:
                                            j.flag = False
                                            j.question = True
                                            mineLeft += 1
                                        elif not j.flag and j.question:
                                            j.question = False

        # Check if won
        w = True
        for i in grid:
            for j in i:
                j.drawGrid()
                if j.val != -1 and not j.clicked:
                    w = False
        if w and gameState != "Exit":
            gameState = "Win"

        # Draw Texts
        if gameState != "Game Over" and gameState != "Win":
            t += 1
        elif gameState == "Game Over":
            drawText("Game Over!", 50)
            drawText("R to restart", 35, 50)
            for i in grid:
                for j in i:
                    if j.flag and j.val != -1:
                        j.mineFalse = True
        else:
            drawText("You WON!", 50)
            drawText("R to restart", 35, 50)
        # Draw time
        s = str(t // 15)
        screen_text = pygame.font.SysFont("Calibri", 50).render(s, True, (0, 0, 0))
        gameDisplay.blit(screen_text, (border, border))
        # Draw mine left
        screen_text = pygame.font.SysFont("Calibri", 50).render(mineLeft.__str__(), True, (0, 0, 0))
        gameDisplay.blit(screen_text, (display_width - border - 50, border))

        pygame.display.update()  # Update screen

        timer.tick(15)  # Tick fps

def menu():
    global game_width, game_height, numMine, display_width, display_height, gameDisplay

    running = True
    input_width = ""
    input_height = ""
    input_mines = ""
    active_input = None
    error_message = ""

    # Define input box positions
    box_width, box_height = 140, 40
    width_box = pygame.Rect(display_width // 2 - box_width // 2, 150, box_width, box_height)
    height_box = pygame.Rect(display_width // 2 - box_width // 2, 220, box_width, box_height)
    mines_box = pygame.Rect(display_width // 2 - box_width // 2, 290, box_width, box_height)
    start_box = pygame.Rect(display_width // 2 - 100, 360, 200, 50)

    while running:
        gameDisplay.fill(bg_color)

        # Draw text labels
        drawText("Set Grid Size", 40, -120)
        drawText("Width:", 30, -50)
        drawText("Height:", 30, 20)
        drawText("Mines:", 30, 90)

        # Draw input boxes
        pygame.draw.rect(gameDisplay, (255, 255, 255), width_box, 2 if active_input == "width" else 1)
        pygame.draw.rect(gameDisplay, (255, 255, 255), height_box, 2 if active_input == "height" else 1)
        pygame.draw.rect(gameDisplay, (255, 255, 255), mines_box, 2 if active_input == "mines" else 1)
        pygame.draw.rect(gameDisplay, (0, 200, 0), start_box)
        
        # Render text
        screen_text = pygame.font.SysFont("Calibri", 30).render("START", True, (255, 255, 255))
        gameDisplay.blit(screen_text, (start_box.x + 70, start_box.y + 15))

        # Render user input
        for box, text in [(width_box, input_width), (height_box, input_height), (mines_box, input_mines)]:
            screen_text = pygame.font.SysFont("Calibri", 30).render(text, True, (0, 0, 0))
            gameDisplay.blit(screen_text, (box.x + 10, box.y + 5))

        # Error message
        if error_message:
            drawText(error_message, 25, 200)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                active_input = None
                if width_box.collidepoint(event.pos):
                    active_input = "width"
                elif height_box.collidepoint(event.pos):
                    active_input = "height"
                elif mines_box.collidepoint(event.pos):
                    active_input = "mines"
                elif start_box.collidepoint(event.pos) and input_width and input_height and input_mines:
                    try:
                        w = int(input_width)
                        h = int(input_height)
                        m = int(input_mines)
                        
                        if w < 1 or h < 1 or m < 1:
                            error_message = "Values must be positive"
                        elif m >= w * h:
                            error_message = "Too many mines"
                        else:
                            game_width = w
                            game_height = h
                            numMine = m
                            display_width = max(300, grid_size * game_width + border * 2)
                            display_height = max(400, grid_size * game_height + border + top_border)
                            gameDisplay = pygame.display.set_mode((display_width, display_height))
                            running = False
                            gameLoop()
                    except ValueError:
                        error_message = "Invalid numbers"

            if event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_BACKSPACE:
                    if active_input == "width":
                        input_width = input_width[:-1]
                    elif active_input == "height":
                        input_height = input_height[:-1]
                    elif active_input == "mines":
                        input_mines = input_mines[:-1]
                elif event.unicode.isdigit():
                    if active_input == "width":
                        input_width += event.unicode
                    elif active_input == "height":
                        input_height += event.unicode
                    elif active_input == "mines":
                        input_mines += event.unicode

                if event.key == pygame.K_RETURN and input_width and input_height and input_mines:
                    game_width = int(input_width)
                    game_height = int(input_height)
                    numMine = int(input_mines)

                    # Adjust display size dynamically
                    display_width = grid_size * game_width + border * 2
                    display_height = grid_size * game_height + border + top_border
                    gameDisplay = pygame.display.set_mode((display_width, display_height))

                    running = False
                    gameLoop()


menu()
pygame.quit()
quit()