import os

import pygame
import kralengine as ke
from typing import Union, Iterable


class AnimationManager:
    def __init__(self, window: ke.KralEngine, frames, name, time):
        self.window = window
        self.frames = frames
        temp = []
        if type(self.frames) == str:
            self.frames = list(os.walk(self.frames))
            for i in self.frames[0][2]:
                temp.append(os.path.join(self.frames[0][0], i))
            self.frames = temp[::-1]
        self.name = name
        self.time = time

    def getSpriteAnimation(self):
        return AnimationManager.SpriteAnimation(self)

    class SpriteAnimation:
        def __init__(self, manager):
            self.manager = manager

        def __repr__(self):
            return f"SpriteAnimation(window={self.manager.window}, frames={self.manager.frames}, " \
                   f"name={self.manager.name}, time={self.manager.time})"


