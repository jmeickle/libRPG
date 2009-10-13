import pygame
from pygame.locals import *

from librpg.context import Context, get_context_stack
from librpg.virtualscreen import get_screen
from librpg.config import game_config
from librpg.util import check_direction, fill_with_surface, descale_point
from librpg.locals import *

from div import Div

class Menu(Div):

    def __init__(self, width, height, x=0, y=0, theme=None, bg=None):
        Div.__init__(self, width, height, theme)
        self.x = x
        self.y = y
        self.cursor = None
        self.menu = self
        self.all_widgets = []
        self.init_bg(bg)

    def init_bg(self, bg):
        self.bg = pygame.Surface((self.width, self.height)).convert_alpha()
        self.bg.fill((0, 0, 0, 255))
        if bg is not None:
            fill_with_surface(self.bg, bg)

    def draw(self):
        scr = get_screen()
        scr.blit(self.bg, (self.x, self.y))
        Div.draw(self)
        Div.render(self, scr, self.x, self.y)
        self.cursor.draw()
        self.cursor.render(scr)

    # Use cursor.bind instead
    def add_cursor(self, cursor):
        if self.cursor is not None:
            return False
        else:
            self.cursor = cursor
            return True

    def remove_cursor(self):
        result = self.cursor
        self.cursor = None
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
        cursor = self.menu.cursor
        if cursor is not None:
            if self.command_cooldown > 0:
                self.command_cooldown -= 1
            elif self.command_queue:
                direction = self.command_queue[0]
                if direction == ACTIVATE:
                    self.activate()
                else:
                    cursor.step(direction)
                    self.command_cooldown = MenuController.COMMAND_COOLDOWN
            cursor.update()
        self.menu.update()

    def activate(self):
        cursor = self.menu.cursor
        if cursor is not None:
            w = cursor.widget
            while w is not None:
                if w.activate():
                    return
                w = w.parent

    def process_event(self, event):
        cursor = self.menu.cursor
        if cursor is not None:
            w = cursor.widget
            while w is not None:
                if w.process_event(event):
                    return True
                w = w.parent
        return self.menu_process_event(event)

    def menu_process_event(self, event):
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
        elif event.type == MOUSEMOTION:
            self.process_mouse_motion(event)
        return False

    def process_mouse_motion(self, event):
        cursor = self.menu.cursor
        if cursor is None:
            return
        pos = descale_point(event.pos)
        print 'process_mouse_motion pos', pos
        if cursor.widget.contains_point(pos):
            return
        for w in self.menu.all_widgets:
            if w.focusable and w.contains_point(pos):
                cursor.move_to(w)
