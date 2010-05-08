import pygame

from librpg.context import Context, Model, get_context_stack
from librpg.virtualscreen import get_screen
from librpg.config import game_config
from librpg.util import fill_with_surface, descale_point
from librpg.image import Image
from librpg.input import Input
from librpg.locals import (SRCALPHA, MOUSEMOTION, UP, DOWN, LEFT, RIGHT,
                           M_1, M_3)

from librpg.menu.div import Div


class Menu(Model, Div):

    """
    A Menu is the outermost container for widgets, representing a whole
    menu ran by a MenuController.

    Menus provide all methods a Div does, most notably add_widget(),
    which is used to put any widgets or Divs on the Menu.

    *width* and *height* specify the dimensions of the menu in pixels.
    *x* and *y* specify the position at which the top left of the menu
    will be on the screen.

    *theme* is a MenuTheme that will be used to render that menu, and
    defaults to the default_theme in librpg.config.menu_config.

    *bg* can be a color or a pygame Surface that will be drawn as the
    menu's background.

    *mouse_control* can be Menu.MOUSE_OFF, Menu.MOUSE_STRICT or
    Menu.MOUSE_LOOSE. MOUSE_OFF will disable mouse control for the menu,
    MOUSE_STRICT will cause the cursor to move to widgets touched by the
    mouse pointer, and MOUSE_LOOSE will move it always to the nearest
    widget.
    """

    MOUSE_OFF = 0
    MOUSE_STRICT = 1
    MOUSE_LOOSE = 2

    def __init__(self, width, height, x=0, y=0, theme=None, bg=None,
                 mouse_control=MOUSE_LOOSE, blocking=True):
        Model.__init__(self)
        Div.__init__(self, width, height, False, theme)
        self.x = x
        self.y = y
        self.cursor = None
        self.menu = self
        self.all_widgets = []
        self.init_bg(bg)
        assert mouse_control in (Menu.MOUSE_OFF,
                                 Menu.MOUSE_STRICT,
                                 Menu.MOUSE_LOOSE),\
                                'mouse_control must be 0, 1 or 2'
        self.mouse_control = mouse_control
        self.blocking = blocking

        self.should_close = False

    def init_bg(self, bg):
        if bg is not None:
            bg_surf = pygame.Surface((self.width, self.height), SRCALPHA, 32)\
                      .convert_alpha()
            if isinstance(bg, tuple) and len(bg) >= 3:
                bg_surf.fill(bg)
            else:
                fill_with_surface(bg_surf, bg)
            self.bg = Image(bg_surf)
        else:
            r = pygame.Rect(0, 0, self.width, self.height)
            self.bg = self.theme.draw_menu_bg(r)

    def draw(self):
        scr = get_screen()
        scr.blit(self.bg.get_surface(), (self.x, self.y))
        Div.draw(self)
        Div.render(self, scr, self.x, self.y)
        if self.cursor is not None:
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
        if self.cursor is not None and self.cursor.widget is widget:
            self.cursor.move_to()

    def open(self):
        """
        Open the menu.
        """
        get_context_stack().stack_model(self)

    def close(self):
        """
        Close the menu.
        """
        self.should_close = True

    def activate(self):
        """
        *Virtual.*
        """
        pass

    def create_controller(self):
        return MenuController(self, self.controller_parent)

    def is_done(self):
        return self.controller.is_done()
    
    def update_input(self):
        cursor = self.menu.cursor
        if cursor is not None:
            w = cursor.widget
            while w.parent is not None:
                #print 'update_input %s' % w
                w.update_input()
                w = w.parent

    def reposition_cursor(self, pos):
        if self.menu.mouse_control == Menu.MOUSE_STRICT:
            self.menu.__reposition_cursor_strict(pos)
        else:
            self.menu.__reposition_cursor_loose(pos)

    def __reposition_cursor_strict(self, pos):
        cursor = self.cursor
        if cursor.widget.contains_point(pos):
            return
        for w in self.all_widgets:
            if w.focusable and w.contains_point(pos):
                cursor.move_to(w)
                return

    def __reposition_cursor_loose(self, pos):
        cursor = self.cursor
        best = (None, 999999)
        for w in self.all_widgets:
            if w.focusable:
                dist = w.distance_to_point(pos)
                if dist < best[1]:
                    best = (w, dist)
        if best[0] is not None:
            cursor.move_to(best[0])


class MenuController(Context):

    COMMAND_COOLDOWN = 5

    def __init__(self, menu, parent=None):
        assert menu is not None, 'menu cannot be None'
        Context.__init__(self, parent)
        self.menu = menu
        menu.controller = self
        self.command_queue = []
        self.command_cooldown = 0
        self.done = False

    def draw(self):
        self.menu.draw()

    def update(self):
        if self.menu.should_close:
            self.done = True
            self.stop()
            return False
        if self.menu.cursor is not None:
            self.menu.cursor.update()
        self.menu.update()
        self.menu.update_input()
        if self.command_cooldown > 0:
            self.command_cooldown -= 1
        else:
            self.__update_input()
        return self.menu.blocking

    def activate(self):
        cursor = self.menu.cursor
        if cursor is not None:
            w = cursor.widget
            while w is not None:
                if w.activate():
                    return
                w = w.parent
        else:
            self.menu.activate()

    def step(self, direction):
        cursor = self.menu.cursor
        if cursor is not None:
            w = cursor.widget
            do_normal_step = True
            while w is not None and do_normal_step:
                if w.step(direction):
                    do_normal_step = False
                w = w.parent
        else:
            do_normal_step = False

        if do_normal_step:
            cursor.step(direction)

    def __update_input(self):
        #print '__update_input'
        for key in game_config.key_cancel:
            if Input.was_pressed(key) is not None:
                self.menu.close()
                self.command_cooldown = MenuController.COMMAND_COOLDOWN
                return
            
        for key in game_config.key_action:
            if Input.was_pressed(key) is not None:
                self.activate()
                self.command_cooldown = MenuController.COMMAND_COOLDOWN
                return
        
        if self.menu.cursor is None:
                return
        
        for key in game_config.key_up:
            if Input.motion(key):
                self.step(UP)
                self.command_cooldown = MenuController.COMMAND_COOLDOWN
                return

        for key in game_config.key_down:
            if Input.motion(key):
                self.step(DOWN)
                self.command_cooldown = MenuController.COMMAND_COOLDOWN
                return

        for key in game_config.key_left:
            if Input.motion(key):
                self.step(LEFT)
                self.command_cooldown = MenuController.COMMAND_COOLDOWN
                return

        for key in game_config.key_right:
            if Input.motion(key):
                self.step(RIGHT)
                self.command_cooldown = MenuController.COMMAND_COOLDOWN
                return

        self.__update_mouse_input()

    def __update_mouse_input(self):
        evt = Input.was_pressed(M_1)
        if evt is not None:
            if self.menu.cursor is not None:
                w = self.menu.cursor.widget
                if w is not None:
                    x, y = descale_point(evt.pos)
                    widget_x, widget_y = w.get_menu_position()
                    captured = w.left_click(x - widget_x, y - widget_y)
                    if not captured:
                        self.activate()

        evt = Input.was_pressed(M_3)
        if evt is not None:
            if self.menu.cursor is not None:
                w = self.menu.cursor.widget
                if w is not None:
                    x, y = descale_point(evt.pos)
                    widget_x, widget_y = w.get_menu_position()
                    captured = w.right_click(x - widget_x, y - widget_y)

        self.__update_mouse_motion()
        
    def __update_mouse_motion(self):
        if self.menu.mouse_control == Menu.MOUSE_OFF:
            return False

        cursor = self.menu.cursor
        if cursor is None:
            return False

        event = Input.event(MOUSEMOTION)
        if event is not None:
            pos = descale_point(event.pos)
            self.menu.reposition_cursor(pos)

    def is_done(self):
        return self.done

    def __repr__(self):
        return '<MenuController of %s>' % self.menu
