import math
import pygame
from pygame.locals import SRCALPHA

from librpg.config import menu_config
from librpg.menu.navigator import WidgetGateway


class Widget(object):

    """
    A Widget is a menu component.
    
    Widgets are typically graphic components that can be added to menus,
    tat may be interactive.
    
    *width* and *height* specify the widget's size in pixels.
    
    *focusable*, if True (default value), will allow cursors to focus that
    widget, so that it receives events while focused.
    
    *theme* is a MenuTheme that will be used to render that widget, and
    defaults to the default_theme in librpg.config.menu_config.
    """

    def __init__(self, width=0, height=0, focusable=True, theme=None):
        self.width = width
        self.height = height
        if width > 0 and height > 0:
            self.surface = pygame.Surface((width, height), SRCALPHA, 32)\
                           .convert_alpha()
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
        *Virtual.*

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

        Update the widget's data. Called every cycle the menu is active.
        """
        pass

    def left_click(self, x, y):
        """
        *Virtual.*

        Handle a left mouse click event.
        
        Return whether the event was captured.
        """
        print self, 'got left_click(%d, %d)' % (x, y)
        return False

    def right_click(self, x, y):
        """
        *Virtual.*

        Handle a right mouse click event.
        
        Return whether the event was captured.
        """
        print self, 'got right_click(%d, %d)' % (x, y)
        return False

    def process_event(self, event):
        """
        *Virtual.*

        Handle an event triggered while the widget was focused.
        
        Return whether the event was captured.
        """
        return False

    def activate(self):
        """
        *Virtual.*

        Handle an activate event triggered while the widget was focused.
        
        Return whether the event was captured.
        """
        # print self, 'activated'
        return False

    def crystallize(self, widget_navigator=None):
        self.gateway.crystallize(widget_navigator)

    def step(self, direction, widget_navigator=None):
        return self.gateway.step(direction, widget_navigator)

    def get_menu_position(self):
        if self.parent is None:
            return (self.x, self.y)
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

    def get_tree(self):
        return [self]

    def contains_point(self, pos):
        x, y = pos
        my_x, my_y = self.get_menu_position()
        return (x >= my_x
                and x < my_x + self.width
                and y >= my_y
                and y < my_y + self.height)

    def distance_to_point(self, pos):
        x, y = pos
        my_left, my_top = self.get_menu_position()
        my_right = my_left + self.width
        my_bottom = my_top + self.height

        if x < my_left:
            dx = x - my_left
        elif x < my_right:
            dx = 0
        else:
            dx = x - my_right

        if y < my_top:
            dy = y - my_top
        elif y < my_bottom:
            dy = 0
        else:
            dy = y - my_bottom

        return math.sqrt(dx ** 2 + dy ** 2)
