import pygame

from librpg.menu import Div, Widget
from librpg.locals import UP, DOWN


class VerticalScrollArea(Div):

    """
    A VerticalScrollArea is a Div that it only partially displayed at each time.
    The "window" through which its contents can be accessed 
    
    The Panel will be rendered with its theme's draw_panel() method.
    """

    def __init__(self, width, height, cell_height, theme=None):
        Div.__init__(self, width, height, False, theme=theme)
        self.cell_height = cell_height
        self.contents = []
        self.start = 0
        self.height_in_cells = height / cell_height
        self.refresh()

    def __getitem__(self, pos):
        return self.contents[pos]

    def get_last(self):
        if self.contents:
            return self.contents[-1]
        else:
            return None

    def get_first(self):
        if self.contents:
            return self.contents[0]
        else:
            return None

    def get_last_visible(self):
        if self.contents:
            i = min(self.start + self.height_in_cells - 1, len(self) - 1)
            return self.contents[i]
        else:
            return None

    def get_first_visible(self):
        if self.contents:
            return self.contents[self.start]
        else:
            return None

    def add_line(self):
        div = Div(self.width, self.cell_height, theme=self.theme)
        self.contents.append(div)
        self.refresh()
        return len(self.contents) - 1

    def remove_line(self, pos):
        if self.menu is not None and self.menu.cursor is not None:
            old = self.menu.cursor.widget
        div = self.contents.pop(pos)
        self.remove_widget(div)
        self.refresh()
        if self.menu is not None and self.menu.cursor is not None:
            if old not in div.get_contents():
                self.menu.cursor.move_to(old)
            elif pos < len(self):
                self.menu.cursor.move_to(self[pos].get_contents()[0])
            elif pos > 0:
                self.menu.cursor.move_to()

    def __len__(self):
        return len(self.contents)

    def scroll_up(self):
        if self.start > 0:
            self.start -= 1
            self.refresh()
            return True
        else:
            return False

    def scroll_down(self):
        if self.start + self.height_in_cells < len(self):
            self.start += 1
            self.refresh()
            return True
        else:
            return False

    def refresh(self):
        if self.menu is not None and self.menu.cursor is not None:
            old = self.menu.cursor.widget
        self.clean()
        end = min(self.start + self.height_in_cells, len(self))
        for pos, i in enumerate(xrange(self.start, end)):
            self.add_widget(self.contents[i], (0, self.cell_height * pos))
        if self.menu is not None and self.menu.cursor is not None:
            self.menu.cursor.move_to(old)

    def draw(self):
        r = pygame.Rect(0, 0, self.width, self.height)
        if self.image is None:
            self.image = self.theme.draw_scroll_area(r)
        Div.draw(self)

    def render(self, screen, x_offset, y_offset):
        Widget.render(self, screen, x_offset, y_offset)
        Div.render(self, screen, x_offset, y_offset)

    def step(self, direction):
        if direction == UP:
            cursor = self.menu.cursor
            if (cursor is not None
                and cursor.widget in self.get_first_visible().get_contents()):
                scrolled = self.scroll_up()
                if scrolled:
                    target_div = self.get_first_visible()
                    cursor.move_to(target_div.get_contents()[0])
                    return True
        elif direction == DOWN:
            cursor = self.menu.cursor
            if (cursor is not None
                and cursor.widget in self.get_last_visible().get_contents()):
                scrolled = self.scroll_down()
                if scrolled:
                    target_div = self.get_last_visible()
                    cursor.move_to(target_div.get_contents()[0])
                    return True
        return False
