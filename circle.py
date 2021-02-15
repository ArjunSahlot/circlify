import pygame
pygame.init()


class Circle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.radius = 0
        self.color = color
        self.grow_speed = 1  # 0 if not growing

    def update(self, window):
        self.draw(window)

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
