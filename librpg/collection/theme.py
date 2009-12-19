import math

import pygame
from pygame.locals import *

from librpg.menu import MenuTheme, CursorTheme
from librpg.image import Image
from librpg.color import *

class ClassicMenuTheme(MenuTheme):

    """
    A simple opaque, color-configurable old school theme.
    """

    def __init__(self, color=DARK_BLUE, border=2,
                 border_color=WHITE,
                 unselected_tab_color=DARKER_BLUE,
                 round_corners=10):
        self.color = color
        self.border = border
        self.border_color = border_color
        self.unselected_tab_color = unselected_tab_color
        self.round_corners = round_corners

    def get_font_name(self):
        return ('sys', 'Verdana')

    def get_font_color(self):
        return WHITE

    def draw_menu_bg(self, rect):
        return self.draw_round_border_rect(rect)

    def draw_panel(self, rect):
        return self.draw_round_border_rect(rect)

    def draw_scroll_area(self, rect):
        return self.draw_round_border_rect(rect)

    def draw_selected_tab(self, rect):
        surface = pygame.Surface((rect.width, rect.height), SRCALPHA, 32)
        pygame.draw.rect(surface, self.border_color, rect)

        inner_rect = pygame.Rect((rect.left + self.border,
                                  rect.top + self.border),
                                 (rect.width - 2 * self.border,
                                  rect.height - self.border))
        pygame.draw.rect(surface, self.color, inner_rect)
        return Image(surface)

    def draw_unselected_tab(self, rect):
        surface = pygame.Surface((rect.width, rect.height), SRCALPHA, 32)
        pygame.draw.rect(surface, self.border_color, rect)

        inner_rect = pygame.Rect((rect.left + self.border,
                                  rect.top + self.border),
                                 (rect.width - 2 * self.border,
                                  rect.height - self.border))
        pygame.draw.rect(surface, self.unselected_tab_color, inner_rect)
        return Image(surface)

    def draw_bar(self, rect, filled=1.0):
        surface = pygame.Surface((rect.width, rect.height), SRCALPHA, 32)
        surface.fill(TRANSPARENT)

        border = 0 if (rect.width < 4 or rect.height < 4) else 1
        for i in xrange(border):
            border_rect = pygame.Rect((rect.left + i, rect.top + i),
                                      (rect.width - 2 * i,
                                       rect.height - 2 * i))
            pygame.draw.rect(surface, WHITE, border_rect, 1)

        width = rect.width - 2 * border
        vertical_lines = int(width * filled)
        for i in xrange(vertical_lines):
            green = (255.0 * (vertical_lines - i)) / width
            color = (255, green, 0, 255)
            pygame.draw.line(surface,
                             color,
                             (rect.left + i + border,
                              rect.top + border),
                             (rect.left + i + border,
                              rect.bottom - 1 - border),
                             1)
        return Image(surface)

    def draw_rounded_rect(self, surface, rect, color,
                          border_flags):
        BORDER = self.round_corners
        Y_0 = rect.top
        Y_1 = rect.top + BORDER
        Y_2 = rect.top + rect.height - BORDER
        X_0 = rect.left
        X_1 = rect.left + BORDER
        X_2 = rect.left + rect.width - BORDER
        W_MIDDLE = rect.width - 2 * BORDER
        H_MIDDLE = rect.height - 2 * BORDER
        
        # Circle to be cut
        circle = pygame.Surface((2 * BORDER + 1,
                                 2 * BORDER), SRCALPHA, 32)
        circle.fill(TRANSPARENT)
        pygame.draw.circle(circle,
                           color,
                           (BORDER + 1, BORDER + 1),
                           BORDER)

        # Middle
        r = pygame.Rect((X_1, Y_1), (W_MIDDLE, H_MIDDLE))
        pygame.draw.rect(surface, color, r)
        
        # Top
        r = pygame.Rect((X_1, Y_0), (W_MIDDLE, BORDER))
        pygame.draw.rect(surface, color, r)
        
        # Bottom
        r = pygame.Rect((X_1, Y_2), (W_MIDDLE, BORDER))
        pygame.draw.rect(surface, color, r)

        # Left
        r = pygame.Rect((X_0, Y_1), (BORDER, H_MIDDLE))
        pygame.draw.rect(surface, color, r)

        # Bottom
        r = pygame.Rect((X_2, Y_1), (BORDER, H_MIDDLE))
        pygame.draw.rect(surface, color, r)

        BORDER1 = BORDER + 1
        
        # Top left
        surface.blit(circle, (X_0 - 1, Y_0 - 1),
                     pygame.Rect(0, 0, BORDER1, BORDER1))
        
        # Top right
        surface.blit(circle, (X_2, Y_0 - 1),
                     pygame.Rect(BORDER1, 0, BORDER1, BORDER1))
        
        # Bottom left
        surface.blit(circle, (X_0-1, Y_2),
                     pygame.Rect(0, BORDER1, BORDER1, BORDER1))
        
        # Bottom right
        surface.blit(circle, (X_2, Y_2),
                     pygame.Rect(BORDER1, BORDER1, BORDER1, BORDER1))

    def draw_round_border_rect(self, rect,
                               border_flags=(None, True, True, True, True)):
        surface = pygame.Surface((rect.width, rect.height), SRCALPHA, 32)
        surface.fill(TRANSPARENT)
        
        self.draw_rounded_rect(surface, rect, self.border_color, border_flags)
        
        inner_rect = pygame.Rect((rect.left + self.border,
                                  rect.top + self.border),
                                 (rect.width - 2 * self.border,
                                  rect.height - 2 * self.border))
        self.draw_rounded_rect(surface, inner_rect, self.color, border_flags)
        
        return Image(surface)
