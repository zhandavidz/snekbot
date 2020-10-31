# import relevant libraries
# you may have to install pygame with: python3 -m pip install -U pygame --user
import pygame
from components import board

# initialize pygame
pygame.init()

# initialize the board
board = board(25, 24, 24, 50)


# set window dimensions
win = pygame.display.set_mode(board.dimensions)

# set the title of the window
pygame.display.set_caption("Snekbot")

# set the clock used for managing fps in the main loop
clock = pygame.time.Clock()



# main loop
run = True
while run:
    # set the fps
    clock.tick(30)

    # end the loop when the user closes the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        board.snek.set_direction("left")
    elif keys[pygame.K_RIGHT]:
        board.snek.set_direction("right")
    elif keys[pygame.K_UP]:
        board.snek.set_direction("up")
    elif keys[pygame.K_DOWN]:
        board.snek.set_direction("down")


    # draw the board
    board.draw(win)

    # refresh the window
    pygame.display.update()

pygame.quit()
