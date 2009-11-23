import pygame
from pygame.locals import *

from librpg.menu import MenuTheme, CursorTheme
from librpg.image import Image


class ClassicMenuTheme(MenuTheme):

    """
    A simple opaque, color-configurable old school theme.
    """

    def __init__(self, color=(0, 0, 128), border=2,
                 border_color=(255, 255, 255), round_corners=5):
        self.color = color
        self.border = border
        self.border_color = border_color
        self.round_corners = round_corners

    def get_font_name(self):
        return ('sys', 'Verdana')

    def get_font_color(self):
        return (255, 255, 255)

    def draw_panel(self, rect):
        surface = pygame.Surface((rect.width, rect.height), SRCALPHA, 32)
        pygame.draw.rect(surface, self.border_color, rect)

        inner_rect = pygame.Rect((rect.top + self.border,
                                  rect.left + self.border),
                                 (rect.width - 2 * self.border,
                                  rect.height - 2 * self.border))
        pygame.draw.rect(surface, self.color, inner_rect)
        return Image(surface)

    def draw_scroll_area(self, rect):
        return self.draw_panel(rect)

    def draw_selected_tab(self, rect):
        pass

    def draw_unselected_tab(self, rect):
        pass

    def draw_bar(self, rect, filled=1.0):
        pass

    def draw_image(self, image):
        pass
