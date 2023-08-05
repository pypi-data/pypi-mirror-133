import pygame
import kralengine as ke
import logging
import os

import __main__


class Actor:
    def __init__(self, window: ke.KralEngine, atype, shape, pos, size, color=(0, 0, 0)):
        self.logger = logging.getLogger(str(id(self)) + " " + os.path.basename(__main__.__file__))
        # Logger
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler('file.log')
        c_handler.setLevel(logging.WARNING)
        f_handler.setLevel(logging.ERROR)
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)
        self.logger.addHandler(c_handler)
        self.logger.addHandler(f_handler)

        self.drawed = False
        self.animate = False
        self.animations = {}
        self.atype = atype
        self.shape = shape
        self.pos = pos
        self.size = size
        self.window = window
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.color = color
        self.image = None
        if hasattr(self.window, "objects"):
            self.window.objects.append(self)

    def draw(self):
        if type(self.atype()) == ke.IMAGE:
            try:
                self.image = pygame.image.load(self.shape.getFullPath())
                if type(self.size) == ke.SIZE:
                    self.image = pygame.transform.scale(self.image, self.size.get_size())
                self.window.window.blit(self.image, self.pos)
                self.drawed = True
            except:
                self.logger.error("Image can't load!")
                self.drawed = False
        elif type(self.atype()) == ke.OBJECT:
            try:
                if type(self.shape()) == ke.RECT:
                    self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size.get_width(), self.size.get_height())
                    pygame.draw.rect(self.window.window, self.color, self.rect)
                    self.drawed = True
            except:
                self.logger.error("Object can't draw!")
                self.drawed = False

    def update(self):
        if self.drawed:
            self.draw()
