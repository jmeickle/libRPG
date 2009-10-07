import pygame

from librpg.menu.theme import MenuTheme

class Cursor(object):

    def __init__(self, theme=None):
        if theme is None:
            self.theme = MenuTheme()
        else:
            self.theme = theme


class ArrowCursor(Cursor):
    pass


class HighlightCursor(Cursor):
    pass
