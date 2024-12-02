import math
import pygame
from board import boards

# Initialize pygame environment
pygame.init()


# Define the pygame parameters 
fps = 60
WIDTH = 900
HEIGHT = 950
PI = math.pi
level = boards                                      # import the lists of level (layout components) - the level is constructed by multiple tiles
flicker = False                                     # flicker control for the BIG white dots
timer = pygame.time.Clock()                         # Control the speed at which the game run
font = pygame.font.Font("freesansbold.ttf", 20)
screen = pygame.display.set_mode([WIDTH, HEIGHT])   # setting pygame display dimensions


# Define the player's parameters
score = 0
counter = 0             # for cycling through images to create the animations
direction = 0           # Initial direction of the player - right
player_x = 450
player_y = 663
player_speed = 2
player_images = []
direction_command = 0
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))  # animating the player biting using multiple images


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

def check_collisions(score):
    # Calculate the height and width of each tile
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30

    # check if the player's x-coordinate is within the playable area
    if 0 < player_x < 870:
        # Determine the player's current tile position using center coordinates
        if level[center_y // num1][center_x // num2] == 1:  # If current tile contains a SMALL dot (level value 1)
            level[center_y // num1][center_x // num2] = 0   # Remove the dot by switching the level value to 0 (empty tile)
            score += 10
        if level[center_y // num1][center_x // num2] == 2:  # If current tile contains a BIG dot (level value 2)
            level[center_y // num1][center_x // num2] = 0
            score += 50
    
    return score

def move_player(player_x, player_y):
    # r, l, u, d
    if direction == 0 and turns_allowed[0]: # move right
        player_x += player_speed
    elif direction == 1 and turns_allowed[1]: # move left
        player_x -= player_speed
    if direction == 2 and turns_allowed[2]: # move up
        player_y -= player_speed
    elif direction == 3 and turns_allowed[3]: # move down
        player_y += player_speed

    return player_x, player_y

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

    # Returns whether or not we're allowed to turn
    return turns


# ---------------------------------------------------------------------------------------

# Start the game loop
run = True

# While the game is running, all the following will be continously executed
while run:
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
    turns_allowed = check_position(center_x, center_y)      # check if the player hit obstacles
    player_x, player_y = move_player(player_x, player_y)    # move the player as the arrow keys pressed
    score = check_collisions(score)                         # check if the player collides with obstacles and update the score

    # Check for conditions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       # termination condition
            run = False
        if event.type == pygame.KEYDOWN:    # detect key presses
            if event.key == pygame.K_RIGHT: # right arrow key
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
        if event.type == pygame.KEYUP:      # detect key releases
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    # "transport" the player to the opposite side of the board if it goes beyond the borders
    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    pygame.display.flip()   # Let everything be drawn on the screen every iteration

pygame.quit()
