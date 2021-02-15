import pygame
from constants import *
from image import Image


# Window Management
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circlify")


def main(window):
    pygame.init()
    clock = pygame.time.Clock()
    image = Image(0, 0, HEIGHT, HEIGHT)

    while True:
        clock.tick(FPS)
        window.fill(BLACK)
        events = pygame.event.get()
        image.update(window)
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
        pygame.display.update()


main(WINDOW)
