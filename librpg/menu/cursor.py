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
            print 'Cursor BOUND to', self.widget
            return True

    def step(self, direction):
        cur = self.widget
        target = cur.step(direction)
        if target is None:
            print 'Cursor COLLIDED'
            return
        self.widget = target
        print 'Cursor STEP %d' % direction
        print 'Arrived at', self.widget, self.widget.position

    def update(self):
        pass#print 'Cursor @ %s' % self.widget


class ArrowCursor(Cursor):
    pass


class HighlightCursor(Cursor):
    pass
