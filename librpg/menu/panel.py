import pygame

from librpg.menu.div import Div
from librpg.menu.widget import Widget

class Panel(Div):

    def draw(self):
        r = pygame.Rect(0, 0, self.width, self.height)
        self.theme.draw_panel(self.surface, r)
        Div.draw(self)

    def render(self, screen, x_offset, y_offset):
        Widget.render(self, screen, x_offset, y_offset)
        Div.render(self, screen, x_offset, y_offset)
