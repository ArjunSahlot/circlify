#
#  Circlify
#  An implementation of a circle packing algorithm used on a image. It can also pack a specific color only.
#  Copyright Arjun Sahlot 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import time
import pygame
from tkinter import Tk
from image import Image
from constants import *
from webbrowser import open
from datetime import datetime
from tkinter.filedialog import askopenfilename, asksaveasfilename
from elements import Button, ImgButton, Slider, ColorPicker, Check
Tk().withdraw()
pygame.init()


class Settings:
    settings = ImgButton(WIDTH - 5 - 100, HEIGHT - 5 - 100, 100, 100, pygame.image.load(os.path.join("assets", "settings_icon.png")), 5, 90)
    x, y, width, height = HEIGHT + 5, 5, WIDTH - HEIGHT - 10, settings.y - 5
    swap = ImgButton(HEIGHT - 115 - 5, 5, 115, 75, pygame.image.load(os.path.join("assets", "swap_icon.png")), 5, 0)
    pause = Check(x + 10, y + 10, "Play/Pause with spacebar")
    toggle = Check(pause.x, pause.y + pause.height + 10, "Show image toggle button")
    stats = Check(toggle.x, toggle.y + toggle.height + 10, "Show statistics")
    active = False

    def update(self, window, events):
        if self.active:
            self.draw(window)
            self.pause.update(window, events, False)
            self.toggle.update(window, events, False)
            self.stats.update(window, events, False)
        self.settings.update(window, events)
        if self.settings.clicked(events):
            self.active = not self.active
        if self.toggle.checked:
            self.swap.update(window, events)

    def draw(self, window):
        pygame.draw.rect(window, WHITE, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height), 5)


class Interface:
    start_x = start_y = 0
    x, y = HEIGHT, 0
    start_time = time.time()
    end_time = time.time()
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
    refresh = ImgButton(settings.settings.x, 5, settings.settings.width, settings.settings.height, pygame.image.load(os.path.join("assets", "refresh_icon.png")), 5, 180)
    font = pygame.font.SysFont("comicsans", 50)
    small_font = pygame.font.SysFont("comicsans", 30)

    def __init__(self, window):
        self.image = Image(self.start_x, self.start_y, HEIGHT, HEIGHT, window)
        self.spawn.value = self.image.circle_spawn_rate
        self.upper.value, self.lower.value = self.image.grow_rate

    def update(self, window, events, fps):
        self.image.update()

        self.imp.update(window)
        if self.imp.clicked(events) and not self.settings.active:
            try:
                self.image.set_image(pygame.image.load(file := askopenfilename()))
                self.imp_text = file.split("/")[-1]
            except Exception as e:
                self.imp_text = str(e) if "()" not in str(e) else "Unable to import image"

        self.exp.update(window)
        if self.exp.clicked(events) and not self.settings.active:
            try:
                pygame.image.save(self.image.render(), asksaveasfilename())
                self.exp_text = f"Latest export: {datetime.now().strftime('%I:%M:%S %p')}"
            except Exception as e:
                self.exp_text = str(e)

        text = self.font.render(self.imp_text, 1, RED if "." not in self.imp_text else BLACK)
        window.blit(text, (self.imp.x + self.imp.width + 10, self.imp.y + self.imp.height/2 - text.get_height()/2))

        text = self.font.render(self.exp_text, 1, RED if "Latest export" not in self.exp_text else BLACK)
        window.blit(text, (self.exp.x + self.exp.width + 10, self.exp.y + self.exp.height/2 - text.get_height()/2))

        self.spawn.update(window, events, self.settings.active)
        self.image.circle_spawn_rate = self.spawn.value

        pygame.draw.rect(window, BLACK, (self.lower.x - 10, self.lower.y - 10, self.spawn.width, 145), 5)
        text = self.small_font.render("Circle Growing Rate", 1, BLACK)
        window.blit(text, (self.lower.x - 10 + self.spawn.width/2 - text.get_width()/2, self.lower.y - 10 - 3 - text.get_height()))

        self.lower.update(window, events, self.settings.active)
        self.upper.value = max(self.upper.value, self.lower.value)
        self.upper.update(window, events, self.settings.active)
        self.lower.value = min(self.lower.value, self.upper.value)
        self.image.grow_rate = (self.lower.value, self.upper.value)

        text = self.small_font.render("Circle Color", 1, BLACK)
        window.blit(text, ((self.circle_color.wheel_pos[0] + self.circle_color.slider_pos[0] + self.circle_color.slider_size[0])/2 - text.get_width()/2, self.circle_color.wheel_pos[1] - text.get_height() - 5))
        self.circle_color.update(window, self.settings.active)

        self.any_color.update(window, events, self.settings.active)

        self.video.update(window, events, self.settings.active)

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
        self.bg_color.update(window, self.settings.active)

        self.link.update(window)
        if self.link.clicked(events):
            open("https://github.com/ArjunSahlot/pixel_painter")

        self.refresh.update(window, events)
        if self.refresh.clicked(events) and not self.settings.active:
            self.image.refresh(self.bg_color.get_rgb(), "ANY" if self.any_color.checked else self.circle_color.get_rgb(), self.video.checked)
            self.start_time = self.end_time = time.time()

        if self.image.growing:
            self.end_time = time.time()

        self.settings.update(window, events)
        if self.settings.stats.checked:
            num_circles = len(self.image.circles)
            elapsed = self.end_time - self.start_time
            small, large = self.image.get_min_max_circles()
            t1 = self.font.render("Statistics", 1, WHITE)
            window.blit(t1, (40, HEIGHT - 200))
            pygame.draw.line(window, WHITE, (5, HEIGHT - 200 + t1.get_height() + 5), (t1.get_width() + 70, HEIGHT - 200 + t1.get_height() + 5), 5)
            stats = [
                f"Total circles: {num_circles}",
                f"Smallest circle size: {small}",
                f"Largest circle size: {large}",
                f"Time elapsed: {round(elapsed, 3)}",
                f"FPS: {round(fps, 3)}"
            ]
            curr = HEIGHT - 200 + t1.get_height() + 20
            for t in stats:
                text = self.small_font.render(t, 1, WHITE)
                window.blit(text, (40 + t1.get_width()/2 - text.get_width()/2, curr))
                curr += text.get_height() + 5

        if self.settings.toggle.checked and self.settings.swap.clicked(events):
            self.image.showing_image = not self.image.showing_image
