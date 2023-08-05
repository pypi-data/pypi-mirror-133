import pygame
import os
from typing import Iterable

import __main__


class KralEngine:
    def __init__(self, title: str = "KralEngine",
                 color: Iterable[int] = (0, 0, 0), fps: int = 60,
                 size: Iterable[int] = (500, 300), debug=False):
        self.title = title
        self.color = color
        self.fps = fps
        self.size = size
        self.width = self.size[0]
        self.height = self.size[1]
        self.debug = debug

        self.objects = []

        self.running = True

        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(self.size)
        self.window.fill(self.color)
        pygame.display.set_caption(self.title)

    def run(self):
        while self.running:
            pygame.display.flip()
            self.clock.tick(self.fps)

            pygame.display.update()
            self.window.fill(self.color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if hasattr(__main__, "update") and __main__.update:
                __main__.update()
            for i in self.objects:
                i.update()
            if self.debug:
                pygame.display.set_caption(self.title + " " + str(int(self.clock.get_fps())))
        pygame.quit()
        quit()


Vec2 = pygame.Vector2
