from librpg.menu.widget import Widget
from librpg.image import Image


class Label(Widget):

    """
    A Label is a widget that displays text.

    *text* is a string with the text to be displayed in the label.
    *size*, *bold* and *italic* are font properties to render the label.

    *max_width* and *max_height* specify the maximum dimensions of the label.
    If any is None, that dimension will be unlimited.

    *focusable* and *theme* behave like in any other Widget.
    """

    def __init__(self, text, max_width=None, max_height=None, size=12,
                 bold=False, italic=False, focusable=True, theme=None):
        Widget.__init__(self, focusable=focusable, theme=theme)
        self._text = text
        self._size = size
        self._bold = bold
        self._italic = italic
        self.changed = False
        self.image = None
        self.max_width = max_width
        self.max_height = max_height
        self.draw()

    def draw(self):
        if self.image is None or self.changed:
            self.changed = False
            if self.max_width is None:
                self.__draw_one_line()
            else:
                self.__draw_multi_line()

    def __draw_one_line(self):
        font = self.theme.get_font(self.size, self.bold, self.italic)
        self.image = Image(font.render(self.text,
                                       self.theme.get_font_anti_alias(),
                                       self.theme.get_font_color()))
        self.width = self.image.width
        self.height = self.image.height
        
    def __draw_multi_line(self):
        pass

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

