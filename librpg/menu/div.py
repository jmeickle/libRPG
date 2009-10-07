import pygame

from widget import Widget
from navigator import EuclidianNavigator

class BoundWidget(object):

    def __init__(self, widget, old_theme):
        self.widget = widget
        self.old_theme = old_theme


class Div(Widget):

    """
    A widget container and organizer.
    """

    def __init__(self, width, height, focusable=True, theme=None):
        Widget.__init__(self, width, height, focusable, theme)
        self.widgets = []

    def add_widget(self, widget, position):
        assert widget.parent is None, 'Widget is already added to a div'
        old_theme = widget.theme
        if widget.theme is None:
            widget.theme = self.theme
        self.widgets.append(BoundWidget(widget, old_theme))
        widget.parent = self
        widget.position = position

    def remove_widget(self, widget):
        if widget.parent is not self:
               return False
        for w in self.widgets:
            if w.widget is widget:
                self.widgets.remove(w)
                w.widget.theme = w.old_theme
                widget.parent = None
                widget.position = None
                return True
        return False

    def draw(self):
        for w in self.widgets:
            w.widget.draw()

    def update(self):
        for w in self.widgets:
            w.widget.update()

    def render(self, screen, x_offset, y_offset):
        for w in self.widgets:
            x_pos = w.widget.position[0] + x_offset
            y_pos = w.widget.position[1] + y_offset
            surf = w.widget.render(screen, x_pos, y_pos)

    def crystallize(self, widget_navigator=EuclidianNavigator()):
        for w in self.widgets:
            w.widget.crystallize(widget_navigator)
        self.gateway.div_crystallize(widget_navigator)
