import pygame

class Widget(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height)).convert_alpha()

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
