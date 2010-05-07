import pygame

import librpg
from librpg.menu import (Menu, Panel, Label, Cursor,
                         ImageWidget, WidgetGroup, Bar, VerticalGrid,
                         AlignCenter, AlignTopLeft)
from librpg.context import get_context_stack
from librpg.path import data_path
from librpg.collection.theme import ClassicMenuTheme
from librpg.input import Input
from librpg.locals import (M_1, M_4, M_3,
                           M_5)


class MenuLabel(Label):

    def __init__(self):
        Label.__init__(self, 'Menu')

    def activate(self):
        print 'MenuLabel activated'
        return True


class AdjustableBar(Bar):

    def update_input(self):
        if Input.was_pressed(M_1) or Input.was_pressed(M_4): 
            self.filled += 0.05
        if Input.was_pressed(M_3) or Input.was_pressed(M_5): 
            self.filled -= 0.05


class AdjustableVerticalGrid(VerticalGrid):

    def __init__(self, width, height, height_in_cells, max_height):
        VerticalGrid.__init__(self, width, height, height_in_cells)
        self.max_height = max_height
        for i in range(height_in_cells):
            label = Label('SidePanel%d' % i)
            self[i].add_widget(label, AlignCenter())

    def update_input(self):
        if Input.was_pressed(M_1) or Input.was_pressed(M_4): 
            self.add_line()
        if Input.was_pressed(M_3) or Input.was_pressed(M_5): 
            self.remove_line()

    def add_line(self):
        if self.height_in_cells < self.max_height:
            i = self.height_in_cells
            self.add_lines()
            label = Label('SidePanel%d' % i)
            self[i].add_widget(label, AlignCenter())

    def remove_line(self):
        if self.height_in_cells > 1:
            self.remove_lines()


class TestMenu(Menu):

    def __init__(self):
        Menu.__init__(self, 400, 300)
        self.panel = Panel(200, 150)
        self.add_widget(self.panel, (40, 80))

        self.add_widget(MenuLabel(), (90, 20))
        self.add_widget(Label('NonFocusable', focusable=False), (150, 20))

        first_panel_label = Label('Panel0')
        self.panel.add_widget(first_panel_label, (40, 20))
        self.panel.add_widget(Label('Panel1'), (120, 20))
        self.panel.add_widget(Label('Panel2'), (40, 60))
        self.panel.add_widget(Label('Panel3'), (120, 60))
        self.panel.add_widget(AdjustableBar(100, 14, filled=0.9),
                              (50, 100))

        side_panel = Panel(110, 220)
        self.add_widget(side_panel, (260, 40))

        grid = AdjustableVerticalGrid(110, 72, 2, 6)
        side_panel.add_widget(grid, AlignTopLeft())

        img = pygame.image.load(data_path('icon.png'))
        #img = pygame.image.load(data_path('test.png'))
        self.add_widget(ImageWidget(img), (8, 8))

        group = WidgetGroup(148, 20)
        group.add_widget(Label('Group0'), (10, 0))
        group.add_widget(Label('Group1'), (90, 0))
        self.add_widget(group, (60, 240))

        #self.crystallize()

        # Add cursor
        cursor = Cursor()
        cursor.bind(self, first_panel_label)


def main():
    librpg.init()
    librpg.config.menu_config.config(theme=ClassicMenuTheme())

    get_context_stack().stack_model(TestMenu())
    get_context_stack().gameloop()

if __name__ == '__main__':
    main()
