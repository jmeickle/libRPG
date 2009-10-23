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

    def align_widget(self, widget, div):
        raise NotImplementedError('Alignment.calc_pos() is abstract')


class AlignTop(Alignment):

    def align_widget(self, widget, div):
        return (_x_center(widget, div), _y_top(widget, div))


class AlignLeft(Alignment):

    def align_widget(self, widget, div):
        return (_x_left(widget, div), _y_center(widget, div))


class AlignBottom(Alignment):

    def align_widget(self, widget, div):
        return (_x_center(widget, div), _y_bottom(widget, div))


class AlignRight(Alignment):

    def align_widget(self, widget, div):
        return (_x_right(widget, div), _y_center(widget, div))


class AlignTopLeft(Alignment):

    def align_widget(self, widget, div):
        return (_x_left(widget, div), _y_top(widget, div))


class AlignBottomLeft(Alignment):

    def align_widget(self, widget, div):
        return (_x_left(widget, div), _y_bottom(widget, div))


class AlignTopRight(Alignment):

    def align_widget(self, widget, div):
        return (_x_right(widget, div), _y_top(widget, div))


class AlignBottomRight(Alignment):

    def align_widget(self, widget, div):
        return (_x_right(widget, div), _y_bottom(widget, div))


class AlignCenter(Alignment):

    def align_widget(self, widget, div):
        return (_x_center(widget, div), _y_center(widget, div))
