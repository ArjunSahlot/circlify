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
from constants import *
from interface import Interface
import vidmaker

v = vidmaker.Video("/home/arjun/Downloads/circlify.mp4", late_export=True)


# Window Management
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circlify")


def main(window):
    pygame.init()
    clock = pygame.time.Clock()
    window.fill(WHITE)
    interface = Interface(window)

    while True:
        clock.tick(FPS)
        window.fill(WHITE)
        events = pygame.event.get()
        interface.update(window, events, clock.get_fps())
        keys = pygame.key.get_pressed()
        ctrl_pressed = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and ctrl_pressed:
                    pygame.quit()
                    return
                elif event.key == pygame.K_SPACE and interface.settings.pause.checked:
                    interface.image.growing = not interface.image.growing
        pygame.display.update()
        v.update(pygame.surfarray.pixels3d(window).swapaxes(0, 1))


main(WINDOW)

v.export(True)
v.compress()
