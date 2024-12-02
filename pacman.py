import math
import pygame
from board import boards

# Initialize pygame environment
pygame.init()

# Define the pygame parameters 
WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # setting pygame display dimensions
timer = pygame.time.Clock()  # Control the speed at which the game run
fps = 60
font = pygame.font.Font("freesansbold.ttf", 20)
level = boards  # import the lists of level (layout components) - the level is constructed by multiple tiles
flicker = False # flicker control for the BIG white dots

PI = math.pi

# Define the player's parameters
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))  # animating the player biting using multiple images
player_x = 450
player_y = 663
direction = 0  # Initial direction of the player - right
counter = 0  # for cycling through images to create the animations

# ---------------------------------------------------------------------------------------

# Draw the layout of the game
def draw_board():
    num1 = ((HEIGHT - 50) // 32)    # How tall each tile should be
    num2 = (WIDTH // 30)            # How wide each tile should be
    
    # iterate through every tiles inside the pacman board
    for i in range(len(level)):
        for j in range(len(level[i])):

            # if the tile's value is 1, then it is a white dot
            if level[i][j] == 1:
                pygame.draw.circle(screen, "white", (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)  # pygame.draw.circle(surface to draw, color, center's x coordinate, center's y coordinate, radius)

            # if the tile's value is 2, then it is a BIG white dot
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, "white", (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10) 

            # 3 is the value of a vertical line
            if level[i][j] == 3:
                pygame.draw.line(screen, "blue", ((j * num2 + (0.5 * num2)), (i * num1)),
                                                ((j * num2 + (0.5 * num2)), (i * num1 + num1)), 3)  # pygame.draw.circle(surface, color, (upperx, upper y), (lower x, lower y), thickness)
                
            # 4 is the value of a BLUE horizontal line
            if level[i][j] == 4:
                pygame.draw.line(screen, "blue", ((j * num2), (i * num1 + (0.5 * num1))),
                                                ((j * num2 + num2), (i * num1 + (0.5 * num1))), 3)  # pygame.draw.circle(surface, color, (left x, left y), (right x, right y), thickness)
                
            # 5 is the value of upper right arc
            if level[i][j] == 5:
                pygame.draw.arc(screen, "blue", [(j * num2 - (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)

            # 6 is the value of upper left arc
            if level[i][j] == 6:
                pygame.draw.arc(screen, "blue",
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)

            # 7 is the value of lower left arc
            if level[i][j] == 7:
                pygame.draw.arc(screen, "blue", [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)

            # 8 is the value of lower right arc
            if level[i][j] == 8:
                pygame.draw.arc(screen, "blue", [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)

            # 9 is the value of a WHITE horizontal line - gate for the ghosts
            if level[i][j] == 9:
                pygame.draw.line(screen, "white", ((j * num2), (i * num1 + (0.5 * num1))),
                                                ((j * num2 + num2), (i * num1 + (0.5 * num1))), 3)  # pygame.draw.circle(surface, color, (left x, left y), (right x, right y), thickness)
                
def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

def check_position(centerx, centery):
    # Checking if the current position is allowed to move in certain direction
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


# ---------------------------------------------------------------------------------------

# Start the game loop
run = True
while run:
    # While the game is running, all the following will be continously executed
    timer.tick(fps)         # Define the frame rate

    if counter < 19:
        # cycling the biting animation
        counter += 1
        if counter > 10:
            flicker = False
    else:
        counter = 0
        flicker = True

    screen.fill('black')    # Create the solid black background for the game
    draw_board()
    draw_player()

    center_x = player_x + 23
    center_y = player_y + 24
    turns_allowed = check_position(center_x, center_y)  # check if the player hit obstacles

    # Check for conditions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # termination condition
            run = False
        if event.type == pygame.KEYDOWN:    # detect key presses
            if event.key == pygame.K_RIGHT: # right arrow key
                direction = 0
            if event.key == pygame.K_LEFT:
                direction = 1
            if event.key == pygame.K_UP:
                direction = 2
            if event.key == pygame.K_DOWN:
                direction = 3

    pygame.display.flip()   # Let everything be drawn on the screen every iteration

pygame.quit()
