import pygame
import random
import cv2
import atexit
from constants import *
from circle import Circle


class Image:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.image = None
        self.background = BLACK

        # Create image with CIRCLIFY on it
        image = pygame.Surface((width, height))
        image.fill((0, 0, 0))
        text = pygame.font.SysFont("comicsans", 250).render("CIRCLIFY", 1, WHITE)
        image.blit(text, (width//2 - text.get_width()//2, height//2 - text.get_height()//2))

        self.open = []
        self.circles: "list[Circle]" = []
        self.circle_spawn_rate = 20  # Higher for higher resolution.
        self.using_cam = True
        self.camera = cv2.VideoCapture(0)
        self.showing_image = False
        self.growing = True

        self.set_image(image, WHITE)

        atexit.register(getattr(self.camera, "release"))

    def set_image(self, image, color="ANY", background=BLACK):
        self.circles.clear()
        image = pygame.transform.scale(image, (self.width, self.height))
        image.set_alpha(0)
        w, h = image.get_size()
        self.image = image
        self.background = background
        if color == "ANY":
            self.open = [(x, y) for x in range(w) for y in range(y)]
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

    def update(self, window):
        self.draw(window)
        if self.using_cam:
            self.image = pygame.transform.scale(pygame.surfarray.make_surface(cv2.cvtColor(self.camera.read()[1], cv2.COLOR_BGR2RGB).swapaxes(1, 0)), (self.width, self.height))
            self.circles.clear()
            open = [[True for _ in range(self.width)] for _ in range(self.height)]
            radii = (30, 25, 20, 15, 10, 5, 2)
            while any([True in row for row in open]):
                possible = [(y, x) for x in range(self.width) for y in range(self.height) if open[y][x]]
                rad = random.choice(radii)
                attempts = 0
                y, x = possible.pop(random.randrange(len(possible)))
                while self.circle_collides(Circle(x, y, (0, 0, 0), rad)):
                    y, x = possible.pop(random.randrange(len(possible)))
                    attempts += 1
                    if attempts > 1:
                        break
                if attempts > 1:
                    if rad == 2:
                        return
                    break
                self.circles.append(Circle(x, y, self.image.get_at((x, y)), rad))
                for rx in range(x-rad, x+rad):
                    for ry in range(y-rad, y+rad):
                        if (rx - x)**2 + (ry - y)**2 < rad**2:
                            try:
                                open[rx][ry] = False
                            except:
                                pass

        else:
            if self.growing and not self.showing_image:
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

            self.circles.append(Circle(x + self.x, y + self.y, self.image.get_at((x, y))))

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

    def draw(self, window):
        if self.showing_image:
            window.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))
        else:
            pygame.draw.rect(window, self.background, (self.x, self.y, self.width, self.height))
            for circle in self.circles:
                circle.draw(window)
