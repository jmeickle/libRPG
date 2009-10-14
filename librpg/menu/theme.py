import pygame

class MenuTheme(object):

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
        return True

    def get_font_color(self):
        DEFAULT_COLOR = (255, 255, 255)
        return DEFAULT_COLOR

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

    def draw_bar(self, surface, rect, filled=1.0, border=1):
        """
        *Virtual.*
        
        Draw a bar delimited by rect onto surface.

        `filled` should be a number between 0.0 and 1.0, indicating how full
        the bar should be.
        """
        TRANSPARENT = (0, 0, 0, 0)
        WHITE = (255, 255, 255, 255)

        surface.fill(TRANSPARENT)
        
        for i in xrange(border):
            border_rect = pygame.Rect((rect.top + i, rect.left + i),
                                      (rect.width - 2 * i,
                                       rect.height - 2 * i))
            pygame.draw.rect(surface, WHITE, border_rect, 1)

        width = rect.width - 2 * border
        vertical_lines = width * filled
        for i in xrange(vertical_lines):
            green = (255.0 * (vertical_lines - i)) / width
            color = (255, green, 0, 255)
            pygame.draw.line(surface,
                             color,
                             (rect.left + i + border, rect.top + border),
                             (rect.left + i + border, rect.bottom - 1 - border),
                             1)

    def draw_image(self, image):
        """
        *Virtual.*
        
        Draw an image. This can be overloaded to apply some filters to
        images used in ImageWidgets.
        """
        return image


class CursorTheme(object):

    BORDER = 2
    HORIZONTAL_OFFSET = 3
    VERTICAL_OFFSET = 3

    def draw_cursor(self, target_rect):
        width = target_rect.w + 2 * (self.BORDER + self.HORIZONTAL_OFFSET)
        height = target_rect.h + 2 * (self.BORDER + self.VERTICAL_OFFSET)
        s = pygame.Surface((width, height)).convert_alpha()
        s.fill((255, 0, 0, 255))
        pygame.draw.rect(s, (0, 0, 0, 0),
                         pygame.Rect((self.BORDER, self.BORDER),
                         (target_rect.w + 2 * self.HORIZONTAL_OFFSET,
                          target_rect.h + 2 * self.VERTICAL_OFFSET)))
        return s, (target_rect.left - self.BORDER - self.HORIZONTAL_OFFSET,
                   target_rect.top - self.BORDER - self.VERTICAL_OFFSET)
