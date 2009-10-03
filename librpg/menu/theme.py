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
        pass


class CursorTheme(object):

    def draw_cursor(self, target_rect):
        pass
