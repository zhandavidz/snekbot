# import relevant libraries
# you may have to install pygame with: python3 -m pip install -U pygame --user
import pygame

# initialize pygame
pygame.init()

# set window dimensions
screen_width = 600
screen_height = 600

win = pygame.display.set_mode((screen_width, screen_height))

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

    # refresh the window
    pygame.display.update()

pygame.quit()
