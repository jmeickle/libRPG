import librpg
from librpg.config import graphics_config
from librpg.menu import (MenuController, Menu, Cursor, Bar, Grid, Panel,
                         AlignCenter)
from librpg.context import get_context_stack

class CrazyBar(Bar):

    def __init__(self, width, height, filled=1.0, focusable=True,
                 theme=None):
        Bar.__init__(self, width, height, filled, focusable, theme)
        self.ascending = True

    def update(self):
        if self.ascending:
            self.filled += 0.02
        else:
            self.filled -= 0.02

        if self.filled == 1.0:
            self.ascending = False
        elif self.filled == 0.0:
            self.ascending = True


class BarMenu(Menu):

    def __init__(self):
        Menu.__init__(self, 480, 320)
        grid = Grid(480, 320, 4, 10)
        for i in xrange(4):
            for j in xrange(10):
                grid[i, j].add_widget(Panel(118, 30), AlignCenter())
                width = 10 + 10 * (i + 1)
                height = 1 + j
                bar = CrazyBar(width, height)
                grid[i, j].add_widget(bar, AlignCenter())
        self.add_widget(grid, AlignCenter())
        
        self.crystallize()

        # Add cursor
        cursor = Cursor()
        cursor.bind(self, grid[0, 0].widgets[0].widget)


def main():
    librpg.init()
    graphics_config.config(screen_width=480, screen_height=320)

    c = MenuController(BarMenu())
    get_context_stack().stack_context(c)
    get_context_stack().gameloop()

if __name__ == '__main__':
    main()
