import os
import pygame
import numpy as np
from colorsys import rgb_to_hsv, hsv_to_rgb
pygame.init()


class Button:

    constants = {
        "bg": (255,) * 3,
        "border": (0,) * 3,
        "text": (0,) * 3,
        "highlight": (180,)*3,
    }

    def __init__(self, x, y, width, height=50, text="Button", border=0):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.text = text
        self.font = pygame.font.SysFont("comicsans", height-5)
        self.padding = height/5
        self.border = border

    def update(self, window):
        self.draw(window)

    def clicked(self, events):
        if self.hovered():
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return event.button == 1

    def draw(self, window):
        pygame.draw.rect(window, self.constants["highlight" if self.hovered() else "bg"], (self.x, self.y, self.width, self.height))
        if self.border: pygame.draw.rect(window, self.constants["border"], (self.x, self.y, self.width, self.height), self.border, border_radius=1)
        text = self.font.render(self.text, 1, self.constants["text"])
        loc = (self.x + self.width/2 - text.get_width()/2, self.y + self.height/2 - text.get_height()/2)
        window.blit(text, loc)

    def hovered(self):
        mx, my = pygame.mouse.get_pos()
        return self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height


class ImgButton:

    constants = {
        "bg": (255,) * 3,
        "border": (0,) * 3,
        "highlight": (0, 0, 0, 75),
        "padding": 5,
    }

    def __init__(self, x, y, width, height, surf, border, end):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.surf = pygame.transform.scale(surf, (self.width - self.constants["padding"]*2, self.height - self.constants["padding"]*2))
        self.border = border
        self.end = end
        self.rot = 0
        self.rotating = False

    def update(self, window, events):
        self.draw(window)
        if self.rotating:
            if self.rot == -self.end:
                self.rot = 0
                self.rotating = False
            else:
                self.rot -= 5 * self.end/90
        if self.clicked(events):
            self.rotating = True

    def draw(self, window):
        pygame.draw.rect(window, self.constants["bg"], (self.x, self.y, self.width, self.height))
        rot = pygame.transform.rotate(self.surf, self.rot)
        rect = rot.get_rect(center=self.surf.get_rect(topleft=(self.x + self.width/2 - self.surf.get_width()/2, self.y + self.height/2 - self.surf.get_height()/2)).center)
        window.blit(rot, rect.topleft)
        if self.hovered():
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            surf.fill(self.constants["highlight"])
            window.blit(surf, (self.x, self.y))
        if self.border:
            pygame.draw.rect(window, self.constants["border"], (self.x, self.y, self.width, self.height), self.border)

    def hovered(self):
        mx, my = pygame.mouse.get_pos()
        return self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height

    def clicked(self, events):
        if self.hovered():
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return event.button == 1


class ColorPicker:
    def __init__(self, wheel_pos, wheel_rad, slider_pos, slider_size, slider_horiz, slider_invert, cursor_rad, display_rect_loc, display_rect_size, start):
        self.wheel_pos, self.wheel_rad = list(wheel_pos), wheel_rad
        self.slider_pos, self.slider_size, self.slider_horiz, self.slider_invert = list(slider_pos), slider_size, slider_horiz, slider_invert
        self.cursor_rad = cursor_rad
        self.display_rect_loc, self.display_rect_size = display_rect_loc, display_rect_size
        self.start = start
        self.set_wheel_cursor()
        self.set_slider_cursor()
        self.slider_surf = pygame.Surface(slider_size)
        self.wheel_surf = pygame.transform.scale(pygame.image.load(os.path.join(os.path.realpath(os.path.dirname(__file__)), "assets", "color_picker.png")), (wheel_rad * 2,) * 2)
        self.cursor_surf = pygame.Surface((self.cursor_rad*2,)*2, pygame.SRCALPHA)
        self.wheel_darken = pygame.Surface((wheel_rad * 2,) * 2, pygame.SRCALPHA)
        self._create_wheel()
        self._create_slider()
        self.update_wheel()

    def set_wheel_cursor(self):
        if self.start is None:
            self.wheel_cursor = np.array((self.wheel_rad,)*2)
        elif self.start == "red":
            self.wheel_cursor = np.array((self.wheel_rad, self.wheel_rad*2-2))

    def set_slider_cursor(self):
        if self.start is None:
            self.slider_cursor = np.array((self.slider_size[0]//2, self.slider_size[1]//2))
        elif self.start == "red":
            self.slider_cursor = np.array((self.slider_size[0]//2, 1))

    def draw(self, window):
        pygame.draw.rect(window, self.get_rgb(), (*self.display_rect_loc, *self.display_rect_size))
        window.blit(self.slider_surf, self.slider_pos)
        self._draw_cursor(window, np.array(self.slider_pos) + np.array(self.slider_cursor))
        window.blit(self.wheel_surf, self.wheel_pos)
        window.blit(self.wheel_darken, self.wheel_pos)
        self._draw_cursor(window, np.array(self.wheel_pos) + np.array(self.wheel_cursor))

    def update(self, window):
        self.draw(window)
        if any(pygame.mouse.get_pressed()):
            x, y = pygame.mouse.get_pos()
            if ((self.wheel_pos[0] + self.wheel_rad - x) ** 2 + (self.wheel_pos[1] + self.wheel_rad - y) ** 2)**0.5 < self.wheel_rad - 2:
                if pygame.mouse.get_pressed()[0]:
                    self.wheel_cursor = (x - self.wheel_pos[0], y - self.wheel_pos[1])
                else:
                    self.set_wheel_cursor()
                return True
            elif self.slider_pos[0] < x < self.slider_pos[0] + self.slider_size[0] and self.slider_pos[1] < y < self.slider_pos[1] + self.slider_size[1]:
                if pygame.mouse.get_pressed()[0]:
                    self.slider_cursor[1] = (y - self.slider_pos[1])*((self.slider_size[1]-1)/self.slider_size[1])
                else:
                    self.set_slider_cursor()
                self.update_wheel()
                return True

    def get_rgb(self):
        wrgb = self.wheel_surf.get_at(self.wheel_cursor)
        srgb = self.slider_surf.get_at(self.slider_cursor)
        whsv = rgb_to_hsv(*(np.array(wrgb)/255)[:3])
        shsv = rgb_to_hsv(*(np.array(srgb)/255)[:3])
        hsv = (whsv[0], whsv[1], shsv[2])
        rgb = np.array(hsv_to_rgb(*hsv))*255
        return rgb

    def get_hsv(self):
        rgb = (np.array(self.get_rgb())/255)[:3]
        return np.array(rgb_to_hsv(*rgb))*255

    def update_wheel(self):
        pygame.draw.circle(self.wheel_darken, (0, 0, 0, np.interp(self.get_hsv()[2], (0, 255), (255, 0))), (self.wheel_rad,)*2, self.wheel_rad)

    def _create_wheel(self):
        return

    def _create_slider(self):
        w, h = self.slider_size
        if self.slider_horiz:
            for x in range(w):
                if self.slider_invert:
                    value = np.interp(x, (0, w), (0, 255))
                else:
                    value = np.interp(x, (0, w), (255, 0))
                pygame.draw.rect(self.slider_surf, (value,)*3, (x, 0, 1, h))

        else:
            for y in range(h):
                if self.slider_invert:
                    value = np.interp(y, (0, h), (0, 255))
                else:
                    value = np.interp(y, (0, h), (255, 0))
                pygame.draw.rect(self.slider_surf, (value,)*3, (0, y, w, 1))
        pygame.draw.rect(self.slider_surf, (255, 255, 255), (0, 0, w, h), 1)

    def _draw_cursor(self, window, pos):
        pygame.draw.circle(window, (255, 255, 255), pos, self.cursor_rad)
        pygame.draw.circle(window, (0, 0, 0), pos, self.cursor_rad, 2)


class Slider:
    colors = {
        "text": (0,) * 3,
        "slider": (50,) * 3,
        "cursor": (130,) * 3,
        "arrows": (255,) * 3,
        "boxes": (80,) * 3,
        "highlighted_boxes": (120,) * 3,
    }
    tri_padx = 8
    tri_pady = 5

    def __init__(self, x, y, width, height=40, init_val=80, val_range=(1, 100), label="Slider", only_int=True):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.font = pygame.font.SysFont("comicsans", height - 15)
        self.label = label
        self.range = val_range
        self.value = init_val
        self.dragging = False
        self.to_int = only_int

    def draw_arrows(self, window):
        left = pygame.Surface((self.height,)*2)
        right = pygame.Surface((self.height,)*2)
        mx, my = pygame.mouse.get_pos()
        colliding = self.x <= mx <= self.x + self.height and self.y <= my <= self.y + self.height
        color = self.colors["highlighted_boxes"] if colliding else self.colors["boxes"]
        left.fill(color)
        colliding = self.x + self.width - self.height <= mx <= self.x + self.width and self.y <= my <= self.y + self.height
        color = self.colors["highlighted_boxes"] if colliding else self.colors["boxes"]
        right.fill(color)
        l = self.tri_padx
        r = self.height - self.tri_padx
        t = self.tri_pady
        m = self.height/2
        b = self.height - self.tri_pady
        pygame.draw.polygon(left, self.colors["arrows"], ((r, t), (l, m), (r, b)))
        pygame.draw.polygon(right, self.colors["arrows"], ((l, t), (r, m), (l, b)))
        window.blit(left, (self.x, self.y))
        window.blit(right, (self.x + self.width - self.height, self.y))

    def update(self, window, events):
        self.draw(window)
        mx, my = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.y <= my <= self.y + self.height:
                    self.dragging = self.x + self.height <= mx <= self.x + self.width - self.height
                    if self.x <= mx <= self.x + self.height:
                        self.value = max(self.value - 1, self.range[0])
                    elif self.x + self.width - self.height <= mx <= self.x + self.width:
                        self.value = min(self.value + 1, self.range[1])
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

        if self.dragging:
            self.loc_to_value()

    def draw(self, window):
        pygame.draw.rect(window, self.colors["slider"], (self.x, self.y, self.width, self.height))
        pygame.draw.rect(window, self.colors["cursor"], (self.value_to_loc() - self.height/2, self.y, self.height, self.height))
        self.draw_arrows(window)
        text = self.font.render(f"{self.label}: {self.value}", 1, self.colors["text"])
        text_loc = (self.x + (self.width-text.get_width()) // 2, self.y + self.height + 5)
        window.blit(text, text_loc)

    def loc_to_value(self):
        val = np.interp(pygame.mouse.get_pos()[0], (self.x + self.height*1.5, self.x + self.width - self.height*1.5), self.range)
        self.value = int(val) if self.to_int else val

    def value_to_loc(self):
        return np.interp(self.value, self.range, (self.x + self.height*1.5, self.x + self.width - self.height*1.5))
