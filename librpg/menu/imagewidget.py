from librpg.menu.widget import Widget


class ImageWidget(Widget):

    """
    A Widget that displays a static image.

    *surface* should be a pygame Surface with the image to be drawn.

    *focusable* and *theme* behave like in any other Widget.
    """

    def __init__(self, surface, focusable=True, theme=None):
        Widget.__init__(self, focusable=focusable, theme=theme)
        self.image = None
        self.surf = surface

    def draw(self):
        if self.image is None or self.changed:
            self.image = self.theme.draw_image(self._surf)
            self.width = self.image.width
            self.height = self.image.height
            self.changed = False

    def __repr__(self):
        return "Image(%dx%d)" % (self.width, self.height)

    def get_surf(self):
        return self._surf

    def set_surf(self, surf):
        self._surf = surf
        self.changed = True
        self.draw()

    surf = property(get_surf, set_surf)
    """
    A pygame Surface with the widget's image.
    """


class AnimatedImageWidget(Widget):

    """
    A Widget that displays an animated image.

    *animation* should be an AnimatedImage with the animation to be
    displayed.
    
    *focusable* behaves like in any other Widget.
    """

    def __init__(self, animation, focusable=True):
        Widget.__init__(self, focusable=focusable, theme=None)
        self.image = animation
        self.width = animation.width
        self.height = animation.height

    def draw(self):
        pass

    def __repr__(self):
        return "AnimatedImageWidget(%d frames)" % (len(self.image.surfaces))
