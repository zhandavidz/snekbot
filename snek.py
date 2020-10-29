# import relevant libraries
# you may have to install pygame with: python3 -m pip install -U pygame --user
import pygame

# initialize pygame
pygame.init()

class checker_square(object):
    def __init__(self, coords, size):
        self.coords = coords
        self.size = size

    def draw(self, win):
        pygame.draw.rect(win, (40, 40, 40), (self.coords[0], self.coords[1], self.size, self.size))


class board(object):
    def __init__(self, square_width, squares_wide, squares_tall, display_buffer = None):
        self.square_width = square_width # MAY NOT NEED TO BE INSTANCE VARIABLE
        self.squares_wide = squares_wide # MAY NOT NEED TO BE INSTANCE VARIABLE
        self.squares_tall = squares_tall # MAY NOT NEED TO BE INSTANCE VARIABLE
        if display_buffer is None:
            self.display_buffer = square_width
        else:
            self.display_buffer = display_buffer

        self.dimensions = (self.square_width * self.squares_wide, self.square_width * self.squares_tall + self.display_buffer)

        self.checkers = []
        for x_coord in range(0, self.squares_wide * self.square_width, 2 * self.square_width):
            for y_coord in range(self.display_buffer, self.squares_tall * self.square_width + self.display_buffer, 2 * self.square_width):
                self.checkers.append(checker_square((x_coord, y_coord), self.square_width))
                self.checkers.append(checker_square((x_coord + self.square_width, y_coord + self.square_width), self.square_width))

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), (0, self.display_buffer, self.dimensions[0], self.dimensions[1]))
        pygame.draw.rect(win, (0, 100, 200), (0, 0, self.dimensions[0], self.display_buffer))
        for checker in self.checkers:
            checker.draw(win)

# initialize the board
board = board(25, 24, 24, 50)


# set window dimensions
win = pygame.display.set_mode(board.dimensions)
# win = pygame.display.set_mode((700,750))

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

    # draw the board
    board.draw(win)

    # refresh the window
    pygame.display.update()

pygame.quit()
