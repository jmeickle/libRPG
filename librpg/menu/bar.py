import pygame

from librpg.menu.widget import Widget

class Bar(Widget):

    def __init__(self, width, height, filled=1.0, border=1, focusable=True, theme=None):
        Widget.__init__(self, width, height, focusable, theme)
        self.filled = filled
        self.border = border
        self.changed = True
        self.draw()

    def draw(self):
        if self.changed:
            self.changed = False
            self.theme.draw_bar(self.surface,
                                pygame.Rect((0, 0), (self.width, self.height)),
                                self.filled, self.border)

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

    def get_border(self):
        return self._border

    def set_border(self, border):
        self._border = border
        self.changed = True

    border = property(get_border, set_border)
