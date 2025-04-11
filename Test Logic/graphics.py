import pygame
import image
from sphere import SpiralSphere, LineSphere
from polygon import Polygon
from klien import KleinBottle


SCREEN_SIZE = 280, 280
SCREEN_TITLE = "Knock Off Scope"
BACKGROUND_COLOR = 0, 0, 0
DRAW_COLOR = 0, 255, 0
BRUSH_RADIUS = 10
CLEAR_SCREEN = False
FADE_RATE = 0.05
FADE_DEATH = 20
FPS = 800


class Pixel:
    def __init__(self, pos, color=DRAW_COLOR):
        self.pos = pos
        self.color = color
        return

    def fade(self):
        if CLEAR_SCREEN:
            return True
        # self.color = (self.color[0] * FADE_RATE, self.color[1] * FADE_RATE, self.color[2] * FADE_RATE)
        self.color = [0, self.color[1] - FADE_RATE, 0]
        return sum(self.color) < FADE_DEATH

    def get_color(self):
        return tuple([int(self.color[i]) for i in range(3)])


class Scope:
    def __init__(self, shape, projection=lambda pos: (pos[0], pos[1]), rotate=False, generate=False, fade_regularly=False):
        self.setup()
        self.shape = shape
        self.img_function = lambda: None
        self.pixel_buffer = []
        self.projection = projection
        self.rotate = rotate
        self.generate = generate
        self.fade_regularly = fade_regularly
        return

    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(SCREEN_TITLE)
        self.running = True
        
        self.pixels = []
        return

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        keys = pygame.key.get_pressed()
        # Quit
        if keys[pygame.K_ESCAPE]:
            self.running = False
        return

    def draw_screen(self):
        self.screen.fill(BACKGROUND_COLOR)
        # Render drawn pixels
        for p in self.pixels:
            self.screen.set_at(p.pos, p.get_color())
        pygame.display.flip()
        return
    
    def fade_points(self):
        index_offset = len(self.pixels) - 1
        for pix_i, pix in enumerate(self.pixels[::-1]):
            if pix.fade():
                self.pixels.pop(index_offset - pix_i)
        return
    
    def add_point(self):
        buffered = False
        if len(self.pixel_buffer) == 0:
            buffered = True
            self.pixel_buffer += self.img_function()
            if self.rotate:
                self.shape.rotate()
            if self.generate:
                self.shape.generate()
        point = self.pixel_buffer.pop()
        pos = [
            int(SCREEN_SIZE[0] * (0.5 + 0.4 * point[0])),
            int(SCREEN_SIZE[1] * (0.5 + 0.4 * point[1]))
        ]
        # pos = [
        #     int(SCREEN_SIZE[0] * (0.5 + 0.1 * point[0])),
        #     int(SCREEN_SIZE[1] * (0.5 + 0.1 * point[1]))
        # ]
        self.pixels.append(Pixel(pos))
        return buffered or self.fade_regularly

    def run(self):
        clock = pygame.time.Clock()
        fade_next_frame = False
        while self.running:
            # Closing etc
            self.handle_events()
            # Drawing
            if fade_next_frame:
                self.fade_points()
            fade_next_frame = self.add_point()
            self.draw_screen()
            # Maintain FPS
            clock.tick(FPS)
            # if clock.get_fps() < FPS - 1:
                # print(f"{FPS} > {clock.get_fps()}")
        pygame.quit()
        return


class Line_Window:
    """
    Draws lines for quick visualization to make sure the shape is actually being drawn right
    """
    def __init__(self):
        self.setup()
        self.run()
        return

    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(SCREEN_TITLE)
        self.running = True
        self.poly = Polygon([4, 4])
        self.get_lines()
        return

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        keys = pygame.key.get_pressed()
        # Quit
        if keys[pygame.K_ESCAPE]:
            self.running = False
        return

    def draw_screen(self):
        self.screen.fill(BACKGROUND_COLOR)
        # Render drawn pixels
        for line in self.lines:
            p1 = [ int(SCREEN_SIZE[0] * (0.5 + 0.4 * line[0][0])), int(SCREEN_SIZE[0] * (0.5 + 0.4 * line[0][1])) ]
            p2 = [ int(SCREEN_SIZE[1] * (0.5 + 0.4 * line[1][0])), int(SCREEN_SIZE[0] * (0.5 + 0.4 * line[1][1])) ]
            pygame.draw.line(self.screen, DRAW_COLOR, p1, p2)
        pygame.display.flip()
        return
    
    def get_lines(self):
        points = self.poly.points
        lines = self.poly.edges
        self.lines = [ [points[l[0]][:-1], points[l[1]][:-1] ] for l in lines ]
        return

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            # Closing etc
            self.handle_events()
            
            # Draw
            self.draw_screen()
            # Update
            self.poly.x_tilt += 0.001
            # self.poly.y_tilt += 0.0002
            self.poly.z_tilt += 0.0005
            self.get_lines()
            self.poly.generate()
            
            clock.tick(FPS)
        pygame.quit()
        return


if __name__ == "__main__":
    # s = Scope(SpiralSphere())
    # s = Scope(KleinBottle())
    # s.img_function = s.shape.get_point

    # s = Scope(Polygon([4, 4]))
    # s.img_function = s.shape.generate_parameterized_path

    # s = Scope(LineSphere())
    # s.img_function = s.shape.get_frame

    s = Scope(image.ImgPath(r"C:\Users\levin\Documents\Files\Images\Levin Graduation-3.jpg", 5000), fade_regularly=True)
    s.img_function = s.shape.get_path

    s.run()

    # Line_Window()
