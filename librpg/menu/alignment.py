def _x_left(widget, div):
    return 0


def _x_center(widget, div):
    return (div.width - widget.width) / 2


def _x_right(widget, div):
    return (div.width - widget.width)


def _y_top(widget, div):
    return 0


def _y_center(widget, div):
    return (div.height - widget.height) / 2


def _y_bottom(widget, div):
    return (div.height - widget.height)


class Alignment(object):

    """
    Alignments can be passed to Div.add_widget() calls as the
    *position* parameter to calculate it automatically.
    """

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
        return (_x_center(widget, div), _y_top(widget, div))


class AlignLeft(Alignment):

    """
    Aligns the widget at the left of the div.
    """

    def align_widget(self, widget, div):
        return (_x_left(widget, div), _y_center(widget, div))


class AlignBottom(Alignment):

    """
    Aligns the widget at the bottom of the div.
    """

    def align_widget(self, widget, div):
        return (_x_center(widget, div), _y_bottom(widget, div))


class AlignRight(Alignment):

    """
    Aligns the widget at the right of the div.
    """

    def align_widget(self, widget, div):
        return (_x_right(widget, div), _y_center(widget, div))


class AlignTopLeft(Alignment):

    """
    Aligns the widget at the top left corner of the div.
    """

    def align_widget(self, widget, div):
        return (_x_left(widget, div), _y_top(widget, div))


class AlignBottomLeft(Alignment):

    """
    Aligns the widget at the bottom left corner of the div.
    """

    def align_widget(self, widget, div):
        return (_x_left(widget, div), _y_bottom(widget, div))


class AlignTopRight(Alignment):

    """
    Aligns the widget at the top right corner of the div.
    """

    def align_widget(self, widget, div):
        return (_x_right(widget, div), _y_top(widget, div))


class AlignBottomRight(Alignment):

    """
    Aligns the widget at the bottom right corner of the div.
    """

    def align_widget(self, widget, div):
        return (_x_right(widget, div), _y_bottom(widget, div))


class AlignCenter(Alignment):

    """
    Aligns the widget at the center of the div.
    """

    def align_widget(self, widget, div):
        return (_x_center(widget, div), _y_center(widget, div))
