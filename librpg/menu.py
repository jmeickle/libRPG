import pygame
from pygame.locals import *

class Menu:

    def __init__(self, position):
    
        self.position = position
        self.widgets = []
    
    def draw():
    
        for widget in self.widgets:
            widget.draw()
    
