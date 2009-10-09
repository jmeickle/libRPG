import pygame

from librpg.menu.theme import MenuTheme
from librpg.config import menu_config

class Cursor(object):

    def __init__(self):
        self.menu = None
        self.widget = None

    def bind(self, menu, widget):
        if not menu.add_cursor(self):
            return False
        else:
            self.menu = menu
            self.widget = widget
            return True

    def step(self, direction):
        target = self.widget.step(direction)
        if target is not None:
            self.widget = target
            print 'Arrived at', self.widget, self.widget.get_center()
        else:
            print 'Blocked'

    def update(self):
        #print 'Cursor @ %s' % self.widget
        pass

    def draw(self):
        pass

class ArrowCursor(Cursor):

    def __init__(self, theme=None):
        Cursor.__init__(self)
        if theme is None:
            self.theme = menu_config.cursor_theme
        else:
            self.theme = theme


class HighlightCursor(Cursor):
    pass
