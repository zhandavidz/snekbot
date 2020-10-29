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
        # black background
        pygame.draw.rect(win, (0, 0, 0), (0, self.display_buffer, self.dimensions[0], self.dimensions[1]))
        # blue strip at the top
        pygame.draw.rect(win, (0, 100, 200), (0, 0, self.dimensions[0], self.display_buffer))

        # add title
        # when display buffer = 50:
        # text = 175px, so round(3.5 * self.display_buffer)
        x = (self.dimensions[0] - (3.5 * self.display_buffer)) // 2
        # height pretty much the size of self.display_buffer, size = 50px
        # when font size = 50, x = 30, so y = self.display_buffer * 1 // 5
        y = self.display_buffer * 1 // 5
        title_font = pygame.font.SysFont("sansserif", self.display_buffer)
        title = title_font.render("SNEKBOT", 1, (255,255,255))
        win.blit(title, (x, y))

        for checker in self.checkers:
            checker.draw(win)

class snek(object):
    def __init__(self, segment_width):
        self.length = 1
        self.x_pixel = 0
        self.y_pixel = 0
        self.segment_width = segment_width
        vel = 5

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), (self.x_pixel, self.y_pixel, self.segment_width, self.segment_width))

# initialize the board
board = board(25, 24, 24, 50)
snek = snek(25)


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
    snek.draw(win)

    # refresh the window
    pygame.display.update()

pygame.quit()
