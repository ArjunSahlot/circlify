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

import pygame
import random
import cv2
import atexit
from constants import *
from circle import Circle


class Image:
    def __init__(self, x, y, width, height, window: pygame.Surface):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.image = None
        self.background = BLACK
        self.window = window

        # Create image with CIRCLIFY on it
        image = pygame.Surface((width, height))
        self.font = lambda size: pygame.font.SysFont("comicsans", size)
        image.fill((0, 0, 0))
        text = self.font(250).render(pygame.display.get_caption()[0].upper(), 1, WHITE)
        image.blit(text, (x + width//2 - text.get_width()//2, y + height//2 - text.get_height()//2))

        self.open = []
        self.circles: "list[Circle]" = []
        self.circle_color = "ANY"
        self.circle_spawn_rate = 20  # Higher for higher resolution.
        self.using_cam = False
        self.camera = cv2.VideoCapture(0)
        self.showing_image = False
        self.growing = True
        self.grow_rate = (1, 1)  # (lower, higher) bounds

        self.set_image(image, WHITE)

        atexit.register(getattr(self.camera, "release"))

    def get_min_max_circles(self):
        if self.circles:
            circles = sorted(self.circles, key=lambda x: x.radius)
            return circles[0].radius, circles[-1].radius
        return 0, 0

    def refresh(self, bg, circle_col, video):
        self.background = bg
        self.circle_color = circle_col
        self.using_cam = video
        self.circles.clear()
        self.growing = True

    def set_image(self, image, color="ANY"):
        self.window.fill((0, 0, 0), (self.x, self.y, self.width, self.height))
        text = self.font(175).render("Calculating...", 1, WHITE)
        self.window.blit(text, (self.x + self.width//2 - text.get_width()//2, self.y + self.height//2 - text.get_height()//2))
        pygame.display.update()
        self.circles.clear()
        image = pygame.transform.scale(image, (self.width, self.height))
        # image.set_alpha(0)
        w, h = image.get_size()
        self.image = image
        self.growing = True
        if color == "ANY":
            self.open = [(x, y) for x in range(w) for y in range(h)]
            return
        self.open.clear()
        dr, dg, db = color  # desired r, g, b
        buffer = 5  # the buffer for a pixel to be desired
        for x in range(w):
            for y in range(h):
                r, g, b, _ = image.get_at((x, y))
                for val in (dr - r, dg - g, db - b):
                    if val <= buffer:
                        self.open.append((x, y))

    def update(self):
        self.draw()
        if not self.showing_image:
            if self.using_cam:
                self.image = pygame.transform.scale(pygame.surfarray.make_surface(cv2.cvtColor(self.camera.read()[1], cv2.COLOR_BGR2RGB).swapaxes(1, 0)), (self.width, self.height))
                rad = random.randint(5, 7)
                self.circles.clear()
                for x in range(rad, self.width-rad, rad*2):
                    for y in range(rad, self.height-rad, rad*2):
                        self.circles.append(Circle(x, y, self.image.get_at((x, y)), rad))
            else:
                if self.growing:
                    self.spawn()
                    for circle in self.circles:
                        circle.grow()
                    self.update_collisions()

    def spawn(self):
        for _ in range(self.circle_spawn_rate):
            if self.open:
                x, y = self.open.pop(random.randrange(len(self.open)))
            else:
                self.growing = False
                return
            attempts = 0
            while self.in_circles((x + self.x, y + self.y)):
                if self.open:
                    x, y = self.open.pop(random.randrange(len(self.open)))
                    attempts += 1
                    if attempts > 20:
                        self.growing = False
                        return
                else:
                    self.growing = False
                    return

            if self.circle_color == "ANY":
                color = self.image.get_at((x, y))
            else:
                color = self.circle_color
            c = Circle(x + self.x, y + self.y, color)
            c.grow_speed = random.randint(*self.grow_rate)
            self.circles.append(c)

    def circle_collides(self, circle: Circle):
        if not (0 < circle.x - circle.radius < self.width) or not (0 < circle.y - circle.radius < self.height):
            return True
        for c in self.circles:
            rad_sum = c.radius + circle.radius
            if abs(c.x - circle.x) < rad_sum or abs(c.y - circle.y) < rad_sum:
                if circle.collide(c):
                    return True
        return False

    def in_circles(self, point):
        for circle in self.circles:
            if circle.contains(point): return True

        return False

    def update_collisions(self):
        if len(self.circles) > 1:
            for i in range(len(self.circles)-1):
                for j in range(i+1, len(self.circles)):
                    c1, c2 = self.circles[i], self.circles[j]
                    rad_sum = c1.radius + c2.radius
                    if abs(c1.x - c2.x) < rad_sum or abs(c1.y - c2.y) < rad_sum:
                        if c1.collide(c2):
                            c1.stop()
                            c2.stop()
        for circle in self.circles:
            if circle.grow_speed:
                if circle.x - circle.radius < 0 or circle.x + circle.radius > self.width or \
                    circle.y - circle.radius < 0 or circle.y + circle.radius > self.height:
                    circle.stop()

    def draw(self, surf=None):
        if surf is None:
            surf = self.window
        if self.showing_image:
            surf.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(surf, self.background, (self.x, self.y, self.width, self.height))
            for circle in self.circles:
                circle.draw(surf)

    def render(self):
        surf = pygame.Surface((self.width, self.height))
        surf.fill(self.background)
        prev = self.showing_image
        self.showing_image = False
        self.draw(surf)
        self.showing_image = prev
        return surf
