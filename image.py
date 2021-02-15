import pygame
import random
from constants import *
from circle import Circle


class Image:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.image = None

        # Create image with CIRCLIFY on it
        image = pygame.Surface((width, height))
        image.fill((0, 0, 0))
        text = pygame.font.SysFont("comicsans", 120).render("CIRCLIFY", 1, WHITE)
        image.blit(text, (width//2 - text.get_width()//2, height//2 - text.get_height()//2))

        self.open = []
        self.circles: "list[Circle]" = []
        self.circle_spawn_rate = 1  # Lower for higher resolution.
        self.showing_image = False
        self.growing = True

        self.set_image(image, WHITE)

    def set_image(self, image, color):
        self.circles.clear()
        image = pygame.transform.scale(image, (self.width, self.height))
        image.set_alpha(0)
        self.image = image
        self.open.clear()
        w, h = image.get_size()
        dr, dg, db = color  # desired r, g, b
        buffer = 5  # the buffer for a pixel to be desired
        for x in range(w):
            for y in range(h):
                r, g, b, _ = image.get_at((x, y))
                for val in (dr - r, dg - g, db - b):
                    if val <= buffer:
                        self.open.append((x, y))

    def update(self, window):
        self.draw(window)
        if self.growing and not self.showing_image:
            self.spawn()
            for circle in self.circles:
                circle.grow()

    def spawn(self):
        for _ in range(self.circle_spawn_rate):
            if self.open:
                x, y = self.open.pop(random.randrange(len(self.open)))
            else:
                self.growing = False
                return
            while self.in_circles((x + self.x, y + self.y)):
                if self.open:
                    x, y = self.open.pop(random.randrange(len(self.open)))
                else:
                    self.growing = False
                    return

            self.circles.append(Circle(x + self.x, y + self.y, self.image.get_at((x, y))))

    def in_circles(self, point):
        for circle in self.circles:
            if circle.contains(point): return True

        return False

    def finish(self):
        for circle in self.circles:
            circle.stop()

    def draw(self, window):
        if self.showing_image:
            window.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))
        else:
            for circle in self.circles:
                circle.draw(window)
