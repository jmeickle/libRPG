import pygame
from pygame.locals import SRCALPHA

from librpg.path import cursor_theme_path

class MenuTheme(object):

    """
    A MenuTheme is a set of methods to draw common widgets.

    When MenuThemes are provided to widgets, those widgets will use
    the theme's methods to draw themselves.
    """

    def get_font(self, size, bold=False, italic=False):
        """
        Return a pygame font to render labels.
        """
        type, name = self.get_font_name()
        if type.lower() in ('sys', 'system'):
            return pygame.font.SysFont(name, size, bold, italic)
        elif type.lower() in ('usr', 'user'):
            return pygame.font.Font(name, size, bold, italic)

    def get_font_name(self):
        """
        *Virtual.*

        Return which font should be used for rendering labels.

        The return value should be (type, fontname), where type is 'sys'
        or 'user', indicating respectively if the font is a SysFont or a
        Font for pygame.
        """
        return ('sys', 'Verdana')

    def get_font_anti_alias(self):
        """
        *Virtual.*

        Return whether the font should be drawn with anti-aliasing.
        """
        return True

    def get_font_color(self):
        """
        *Virtual.*

        Return the color to be used for fonts.
        """
        WHITE = (255, 255, 255)
        return WHITE

    def draw_panel(self, surface, rect):
        """
        *Virtual.*

        Draw a Panel delimited by rect onto surface.
        """
        DEFAULT_COLOR = (128, 0, 128, 128)
        pygame.draw.rect(surface, DEFAULT_COLOR, rect)

    def draw_selected_tab(self, surface, rect):
        """
        *Virtual.*

        Draw an active tab header delimited by rect onto surface.
        """
        pass

    def draw_unselected_tab(self, surface, rect):
        """
        *Virtual.*

        Draw an inactive tab header delimited by rect onto surface.
        """
        pass

    def draw_bar(self, surface, rect, filled=1.0):
        """
        *Virtual.*

        Draw a bar delimited by rect onto surface.

        `filled` should be a number between 0.0 and 1.0, indicating how full
        the bar should be.
        """
        TRANSPARENT = (0, 0, 0, 0)
        WHITE = (255, 255, 255, 255)

        surface.fill(TRANSPARENT)

        border = min(rect.width, rect.height) / 6
        for i in xrange(border):
            border_rect = pygame.Rect((rect.top + i, rect.left + i),
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

    def draw_image(self, image):
        """
        *Virtual.*

        Draw an image. This can be overloaded to apply some filters to
        images used in ImageWidgets.
        """
        return image


class CursorTheme(object):

    """
    A CursorTheme describes how to draw a cursor.
    """

    BORDER = 2
    HORIZONTAL_OFFSET = 3
    VERTICAL_OFFSET = 3

    def draw_cursor(self, target_rect):
        """
        *Virtual.*

        Provide a pygame Surface with the cursor's image.

        Return a tuple of two elements, the first being a pygame Surface
        with the cursor's image and the second an (x, y) tuple with the
        position at which the top left of that Surface should be drawn.

        *target_rect* is the pygame Rect describing the cursor's target.
        """
        width = target_rect.w + 2 * (self.BORDER + self.HORIZONTAL_OFFSET)
        height = target_rect.h + 2 * (self.BORDER + self.VERTICAL_OFFSET)
        s = pygame.Surface((width, height), SRCALPHA, 32).convert_alpha()
        s.fill((255, 0, 0, 255))
        pygame.draw.rect(s, (0, 0, 0, 0),
                         pygame.Rect((self.BORDER, self.BORDER),
                         (target_rect.w + 2 * self.HORIZONTAL_OFFSET,
                          target_rect.h + 2 * self.VERTICAL_OFFSET)))
        return s, (target_rect.left - self.BORDER - self.HORIZONTAL_OFFSET,
                   target_rect.top - self.BORDER - self.VERTICAL_OFFSET)


class PictureCursorTheme(CursorTheme):

    """
    A CursorTheme that renders an image loaded from a file as cursor.

    *filename* specifies which file contains the cursor's image.

    The cursor will be drawn to the left of its target. *x_offset* and
    *y_offset* can be used to adjust the cursor's position.
    """

    def __init__(self, filename, x_offset=0, y_offset=0):
        self.filename = filename
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.image = pygame.image.load(self.filename)

    def draw_cursor(self, target_rect):
        center_x = target_rect.left + self.x_offset
        center_y = target_rect.top + target_rect.h / 2 + self.y_offset
        return self.image, (center_x - self.image.get_width(),
                            center_y - self.image.get_height() / 2)


class ArrowCursorTheme(PictureCursorTheme):

    """
    Default CursorTheme for ChoiceDialogs. Displays an arrow by the target.
    """

    def __init__(self, x_offset=-1, y_offset=1):
        PictureCursorTheme.__init__(self, cursor_theme_path('arrow.png'),
                                    x_offset, y_offset)
