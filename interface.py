import pygame
from constants import *
from image import Image


class Interface:
    def __init__(self, bound):
        self.x = self.y = 0
        self.im_width, self.im_height = bound, HEIGHT
        
