import pygame

from librpg.menu.widget import Widget
from librpg.menu.navigator import EuclidianNavigator

class BoundWidget(object):

    def __init__(self, widget, old_theme):
        self.widget = widget
        self.old_theme = old_theme


class Div(Widget):

    """
    A widget container and organizer.
    """

    def __init__(self, width, height, focusable=False, theme=None):
        Widget.__init__(self, width, height, focusable, theme)
        self.widgets = []

    def add_widget(self, widget, position):
        assert widget.parent is None, 'Widget is already added to a div'
        old_theme = widget.theme
        if widget.theme is None:
            widget.theme = self.theme
        self.widgets.append(BoundWidget(widget, old_theme))
        widget.parent = self

        try:
            widget.position = position.align_widget(widget, self)
        except AttributeError:
            # position is not an Alignment
            widget.position = position

        if self.menu is not None:
            for w in widget.get_tree():
                if w.menu is not self.menu:
                    w.menu = self.menu
                    self.menu.register_widget(w)

    def remove_widget(self, widget):
        if widget.parent is not self:
               return False
        for w in self.widgets:
            if w.widget is widget:
                self.widgets.remove(w)
                w.widget.theme = w.old_theme
                widget.parent = None
                widget.position = None
                widget.menu = None
                self.menu.unregister_widget(widget)
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

    def get_tree(self):
        result = [self]
        for w in self.widgets:
            result.extend(w.widget.get_tree())
        return result


class WidgetGroup(Div):
    def __init__(self, width, height, theme=None):
        Div.__init__(self, width, height, True, theme)

    def add_widget(self, widget, position):
        Div.add_widget(self, widget, position)
        for w in widget.get_tree():
            w.focusable = False
