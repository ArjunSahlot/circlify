import pygame
from tkinter import Tk
from image import Image
from constants import *
from webbrowser import open
from datetime import datetime
from elements import Button, ImgButton, Slider, ColorPicker, Check
from tkinter.filedialog import askopenfilename, asksaveasfilename
Tk().withdraw()
pygame.init()


class Settings:
    settings = ImgButton(WIDTH - 5 - 100, HEIGHT - 5 - 100, 100, 100, pygame.image.load(os.path.join("assets", "settings_icon.png")), 5, 90)


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
    circle_color = ColorPicker(
        (x + 5, upper.y + upper.height + 75),
        150,
        (x + 150*2 + 5 + 8, upper.y + upper.height + 75),
        (35, 150*2),
        False,
        False,
        5,
        (x + 5, upper.y + upper.height + 75 + 150*2 + 5),
        (150*2 + 8 + 35, 35),
        None
    )
    bg_color = ColorPicker(
        (circle_color.slider_pos[0] + circle_color.slider_size[0] + 75, upper.y + upper.height + 75),
        150,
        (circle_color.slider_pos[0] + circle_color.slider_size[0] + 75 + 150*2 + 8, upper.y + upper.height + 75),
        (35, 150*2),
        False,
        False,
        5,
        (circle_color.slider_pos[0] + circle_color.slider_size[0] + 75, upper.y + upper.height + 75 + 150*2 + 5),
        (150*2 + 8 + 35, 35),
        "black"
    )
    any_color = Check(circle_color.display_rect_loc[0], circle_color.display_rect_loc[1] + circle_color.display_rect_size[1] + 5, "Use default color")
    any_color.checked = True
    video = Check(any_color.x, any_color.y + any_color.height + 5, "Use Video!")
    link = Button(x + 5, HEIGHT - 60 - 5, 685, 60, "Create an image using Pixel Painter!", 5, BLUE)
    settings = Settings()
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

        text = self.small_font.render("Circle Color", 1, BLACK)
        window.blit(text, ((self.circle_color.wheel_pos[0] + self.circle_color.slider_pos[0] + self.circle_color.slider_size[0])/2 - text.get_width()/2, self.circle_color.wheel_pos[1] - text.get_height() - 5))
        self.circle_color.update(window)

        self.any_color.update(window, events)

        self.video.update(window, events)

        if self.any_color.checked or self.video.checked:
            pad = 10
            width = self.circle_color.display_rect_size[0] + pad + 5
            height = self.circle_color.display_rect_loc[1] + self.circle_color.display_rect_size[1] - self.circle_color.wheel_pos[1] + text.get_height() + pad*2
            if self.video.checked:
                height += self.any_color.height
            surf = pygame.Surface((width, height), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 90))
            window.blit(surf, (self.circle_color.wheel_pos[0] - 5, self.circle_color.wheel_pos[1] - text.get_height() - 5 - pad))

        text = self.small_font.render("Background Color", 1, BLACK)
        window.blit(text, ((self.bg_color.wheel_pos[0] + self.bg_color.slider_pos[0] + self.bg_color.slider_size[0])/2 - text.get_width()/2, self.bg_color.wheel_pos[1] - text.get_height() - 5))
        self.bg_color.update(window)

        self.link.update(window)
        if self.link.clicked(events):
            open("https://github.com/ArjunSahlot/pixel_painter")

        # self.settings.update(window, events)

        self.refresh.update(window, events)
        if self.refresh.clicked(events):
            self.image.refresh(self.bg_color.get_rgb(), "ANY" if self.any_color.checked else self.circle_color.get_rgb(), self.video.checked)
