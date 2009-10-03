import pygame

from widget import Widget

class BoundWidget(object):

    def __init__(self, widget, position):
        self.widget = widget
        self.position = position


class Div(Widget):

    """
    A widget container and organizer.
    """

    def __init__(self, width, height):
        Widget.__init__(self, width, height)
        self.widgets = []

    def add_widget(self, widget, position):
        self.widgets.append(BoundWidget(widget, position))

    def remove_widget(self, widget):
        for w in self.widgets:
            if w.widget is widget:
                self.widgets.remove(w)
                return False
        return True

    def draw(self):
        for w in self.widgets:
            w.widget.draw()

    def update(self):
        for w in self.widgets:
            w.widget.update()
