import pygame
import random
from circle import Circle


class Image:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.image = None  # Make this a pygame.Surface with text on it saying circlify
        self.circles = []
        self.circle_spawn_rate = 1  # Lower for higher resolution.
        self.active = True

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
        if self.active:
            for circle in self.circles:
                circle.draw(window)
        else:
            window.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))
