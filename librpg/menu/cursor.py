import pygame

from librpg.menu.theme import MenuTheme

class Cursor(object):

    def __init__(self, theme=None):
        if theme is None:
            self.theme = MenuTheme()
        else:
            self.theme = theme

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
            print 'Arrived at', self.widget, self.widget.get_menu_position()
        else:
            print 'Blocked'

    def update(self):
        #print 'Cursor @ %s' % self.widget
        pass


class ArrowCursor(Cursor):
    pass


class HighlightCursor(Cursor):
    pass
