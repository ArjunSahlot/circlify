import pygame
pygame.init()


class Circle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.radius = 0
        self.color = color
        self.grow_speed = 1  # 0 if not growing

    def contains(self, point):
        x, y = point
        return (y - self.y)**2 + (x - self.x)**2 < self.radius**2

    def update(self, window):
        self.draw(window)
        self.radius += self.grow_speed

    def grow(self):
        self.grow_speed = 1

    def stop(self):
        self.grow_speed = 0

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
