import pygame

from librpg.menu.theme import MenuTheme
from librpg.config import menu_config

class Cursor(object):

    def __init__(self, navigator=None):
        self.menu = None
        self.widget = None
        self.navigator = navigator

    def bind(self, menu, widget):
        if not menu.add_cursor(self):
            return False
        else:
            self.menu = menu
            self.widget = widget
            return True

    def step(self, direction):
        if self.navigator is not None:
            target = self.widget.step(direction, self.navigator)
        else:
            target = self.widget.step(direction)
        if target is not None:
            self.widget = target

    def update(self):
        pass

    def draw(self):
        pass

    def move_to(self, widget):
        self.widget = widget


class ArrowCursor(Cursor):

    def __init__(self, theme=None):
        Cursor.__init__(self)
        if theme is None:
            self.theme = menu_config.cursor_theme
        else:
            self.theme = theme
        self.drawn_widget = None

    def draw(self):
        if self.drawn_widget != self.widget:
            widget = self.widget
            rect = widget.get_menu_rect()
            self.surface, self.target_pos = self.theme.draw_cursor(rect)
            self.drawn_widget = widget

    def render(self, screen):
        screen.blit(self.surface, self.target_pos)


class HighlightCursor(Cursor):
    pass
