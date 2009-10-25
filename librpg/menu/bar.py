import pygame

from librpg.menu.widget import Widget


class Bar(Widget):

    """
    A Bar is a Widget that displays a recipient that can be from 0% to
    100% filled.
    
    *width* and *height* are the Bar's dimensions, and how it scales will
    depend on the theme.
    
    *filled* is a float from 0.0 to 1.0 representing how full the bar is,
    initially.
    
    *focusable* and *theme* behave like in any other Widget.
    """

    def __init__(self, width, height, filled=1.0, focusable=True,
                 theme=None):
        Widget.__init__(self, width, height, focusable, theme)
        self.filled = filled
        self.changed = True
        self.draw()

    def draw(self):
        if self.changed:
            self.changed = False
            self.theme.draw_bar(self.surface,
                                pygame.Rect((0, 0), (self.width, self.height)),
                                self.filled)

    def __repr__(self):
        return "Bar(%.2f%%)" % self.filled

    def get_filled(self):
        return self._filled

    def set_filled(self, filled):
        self._filled = filled
        if self._filled < 0:
            self._filled = 0
        elif self._filled > 1.0:
            self._filled = 1.0
        self.changed = True

    filled = property(get_filled, set_filled)
    """
    Float from 0.0 to 1.0 representing how full the bar is.
    """

    # def get_border(self):
        # return self._border

    # def set_border(self, border):
        # self._border = border
        # self.changed = True

    # border = property(get_border, set_border)
