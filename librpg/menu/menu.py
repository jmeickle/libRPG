from pygame.locals import *

from librpg.context import Context
from librpg.virtualscreen import get_screen
from librpg.config import game_config

from div import Div

class Menu(Div):

    def __init__(self, width, height, x=0, y=0, theme=None):
        Div.__init__(self, width, height, theme)
        self.x = x
        self.y = y

    def draw(self):
        Div.draw(self)
        Div.render(self, get_screen(), self.x, self.y)

    def process_event(self, event):
        if event.type == KEYDOWN:
            if event.key in game_config.key_cancel:
                self.controller.stop()


class MenuController(Context):

    def __init__(self, menu, parent=None):
        assert menu is not None, 'menu cannot be None'
        Context.__init__(self, parent)
        self.menu = menu
        menu.controller = self

    def draw(self):
        self.menu.draw()

    def update(self):
        self.menu.update()

    def process_event(self, event):
        return self.menu.process_event(event)
