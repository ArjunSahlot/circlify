import pygame
import random
from constants import *
from circle import Circle


class Image:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        # Create image with CIRCLIFY on it
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 0, 0))
        text = pygame.font.SysFont("comicsans", 120).render("CIRCLIFY", 1, WHITE)
        self.image.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - text.get_height()//2))

        self.circles = []
        self.circle_spawn_rate = 1  # Lower for higher resolution.
        self.showing_image = False
        self.growing = True

    def update(self, window):
        self.draw(self, window)

    def spawn(self):
        for _ in range(self.circle_spawn_rate):
            x, y = random.randint(self.width, self.height)
            while self.in_circles((x, y)):
                x, y = random.randint(self.width, self.height)
            self.circles.append(Circle(x, y, self.image.get_at((x, y))))

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
