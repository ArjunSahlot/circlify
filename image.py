import pygame


class Image:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.image = None  # Make this a pygame.Surface with text on it saying circlify
        self.circles = []
        self.circle_spawn_rate = 1  # Lower for higher resolution.

    def update(self, window):
        self.draw(self, window)

    def draw(self, window):
        pass
