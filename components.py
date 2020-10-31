import pygame

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

        self.obstacles = [self.add_apple(3,3)]

        checker_coords = (0, self.display_buffer)
        self.checkers = []
        for x_coord in range(0, self.squares_wide * self.square_width, 2 * self.square_width):
            for y_coord in range(self.display_buffer, self.squares_tall * self.square_width + self.display_buffer, 2 * self.square_width):
                self.checkers.append(checker_square((x_coord, y_coord), self.square_width))
                self.checkers.append(checker_square((x_coord + self.square_width, y_coord + self.square_width), self.square_width))

        self.snek = snek(checker_coords[0], checker_coords[1], self.square_width)


    def draw(self, win):
        # black background
        pygame.draw.rect(win, (0, 0, 0), (0, self.display_buffer, self.dimensions[0], self.dimensions[1]))
        # blue strip at the top
        pygame.draw.rect(win, (0, 100, 200), (0, 0, self.dimensions[0], self.display_buffer))

        # add title
        # when display buffer = 50:
        # text = 175px, so round(3.5 * self.display_buffer)
        x = round((self.dimensions[0] - (3.5 * self.display_buffer)) / 2)
        # height pretty much the size of self.display_buffer, size = 50px
        # when font size = 50, x = 30, so y = self.display_buffer * 1 // 5
        y = round(self.display_buffer / 5)
        title_font = pygame.font.SysFont("sansserif", self.display_buffer)
        title = title_font.render("SNEKBOT", 1, (255,255,255))
        win.blit(title, (x, y))
        for checker in self.checkers:
            checker.draw(win)
        
        if not self.is_snek_within_boundaries():
            self.snek.kill()

        for obstacle in self.obstacles:
            obstacle.draw(win)
        
        if self.is_snek_aligned():
            # print('hi')
            self.snek.switch_direction()
            self.snek.update_segments(self.get_pixel_of_square, self.get_square_of_pixel)
        self.snek.draw(win)

    def add_apple(self, x_index, y_index):
        return apple(self.get_pixel_of_square(x_index, y_index)[0], self.get_pixel_of_square(x_index, y_index)[1], x_index, y_index, self.square_width)

    def is_aligned_to_grid(self, x, y):
        return x % self.square_width == 0 and (y - self.display_buffer) % self.square_width == 0
    def is_snek_aligned(self):
        return self.is_aligned_to_grid(self.snek.get_head_pixel()[0], self.snek.get_head_pixel()[1])

    def is_within_boundaries(self, x, y):
        return (0 <= x and x <= self.dimensions[0] - self.square_width) and (self.display_buffer <= y and y <= self.dimensions[1] - self.square_width)
    def is_snek_within_boundaries(self):
        return self.is_within_boundaries(self.snek.get_head_pixel()[0], self.snek.get_head_pixel()[1])

    def get_pixel_of_square(self, x_index, y_index):
        return (x_index * self.square_width, y_index * self.square_width + self.display_buffer)

    def get_square_of_pixel(self, x, y):
        return (x // self.square_width, (y - self.display_buffer) // self.square_width)


class snek(object):
    def __init__(self, x, y, segment_width, initial_direction = "right"):
        self.segments = [segment(x, y, 0, 0, segment_width, initial_direction)]
        self.segment_width = segment_width
        self.next_direction = initial_direction
        self.alive = True
        self.vel = 5

    def switch_direction(self):
        self.segments[0].set_direction(self.next_direction)

    def get_head_pixel(self):
        return self.segments[0].x_pixel, self.segments[0].y_pixel

    def set_direction(self, direction):
        self.next_direction = direction

    def move_segments(self):
        # move the first one
        self.segments[0].move(self.vel)
        # and the last one
        if len(self.segments) > 1:
            self.segments[-1].move(self.vel)

    def update_segments(self, get_pixel_of_square, get_square_of_pixel):
        new_x_index, new_y_index = get_square_of_pixel(self.get_head_pixel()[0], self.get_head_pixel()[1])
        for segment in self.segments:
            new_x_index, new_y_index = segment.update(new_x_index, new_y_index, get_pixel_of_square)

    def kill(self):
        self.alive = False

    def draw(self, win):
        if self.alive:
            #TODO: make the board call the and update
            # if is_aligned(self.segments[0].x_pixel, self.segments[0].y_pixel):
            #     self.switch_direction()
            #     self.update_segments(self.segments[0].x_pixel, self.segments[0].y_pixel, get_pixel_of_square, get_square_of_pixel)


            # if not is_within_boundaries(self.segments[0].x_pixel, self.segments[0].y_pixel):
            #     self.alive = False
            # else:
                # we do not want to draw the last one
            for segment in self.segments:
                self.move_segments()
                segment.draw(win)

class segment(object):
    def __init__(self, x_pixel, y_pixel, x_index, y_index, size, direction):
        self.x_pixel = x_pixel
        self.y_pixel = y_pixel
        self.x_index = x_index
        self.y_index = y_index
        self.size = size
        self.direction = "right"

    def set_direction(self, direction):
        self.direction = direction

    def move(self, vel):
        if self.direction == "right":
            self.x_pixel += vel
        elif self.direction == "left":
            self.x_pixel -= vel
        elif self.direction == "up":
            self.y_pixel -= vel
        elif self.direction == "down":
            self.y_pixel += vel

    def update(self, new_x_index, new_y_index, get_pixel_of_square):
        self.x_pixel, self.y_pixel = get_pixel_of_square(new_x_index, new_y_index)
        old_x_index, old_y_index = self.x_index, self.y_index
        self.x_index, self.y_index = new_x_index, new_y_index
        return old_x_index, old_y_index

    def draw(self, win):
        pygame.draw.rect(win, (71, 224, 71), (self.x_pixel, self.y_pixel, self.size, self.size))

class apple(object):
    def __init__(self, x_pixel, y_pixel, x_index, y_index, size):
        self.x_pixel = x_pixel
        self.y_pixel = y_pixel
        self.x_index = x_index
        self.y_index = y_index
        self.size = size
    
    def draw(self, win):
        pygame.draw.ellipse(win, (223, 20, 76), pygame.Rect(self.x_pixel, self.y_pixel, self.size, self.size))