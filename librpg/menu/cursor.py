from librpg.config import menu_config


class Cursor(object):

    """
    A Cursor is a player-controlled component to interact with the menu.

    *theme* is the CursorTheme to render that Cursor. If None is passed
    (or the default is kept), the cursor will use
    librpg.config.menu_config.cursor_theme.

    *navigator* is the WidgetNavigator with the navigation algorithm
    to be used. If None is passed (or the default is kept), the cursor
    will use LineNavigator.
    """

    def __init__(self, theme=None, navigator=None):
        self.menu = None
        self.widget = None
        self.navigator = navigator
        if theme is None:
            self.theme = menu_config.cursor_theme
        else:
            self.theme = theme
        self.drawn_widget = None

    def bind(self, menu, widget=None):
        """
        Bind the cursor to a *menu*, starting at *widget*.

        Returns whether the operation succeeded.

        If *widget* is not specified, the cursor is bound to the first
        widget found in the menu.
        """
        if widget is None:
            # Bind to the first widget in the menu found
            old_menu = self.menu
            self.menu = menu
            if not self.move_to():
                self.menu = old_menu
                return False
            if not menu.add_cursor(self):
                self.menu = old_menu
                return False
            return True
        else:
            # Bind to *widget*
            if widget not in menu.get_tree():
                return False
            if not menu.add_cursor(self):
                return False
            self.menu = menu
            self.move_to(widget)
            return True

    def step(self, direction):
        if self.navigator is not None:
            target = self.widget.widget_step(direction, self.navigator)
        else:
            target = self.widget.widget_step(direction)
        if target is not None:
            self.widget = target

    def update(self):
        pass

    def draw(self):
        if self.drawn_widget != self.widget:
            widget = self.widget
            rect = widget.get_menu_rect()
            self.image, self.target_pos = self.theme.draw_cursor(rect)
            self.drawn_widget = widget

    def move_to(self, widget=None):
        """
        Move the cursor to another widget.
        """
        if widget is None:
            for candidate in self.menu.get_tree():
                if candidate.focusable:
                    self.widget = candidate
                    return True
            return False
        else:
            if widget not in self.menu.get_tree():
                raise Exception('Cursor is being moved to a widget not in '
                                'its Menu.')
            self.widget = widget
            return True

    def render(self, screen):
        screen.blit(self.image.get_surface(), self.target_pos)


class HighlightCursor(Cursor):
    pass
