import pygame

from librpg.menu.div import Div
from librpg.menu.widget import Widget


class Panel(Div):

    """
    A Panel is a visible Div.

    The Panel will be rendered with its theme's draw_panel() method.
    """

    def draw(self):
        r = pygame.Rect(0, 0, self.width, self.height)
        self.image = self.theme.draw_panel(r)
        Div.draw(self)

    def render(self, screen, x_offset, y_offset):
        Widget.render(self, screen, x_offset, y_offset)
        Div.render(self, screen, x_offset, y_offset)
