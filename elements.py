import pygame


class Button:
    colors = {
        "bg": (0,) * 3,
        "border": (255,) * 3,
        "text": (255,) * 3,
        "highlight": (100, 100, 100),
    }

    def __init__(self, x, y, width, height=50, text="Button", border=0):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.text = text
        self.font = pygame.font.SysFont("comicsans", height*5//9)
        self.padding = height/5
        self.border = border

    def update(self, window, events=None):
        self.draw(window)

    def clicked(self, events):
        if self.hovered():
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return event.button == 1

    def draw(self, window):
        pygame.draw.rect(window, self.colors["highlight" if self.hovered() else "bg"], (self.x, self.y, self.width, self.height))
        if self.border: pygame.draw.rect(window, self.colors["border"], (self.x, self.y, self.width, self.height), self.border, border_radius=1)
        text = self.font.render(self.text, 1, self.colors["text"])
        loc = (self.x + self.width/2 - text.get_width()/2, self.y + self.height/2 - text.get_height()/2)
        window.blit(text, loc)

    def hovered(self):
        mx, my = pygame.mouse.get_pos()
        return self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height
