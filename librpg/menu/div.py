import pygame

from widget import Widget

class BoundWidget(object):

    def __init__(self, widget, position, old_theme):
        self.widget = widget
        self.position = position
        self.old_theme = old_theme


class Div(Widget):

    """
    A widget container and organizer.
    """

    def __init__(self, width, height, theme=None):
        Widget.__init__(self, width, height, theme)
        self.widgets = []

    def add_widget(self, widget, position):
        old_theme = widget.theme
        if widget.theme is None:
            widget.theme = self.theme
        self.widgets.append(BoundWidget(widget, position, old_theme))

    def remove_widget(self, widget):
        for w in self.widgets:
            if w.widget is widget:
                self.widgets.remove(w)
                w.widget.theme = w.old_theme
                return False
        return True

    def draw(self):
        for w in self.widgets:
            w.widget.draw()

    def update(self):
        for w in self.widgets:
            w.widget.update()

    def render(self, screen, x_offset, y_offset):
        for w in self.widgets:
            x_pos = w.position[0] + x_offset
            y_pos = w.position[1] + y_offset
            surf = w.widget.render(screen, x_pos, y_pos)
