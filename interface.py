import pygame
from constants import *
from elements import Button
from image import Image
pygame.init()


class Interface:
    start_x = start_y = 0
    x, y = HEIGHT, 0
    image = Image(start_x, start_y, HEIGHT, HEIGHT)
    imp = Button(WIDTH - 5 - 225, 5, 225, 65, "Import", 5)
    exp = Button(imp.x, imp.y+imp.height + 5, imp.width, imp.height, "Export", imp.border)

    def update(self, window, events):
        self.image.update(window)
        self.imp.update(window)
        self.exp.update(window)
