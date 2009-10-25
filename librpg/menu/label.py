import pygame

from librpg.menu.widget import Widget


class Label(Widget):

    """
    A Label is a widget that displays text.

    *text* is a string with the text to be displayed in the label.
    *size*, *bold* and *italic* are font properties to render the label.

    *focusable* and *theme* behave like in any other Widget.
    """

    def __init__(self, text='', size=12, bold=False, italic=False,
                 focusable=True, theme=None):
        Widget.__init__(self, focusable=focusable, theme=theme)
        self._text = text
        self._size = size
        self._bold = bold
        self._italic = italic
        self.changed = False
        self.draw()

    def draw(self):
        if self.surface is None or self.changed:
            self.changed = False
            font = self.theme.get_font(self.size, self.bold, self.italic)
            self.surface = font.render(self.text,
                                       self.theme.get_font_anti_alias(),
                                       self.theme.get_font_color())
            self.width = self.surface.get_width()
            self.height = self.surface.get_height()

    def __repr__(self):
        return "Label('%s')" % self._text

    def get_text(self):
        return self._text

    def set_text(self, text):
        self.changed = True
        self._text = text

    text = property(get_text, set_text)
    """
    The string to be displayed in the label.
    """

    def get_size(self):
        return self._size

    def set_size(self, size):
        self.changed = True
        self._size = size

    size = property(get_size, set_size)
    """
    The font size to render the label.
    """

    def get_bold(self):
        return self._bold

    def set_bold(self, bold=True):
        self.changed = True
        self._bold = bold

    bold = property(get_bold, set_bold)
    """
    Whether the letters should be rendered as bold.
    """

    def get_italic(self):
        return self._italic

    def set_italic(self, italic=True):
        self.changed = True
        self._italic = italic

    italic = property(get_italic, set_italic)
    """
    Whether the letters should be rendered as italic.
    """
