import pygame

from widget import Widget

class ImageWidget(Widget):

    def __init__(self, image, focusable=True, theme=None):
        Widget.__init__(self, focusable=focusable, theme=theme)
        self.image = image
        self.draw()

    def draw(self):
        pass

    def __repr__(self):
        return "Image(%dx%d)" % (self.width, self.height)

    def get_image(self):
        return self.surface

    def set_image(self, image):
        self.surface = image
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

    image = property(get_image, set_image)
