import math
import pygame

from librpg.config import menu_config
from librpg.menu.navigator import WidgetGateway
from librpg.locals import UP, DOWN, LEFT, RIGHT, CENTER


class Widget(object):

    """
    A Widget is a menu component.

    Widgets are typically graphic components that can be added to menus,
    possibly interactive.

    *width* and *height* specify the widget's size in pixels.

    *focusable*, if True (default value), will allow cursors to focus that
    widget, so that it receives events while focused.

    *theme* is a MenuTheme that will be used to render that widget, and
    defaults to the default_theme in librpg.config.menu_config.
    """

    def __init__(self, width=0, height=0, focusable=True, theme=None):
        self.width = width
        self.height = height
        self.image = None

        if theme is not None:
            self.theme = theme
        else:
            self.theme = menu_config.theme

        self.focusable = focusable

        self.parent = None
        self._position = None
        self.menu = None

        self.gateway = WidgetGateway(self)
        self.crystallized = False

    def get_surface(self):
        """
        *Virtual.*

        Return a pygame Surface with the widget's image as it should be
        rendered.
        """
        if self.image is not None:
            return self.image.get_surface()
        else:
            return None

    def draw(self):
        """
        *Virtual.*

        Render the widget on its `image` attribute.
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

    def update_input(self):
        pass

    def left_click(self, x, y):
        """
        *Virtual.*

        Handle a left mouse click event.

        Return whether the event was captured.
        """
        return False

    def right_click(self, x, y):
        """
        *Virtual.*

        Handle a right mouse click event.

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

    def step(self, direction):
        """
        *Virtual.*

        Handle a step event triggered while the widget was focused.

        Return whether the event was captured.
        """
        return False
        
    def crystallize(self, widget_navigator=None):
        self.gateway.crystallize(widget_navigator)

    def widget_step(self, direction, widget_navigator=None):
        return self.gateway.step(direction, widget_navigator)

    def __get_position(self):
        return self._position

    __BAD_SET_POSITION_ARG_ERROR = ('Widget.position has to take an (x, y[, '
                                    'x_align, y_align]) tuple as parameter, '
                                    'where x_align is in (LEFT, CENTER, RIGHT) '
                                    'and y_align is in (UP, CENTER, DOWN).')

    def __set_position(self, pos):
        if pos is None or len(pos) == 2:
            self._position = pos
        else:
            x, y = pos[:2]
            anchor_x, anchor_y = pos[2:4]
            
            if anchor_x == LEFT:
                pass
            elif anchor_x == CENTER:
                x -= self.width / 2
            elif anchor_x == RIGHT:
                x -= self.width
            else:
                raise ValueError(Widget.__BAD_SET_POSITION_ARG_ERROR)
            
            if anchor_y == LEFT:
                pass
            elif anchor_y == CENTER:
                y -= self.height / 2
            elif anchor_y == RIGHT:
                y -= self.height
            else:
                raise ValueError(Widget.__BAD_SET_POSITION_ARG_ERROR)

            self._position = x, y

    position = property(__get_position, __set_position)
    """
    The (x, y) widget position inside its Div.
    
    If the widget is not in any Div, the value is None.
    """
    
    def __get_left(self):
        return self._position[0]

    left = property(__get_left)
    """
    The left boundary of the widget relatively to its Div. 
    """
    
    def __get_top(self):
        return self._position[1]

    top = property(__get_top)
    """
    The top boundary of the widget relatively to its Div. 
    """
    
    def __get_right(self):
        return self._position[0] + self.width

    right = property(__get_right)
    """
    The right boundary of the widget relatively to its Div. 
    """
    
    def __get_bottom(self):
        return self._position[1] + self.height

    bottom = property(__get_bottom)
    """
    The bottom boundary of the widget relatively to its Div. 
    """

    def get_menu_position(self):
        """
        Return the (x, y) widget position inside its menu.
        
        If the widget is not in any menu, the return is None.
        """
        if self.menu is None:
            return None
        else:
            if self.parent is None:
                return (self.x, self.y)
            else:
                parent_pos = self.parent.get_menu_position()
                x = parent_pos[0] + self.left
                y = parent_pos[1] + self.top
                return (x, y)

    def get_center(self):
        """
        Return the (x, y) widget center position inside its menu.
        
        If the widget is not in any menu, the return is None.
        """
        if self.menu is None:
            return None
        else:
            x, y = self.get_menu_position()
            return (x + self.width / 2, y + self.height / 2)

    def get_menu_rect(self):
        """
        Return the pygame Rect representing the widget's dimensions in its
        menu.
        
        If the widget is not in any menu, the return is None.
        """
        if self.menu is None:
            return None
        else:
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
