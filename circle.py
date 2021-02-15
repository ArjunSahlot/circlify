import pygame
pygame.init()


class Circle:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.grow_speed = 1  # 0 if not growing

    def update(self, window):
        self.draw(window)

    def draw(self, window):
        pass
