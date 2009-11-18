import pygame

from librpg.menu import Div, Widget


class VerticalScrollArea(Div):

    """
    A VerticalScrollArea is a Div that it only partially displayed at each time.
    The "window" through which its contents can be accessed 
    
    The Panel will be rendered with its theme's draw_panel() method.
    """

    def draw(self):
        r = pygame.Rect(0, 0, self.width, self.height)
        if self.image is None:
            self.image = self.theme.draw_scroll_area(r)
        Div.draw(self)

    def render(self, screen, x_offset, y_offset):
        Widget.render(self, screen, x_offset, y_offset)
        Div.render(self, screen, x_offset, y_offset)

