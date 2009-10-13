import pygame
from pygame import *

import librpg
from librpg.menu import (MenuController, Menu, Panel, Label, ArrowCursor,
                         ImageWidget, WidgetGroup)
from librpg.context import get_context_stack
from librpg.path import data_path

class MenuLabel(Label):

    def __init__(self):
        Label.__init__(self, 'Menu')

    def activate(self):
        print 'MenuLabel activated'
        return True

    def process_event(self, event):
        print event
        if event.type == KEYDOWN:
            print 'MenuLabel captured key press %d' % event.key
        return False


class TestMenu(Menu):

    def __init__(self):
        Menu.__init__(self, 400, 300)
        self.panel = Panel(200, 150)
        self.add_widget(self.panel, (40, 80))
        
        self.add_widget(MenuLabel(), (90, 20))
        self.add_widget(Label('NonFocusable', focusable=False), (150, 20))
        
        first_panel_label = Label('Panel0')
        self.panel.add_widget(first_panel_label, (40, 40))
        self.panel.add_widget(Label('Panel1'), (120, 40))
        self.panel.add_widget(Label('Panel2'), (40, 80))
        self.panel.add_widget(Label('Panel3'), (120, 80))

        self.side_panel = Panel(110, 220)
        self.add_widget(self.side_panel, (260, 40))
        for i in range(6):
            label = Label('SidePanel%d' % i)
            pos = (20, 20 + 30 * i)
            self.side_panel.add_widget(label, pos)

        img = pygame.image.load(data_path('icon.png'))
        self.add_widget(ImageWidget(img), (8, 8))

        group = WidgetGroup(148, 20)
        group.add_widget(Label('Group0'), (10, 0))
        group.add_widget(Label('Group1'), (90, 0))
        self.add_widget(group, (60, 240))
        self.crystallize()

        # Add cursor
        cursor = ArrowCursor()
        cursor.bind(self, first_panel_label)


def main():
    librpg.init()

    c = MenuController(TestMenu())
    get_context_stack().stack_context(c)
    get_context_stack().gameloop()

if __name__ == '__main__':
    main()

