import pygame
from constants import *
from image import Image
pygame.init()


class Interface:
    def __init__(self):
        self.start_x = self.start_y = 0
        self.im_size = HEIGHT
        self.x, self.y = HEIGHT, 0
