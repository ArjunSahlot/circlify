import pygame
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
        "highlight": (180,)*3,
        "padding": 5,
    }

    def __init__(self, x, y, width, height, surf, border):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.surf = pygame.transform.scale(surf, (self.width - self.constants["padding"]*2, self.height - self.constants["padding"]*2))
        self.border = border

    def update(self, window, events):
        pass
