import pygame

from librpg.config import menu_config
from navigator import WidgetGateway, EuclidianNavigator

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
        self.menu = None

        self.gateway = WidgetGateway(self)
        self.crystallized = False

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

    def crystallize(self, widget_navigator=EuclidianNavigator()):
        self.gateway.crystallize(widget_navigator)

    def step(self, direction, widget_navigator=EuclidianNavigator()):
        return self.gateway.step(direction, widget_navigator)

    def is_div(self):
        return False

    def get_menu_position(self):
        if self.parent is None:
            return (0, 0)
        else:
            parent_pos = self.parent.get_menu_position()
            x = parent_pos[0] + self.position[0]
            y = parent_pos[1] + self.position[1]
            return (x, y)

    def get_center(self):
        x, y = self.get_menu_position()
        return (x + self.width / 2, y + self.height / 2)

    def get_menu_rect(self):
        return pygame.Rect(self.get_menu_position(), (self.width, self.height))
