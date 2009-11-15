def _x_left(widget, div, border):
    return border


def _x_center(widget, div):
    return (div.width - widget.width) / 2


def _x_right(widget, div, border):
    return (div.width - widget.width - border)


def _y_top(widget, div, border):
    return border


def _y_center(widget, div):
    return (div.height - widget.height) / 2


def _y_bottom(widget, div, border):
    return (div.height - widget.height - border)


class Alignment(object):

    """
    Alignments can be passed to Div.add_widget() calls as the
    *position* parameter to calculate it automatically.
    
    *border* should be the offset in pixels from the location specified.
    """

    def __init__(self, border=0):
        self.border = border

    def align_widget(self, widget, div):
        """
        *Abstract.*

        Return the position that *widget* should have inside *div*.
        """
        raise NotImplementedError('Alignment.calc_pos() is abstract')


class AlignTop(Alignment):

    """
    Aligns the widget at the top of the div.
    """

    def align_widget(self, widget, div):
        return (_x_center(widget, div), _y_top(widget, div, self.border))


class AlignLeft(Alignment):

    """
    Aligns the widget at the left of the div.
    """

    def align_widget(self, widget, div):
        return (_x_left(widget, div, self.border), _y_center(widget, div))


class AlignBottom(Alignment):

    """
    Aligns the widget at the bottom of the div.
    """

    def align_widget(self, widget, div):
        return (_x_center(widget, div), _y_bottom(widget, div, self.border))


class AlignRight(Alignment):

    """
    Aligns the widget at the right of the div.
    """

    def align_widget(self, widget, div):
        return (_x_right(widget, div, self.border), _y_center(widget, div))


class AlignTopLeft(Alignment):

    """
    Aligns the widget at the top left corner of the div.
    """

    def align_widget(self, widget, div):
        return (_x_left(widget, div, self.border),
                _y_top(widget, div, self.border))


class AlignBottomLeft(Alignment):

    """
    Aligns the widget at the bottom left corner of the div.
    """

    def align_widget(self, widget, div):
        return (_x_left(widget, div, self.border),
                _y_bottom(widget, div, self.border))


class AlignTopRight(Alignment):

    """
    Aligns the widget at the top right corner of the div.
    """

    def align_widget(self, widget, div):
        return (_x_right(widget, div, self.border),
                _y_top(widget, div, self.border))


class AlignBottomRight(Alignment):

    """
    Aligns the widget at the bottom right corner of the div.
    """

    def align_widget(self, widget, div):
        return (_x_right(widget, div, self.border),
                _y_bottom(widget, div, self.border))


class AlignCenter(Alignment):

    """
    Aligns the widget at the center of the div.
    """

    def align_widget(self, widget, div):
        return (_x_center(widget, div), _y_center(widget, div))
