from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from kralengine.main import KralEngine, Vec2
from kralengine.actor import Actor
from kralengine.text import Text
from kralengine.input import Input
from kralengine.line import Line
from kralengine.animation import AnimationManager
from kralengine.types import IMAGE, OBJECT
from kralengine.size import IMAGE_SIZE, SIZE
from kralengine.shapes import RECT, ELLIPSE, CIRCLE
from kralengine.utils import ResourceLocation