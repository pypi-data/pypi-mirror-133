import pygame


class Text:
    def __init__(self, window, text="KralEngine", pos=(0, 0, 0), color=(0, 0, 0), font="Arial",
                 font_size=16, font_type: str = "sysfont"):
        pygame.font.init()

        self.drawed = False

        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.window = window
        self.text = text
        self.color = color
        self.font = font
        self.font_size = font_size
        if font_type.lower() == "sysfont":
            self.font = pygame.font.SysFont(font, self.font_size)
        elif font_type.lower() == "custom":
            self.font = pygame.font.Font(font, self.font_size)
        else:
            if self.window.debug:
                print("DEBUG - TEXT: Font type is invalid or undefined!")
            self.font = pygame.font.SysFont("Arial", self.font_size)

        self.window.objects.append(self)

    def write(self):
        self.drawed = True
        text = self.font.render(self.text, False, self.color)
        self.window.window.blit(text, self.pos)

    def update(self):
        self.pos = [self.x, self.y]
        if self.drawed:
            self.write()
