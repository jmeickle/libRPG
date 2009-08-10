import pygame
from pygame.locals import *

class Menu(object):

    def __init__(self, position):
        self.position = position
        self.widgets = []

    def draw():
        for widget in self.widgets:
            widget.draw()


