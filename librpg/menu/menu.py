from pygame.locals import *

from librpg.context import Context, get_context_stack
from librpg.virtualscreen import get_screen
from librpg.config import game_config
from librpg.util import check_direction
from librpg.locals import *

from div import Div

class Menu(Div):

    def __init__(self, width, height, x=0, y=0, theme=None):
        Div.__init__(self, width, height, theme)
        self.x = x
        self.y = y
        self._cursor = None
        self.menu = self
        self.all_widgets = []

    def draw(self):
        Div.draw(self)
        Div.render(self, get_screen(), self.x, self.y)

    # Use cursor.bind instead
    def add_cursor(self, cursor):
        if self._cursor is not None:
            return False
        else:
            self._cursor = cursor
            return True

    def remove_cursor(self):
        result = self._cursor
        self._cursor = None
        return result

    def register_widget(self, widget):
        self.all_widgets.append(widget)

    def unregister_widget(self, widget):
        self.all_widgets.remove(widget)


class MenuController(Context):

    COMMAND_COOLDOWN = 5

    def __init__(self, menu, parent=None):
        assert menu is not None, 'menu cannot be None'
        Context.__init__(self, parent)
        self.menu = menu
        menu.controller = self
        self.command_queue = []
        self.command_cooldown = 0

    def draw(self):
        self.menu.draw()

    def update(self):
        cursor = self.menu._cursor
        if cursor is not None:
            if self.command_cooldown > 0:
                self.command_cooldown -= 1
            elif self.command_queue:
                direction = self.command_queue[0]
                if direction != ACTIVATE:
                    cursor.step(direction)
                    self.command_cooldown = MenuController.COMMAND_COOLDOWN
            cursor.update()
        self.menu.update()

    def process_event(self, event):
        if event.type == QUIT:
            get_context_stack().stop()
            return True
        elif event.type == KEYDOWN:
            direction = check_direction(event.key)
            if direction is not None and\
               not direction in self.command_queue:
                self.command_queue.append(direction)
                return True
            elif event.key in game_config.key_action:
                if not ACTIVATE in self.command_queue:
                    self.command_queue.insert(0, ACTIVATE)
                return True
            elif event.key in game_config.key_cancel:
                self.stop()
                return True
        elif event.type == KEYUP:
            direction = check_direction(event.key)
            if direction is not None and\
               direction in self.command_queue:
                self.command_queue.remove(direction)
                return True
            elif event.key in game_config.key_action \
                 and ACTIVATE in self.command_queue:
                self.command_queue.remove(ACTIVATE)
                return True
        return False
