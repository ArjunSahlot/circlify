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
    imp_text = "No file imported."
    exp = Button(imp.x, imp.y+imp.height + 5, imp.width, imp.height, "Export", imp.border)
    exp_text = "Latest export: Never"
    settings = ImgButton(WIDTH - 5 - 100, HEIGHT - 5 - 100, 100, 100, pygame.image.load(os.path.join("assets", "settings_icon.png")), 5)
    font = pygame.font.SysFont("comicsans", 50)

    def update(self, window, events):
        self.image.update(window)
        self.imp.update(window)
        if self.imp.clicked(events):
            try:
                self.image.set_image(pygame.image.load(file := askopenfilename()))
                self.imp_text = file.split("/")[-1]
            except Exception as e:
                self.imp_text = str(e) if "()" not in str(e) else "Unable to import image"
        self.exp.update(window)
        if self.exp.clicked(events):
            pygame.image.save(self.image.render(), asksaveasfilename())
        t1 = self.font.render(self.imp_text, 1, RED if "." not in self.imp_text else BLACK)
        window.blit(t1, (self.imp.x + self.imp.width + 10, self.imp.y + self.imp.height/2 - t1.get_height()/2))
        t2 = self.font.render(self.exp_text, 1, RED if self.exp_text == "Export failed" else BLACK)
        window.blit(t2, (self.exp.x + self.exp.width + 10, self.exp.y + self.exp.height/2 - t2.get_height()/2))
        self.settings.update(window, events)
