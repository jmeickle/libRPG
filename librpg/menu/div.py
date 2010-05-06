from librpg.menu.widget import Widget


class BoundWidget(object):

    def __init__(self, widget, old_theme):
        self.widget = widget
        self.old_theme = old_theme


class Div(Widget):

    """
    A widget container and organizer.

    A Div is an invisible rectangular area that stores widgets
    logically. As a Widget, Divs can be nested (Divs may be added to
    other Divs.

    *width*, *height*, *focusable* and *theme* behave like in any other
    Widget.
    """

    def __init__(self, width, height, focusable=False, theme=None):
        Widget.__init__(self, width, height, focusable, theme)
        self.widgets = []

    def add_widget(self, widget, position):
        """
        Add a *widget* to the Div at a given *position*.

        *position* should be an (x, y) tuple in pixels, and relative
        to the Div's top left. Alternatively, an Alignment can be passed
        to calculate the position automatically.
        """
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
        """
        Remove a *widget* from the Div.

        If *widget* is a Widget container, that is, its get_tree()
        returns a list of all widgets it contains, as is the case of Divs,
        all child widgets will be removed as well from this Div.
        """
        if widget.parent is not self:
            return False
        for w in self.widgets:
            if w.widget is widget:
                self.widgets.remove(w)
                w.widget.theme = w.old_theme
                widget.parent = None
                widget.position = None
                widget_and_children = w.widget.get_tree()
                for x in widget_and_children:
                    x.menu = None
                    self.menu.unregister_widget(x)
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
            w.widget.render(screen, x_pos, y_pos)

    def crystallize(self, widget_navigator=None):
        """
        Build static navigation links between widgets.

        This preprocessing will create a "crystalline" structure
        with the widgets, speeding up navigation. Widgets should not be
        added to or removed from the Div after it is crystallized,
        therefore dynamic menu structures should not use it.
        """
        for w in self.widgets:
            w.widget.crystallize(widget_navigator)

    def get_tree(self):
        result = [self]
        for w in self.widgets:
            result.extend(w.widget.get_tree())
        return result

    def get_contents(self):
        return [w.widget for w in self.widgets]

    def clean(self):
        for w in self.get_contents():
            self.remove_widget(w)


class WidgetGroup(Div):

    """
    A WidgetGroup is a Div that is focused a whole.
    """

    def __init__(self, width, height, theme=None):
        Div.__init__(self, width, height, True, theme)

    def add_widget(self, widget, position):
        Div.add_widget(self, widget, position)
        for w in widget.get_tree():
            w.focusable = False
