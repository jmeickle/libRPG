import pygame

from librpg.config import menu_config

class Widget(object):

    def __init__(self, width=0, height=0, focusable=True, theme=None):
        self.width = width
        self.height = height
        if width > 0 and height > 0:
            self.surface = pygame.Surface((width, height)).convert_alpha()
        else:
            self.surface = None

        if theme is not None:
            self.theme = theme
        else:
            self.theme = menu_config.theme

        self.focusable = focusable

        self.parent = None
        self.position = None

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
        surf = self.get_surface()
        if surf is not None:
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
