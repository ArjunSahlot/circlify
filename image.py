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
        self.set_image(image, WHITE)

        self.open = [(x, y) for x in range(width) for y in range(height)]
        self.circles: "list[Circle]" = []
        self.circle_spawn_rate = 1  # Lower for higher resolution.
        self.showing_image = False
        self.growing = True

    def set_image(self, image, color):
        self.circles.clear()
        image = pygame.transform.scale(image, (self.width, self.height))
        self.image = image

    def update(self, window):
        self.draw(window)
        if self.growing:
            self.spawn()
            for circle in self.circles:
                circle.grow()

    def spawn(self):
        for _ in range(self.circle_spawn_rate):
            x, y = random.randrange(self.width), random.randrange(self.height)
            attempts = 0
            while self.in_circles((x + self.x, y + self.y)):
                x, y = random.randrange(self.width), random.randrange(self.height)
                attempts += 1
                if attempts > 1000:
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
