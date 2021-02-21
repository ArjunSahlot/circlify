import pygame
from constants import *
from elements import Button, ImgButton
from image import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
Tk().withdraw()
pygame.init()


class Interface:
    start_x = start_y = 0
    x, y = HEIGHT, 0
    image = Image(start_x, start_y, HEIGHT, HEIGHT)
    imp = Button(x + 5, 5, 225, 65, "Import", 5)
    imp_text = "No file imported"
    exp = Button(imp.x, imp.y+imp.height + 5, imp.width, imp.height, "Export", imp.border)
    exp_text = "Latest export: Never"
    settings = ImgButton(WIDTH - 5 - 100, HEIGHT - 5 - 100, 100, 100, pygame.image.load(os.path.join("assets", "settings_icon.png")), 5)

    def update(self, window, events):
        self.image.update(window)
        self.imp.update(window)
        if self.imp.clicked(events):
            self.image.set_image(pygame.image.load(askopenfilename()))
        self.exp.update(window)
        if self.exp.clicked(events):
            pygame.image.save(self.image.render(), asksaveasfilename())
        self.settings.update(window, events)
