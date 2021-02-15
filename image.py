import pygame


class Image:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.image = None  # Make this a pygame.Surface with text on it saying circlify
        self.circles = []
        self.circle_spawn_rate = 1  # Lower for higher resolution.
        self.active = True

    def update(self, window):
        self.draw(self, window)

    def finish(self):
        for circle in self.circles:
            circle.stop()

    def draw(self, window):
        if self.active:
            for circle in self.circles:
                circle.draw(window)
        else:
            window.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))
