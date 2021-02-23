import pygame
from tkinter import Tk
from image import Image
from constants import *
from datetime import datetime
from elements import Button, ImgButton, Slider, ColorPicker
from tkinter.filedialog import askopenfilename, asksaveasfilename
Tk().withdraw()
pygame.init()


class Interface:
    start_x = start_y = 0
    x, y = HEIGHT, 0
    imp = Button(x + 5, 5, 225, 65, "Import", 5)
    imp_text = "No file imported."
    exp = Button(imp.x, imp.y+imp.height + 5, imp.width, imp.height, "Export", imp.border)
    exp_text = "Latest export: Never"
    spawn = Slider(x + 5, exp.y + exp.height + 20, 500, 40, 20, (1, 100), "Circle Spawn Rate")
    lower = Slider(x + 30, spawn.y + spawn.height + 80, spawn.width - (x + 30 - spawn.x)*2, spawn.height, 1, (1, 20), "Lower Bound")
    upper = Slider(lower.x, lower.y + lower.height + 25, lower.width, lower.height, lower.value, lower.range, lower.label.replace("Lower", "Upper"))
    color = ColorPicker((x + 5, upper.y + upper.height + 75), 150, (x + 150*2 + 5 + 8, upper.y + upper.height + 75), (35, 300), False, False, 5, (x + 150*2 + 5 + 8 + 35 + 10, upper.y + upper.height + 75), (50, 300), None)
    settings = ImgButton(WIDTH - 5 - 100, HEIGHT - 5 - 100, 100, 100, pygame.image.load(os.path.join("assets", "settings_icon.png")), 5, 90)
    refresh = ImgButton(settings.x, 5, settings.width, settings.height, pygame.image.load(os.path.join("assets", "refresh_icon.png")), 5, 180)
    font = pygame.font.SysFont("comicsans", 50)
    small_font = pygame.font.SysFont("comicsans", 30)

    def __init__(self, window):
        self.image = Image(self.start_x, self.start_y, HEIGHT, HEIGHT, window)
        self.spawn.value = self.image.circle_spawn_rate
        self.upper.value, self.lower.value = self.image.grow_rate

    def update(self, window, events):
        self.image.update()

        self.imp.update(window)
        if self.imp.clicked(events):
            try:
                self.image.set_image(pygame.image.load(file := askopenfilename()))
                self.imp_text = file.split("/")[-1]
            except Exception as e:
                self.imp_text = str(e) if "()" not in str(e) else "Unable to import image"

        self.exp.update(window)
        if self.exp.clicked(events):
            try:
                pygame.image.save(self.image.render(), asksaveasfilename())
                self.exp_text = f"Latest export: {datetime.now().strftime('%I:%M:%S %p')}"
            except Exception as e:
                self.exp_text = str(e)

        text = self.font.render(self.imp_text, 1, RED if "." not in self.imp_text else BLACK)
        window.blit(text, (self.imp.x + self.imp.width + 10, self.imp.y + self.imp.height/2 - text.get_height()/2))

        text = self.font.render(self.exp_text, 1, RED if "Latest export" not in self.exp_text else BLACK)
        window.blit(text, (self.exp.x + self.exp.width + 10, self.exp.y + self.exp.height/2 - text.get_height()/2))

        self.spawn.update(window, events)
        self.image.circle_spawn_rate = self.spawn.value

        pygame.draw.rect(window, BLACK, (self.lower.x - 10, self.lower.y - 10, self.spawn.width, 145), 5)
        text = self.small_font.render("Circle Growing Rate", 1, BLACK)
        window.blit(text, (self.lower.x - 10 + self.spawn.width/2 - text.get_width()/2, self.lower.y - 10 - 3 - text.get_height()))

        self.lower.update(window, events)
        self.upper.value = max(self.upper.value, self.lower.value)
        self.upper.update(window, events)
        self.lower.value = min(self.lower.value, self.upper.value)
        self.image.grow_rate = (self.lower.value, self.upper.value)

        text = self.small_font.render("Circle Filling Color", 1, BLACK)
        window.blit(text, (self.color.wheel_pos[0] + self.color.wheel_rad - text.get_width()/2, self.color.wheel_pos[1] - text.get_height() - 5))
        self.color.update(window)

        self.settings.update(window, events)

        self.refresh.update(window, events)
        if self.refresh.clicked(events):
            self.image.refresh()
