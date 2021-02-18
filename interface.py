import pygame
from constants import *
from image import Image
pygame.init()


class Interface:
    start_x = start_y = 0
    image = Image(start_x, start_y, HEIGHT, HEIGHT)
    x, y = HEIGHT, 0

    def update(self, window, events):
        self.draw(window)

    def draw(self, window):
        pass
