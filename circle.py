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

from pygame import gfxdraw


class Circle:
    def __init__(self, x, y, color, radius=0):
        self.x, self.y = x, y
        self.radius = radius
        self.color = color
        self.grow_speed = 1  # 0 if not growing

    def contains(self, point):
        x, y = point
        return (y - self.y)**2 + (x - self.x)**2 < self.radius**2

    def collide(self, other):
        dist = (self.x - other.x)**2 + (self.y - other.y)**2
        return dist < (self.radius + other.radius) ** 2

    def update(self, window):
        self.draw(window)
        self.radius += self.grow_speed

    def grow(self):
        self.radius += self.grow_speed

    def stop(self):
        self.grow_speed = 0

    def draw(self, window):
        gfxdraw.aacircle(window, self.x, self.y, self.radius, self.color)
        gfxdraw.filled_circle(window, self.x, self.y, self.radius, self.color)
