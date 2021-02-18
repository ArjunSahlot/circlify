import pygame
from constants import *
from elements import Button
from image import Image
pygame.init()


class Interface:
    start_x = start_y = 0
    x, y = HEIGHT, 0
    image = Image(start_x, start_y, HEIGHT, HEIGHT)
    imp = Button(WIDTH - 5 - 150, 5, 150, text="Import", border=5)
    exp = Button(imp.x, imp.y+imp.height + 5, imp.width, text="Export", border=imp.border)

    def update(self, window, events):
        self.image.update(window)
        self.imp.update(window)
        self.exp.update(window)
