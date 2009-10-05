import pygame

from librpg.config import menu_config

class Widget(object):

    def __init__(self, width, height, theme=None):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height)).convert_alpha()
        if theme is not None:
            self.theme = theme
        else:
            self.theme = menu_config.theme

    def get_surface(self):
        """
        Return a pygame Surface with the widget's image as it should be
        rendered.
        """
        return self.surface

    def draw(self):
        """
        *Virtual.*
        
        Render the widget on its `surface` attribute.
        """
        pass

    def render(self, screen, x_offset, y_offset):
        screen.blit(self.get_surface(), (x_offset, y_offset))

    def update(self):
        """
        *Virtual.*
        
        Update the widget's data.
        """
        pass

    def left_click(self, x, y):
        """
        *Virtual.*
        
        Handle a left mouse click event.
        """
        pass
    
    def right_click(self, x, y):
        """
        *Virtual.*
        
        Handle a right mouse click event.
        """
        pass
