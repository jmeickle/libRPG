import pygame

from librpg.menu.widget import Widget

class ImageWidget(Widget):

    def __init__(self, image, focusable=True, theme=None):
        Widget.__init__(self, focusable=focusable, theme=theme)
        self.image = image

    def draw(self):
        if self.surface is None or self.changed:
            self.surface = self.theme.draw_image(self._image)
            self.width = self.surface.get_width()
            self.height = self.surface.get_height()
            self.changed = False

    def __repr__(self):
        return "Image(%dx%d)" % (self.width, self.height)

    def get_image(self):
        return self._image

    def set_image(self, image):
        self._image = image
        self.changed = True
        self.draw()

    image = property(get_image, set_image)
