"""
The :mod:`config` module provides objects that configure several aspects
of LibRPG. These objects are in the module scope, so they can be accessed
as librpg.config.[object]. These object's attributes are used by several
modules, providing flexibility for LibRPG games.

The global configuration objects are:

    **graphics_config**
        GraphicsConfig object

    **dialog_config**
        DialogConfig object

    **game_config**
        GameConfig object

    **menu_config**
        MenuConfig object
"""

import pygame

from librpg.locals import *
from librpg import virtualscreen


class Config(object):

    """
    The Config objects are basically attribute containers with a shortcut
    to set several attributes at once, the Config.config() method.
    """

    def __init__(self, late_attributions=None):
        if late_attributions == None:
            self.late_attributions = []
        else:
            self.late_attributions = late_attributions

    def config(self, **kv):
        """
        Whatever keyword parameters are passed to config() will make that
        attribute be set to the desired value.
        """
        scheduled = {}

        for key, value in kv.iteritems():
            if hasattr(self, key):
                if key not in self.late_attributions:
                    setattr(self, key, value)
                else:
                    scheduled[key] = value
            else:
                raise Exception('config() does not take %s as parameter' % key)

        for key, value in scheduled.iteritems():
            setattr(self, key, value)


class GraphicsConfig(Config):

    """
    The GraphicsConfig contains attributes related to map and screen
    rendering.
    
    :attr:`camera_mode`
        CameraMode for displaying following the PartyAvatar on the map.
    
    :attr:`display_mode`
        Combination of flags that will be used to config the screen. Passed
        directly to pygame.display.set_mode().
    
    :attr:`screen_width`
        Game window width in pixels.
    
    :attr:`screen_height`
        Game window height in pixels.
    
    :attr:`object_width`
        MapObjects' width in pixels. Does not apply for ScenarioMapObjects.
    
    :attr:`object_height`
        MapObjects' height in pixels. Does not apply for ScenarioMapObjects.
    
    :attr:`tile_size`
        Tiles' width and height in pixels.
    
    :attr:`scale`
        Zoom to use when drawing anything on the screen. When 1, it will be
        drawn in the normal scale, which will look very small for low
        resolution graphics. Numbers higher than 1 will enlarge the screen
        while numbers lower than 1 will reduce it. Non-integers MAY be
        passed.
    
    :attr:`real_screen_dimensions`
        2-Tuple with height and width of the actual screen. Read-only.

    :attr:`animation_frame_period`
        Number of frames after which the next frame of tile animation will
        be displayed.
    """

    _screen_width = 400
    _screen_height = 300
    _tile_size = 16
    _object_height = 32
    _object_width = 24
    _scale = 2
    camera_mode = None
    display_mode = 0
    animation_frame_period = 15
    # display_mode = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN

    def __init__(self):
        Config.__init__(self)
        self.calc_screen_dimensions()
        self.calc_object_dimensions()
        self.calc_map_border_width()
        self.calc_map_border_height()

    def get_screen_width(self):
        return self._screen_width

    def set_screen_width(self, new_value):
        self._screen_width = new_value
        self.calc_map_border_width()
        self.calc_screen_dimensions()
        self.recreate_screeens()

    screen_width = property(get_screen_width, set_screen_width)

    def get_screen_height(self):
        return self._screen_height

    def set_screen_height(self, new_value):
        self._screen_height = new_value
        self.calc_map_border_height()
        self.calc_screen_dimensions()
        self.recreate_screeens()

    screen_height = property(get_screen_height, set_screen_height)

    def get_object_width(self):
        return self._object_width

    def set_object_width(self, new_value):
        self._object_width = new_value
        self.calc_object_dimensions()

    object_width = property(get_object_width, set_object_width)

    def get_object_height(self):
        return self._object_height

    def set_object_height(self, new_value):
        self._object_height = new_value
        self.calc_object_dimensions()

    object_height = property(get_object_height, set_object_height)

    def get_tile_size(self):
        return self._tile_size

    def set_tile_size(self, new_value):
        self._tile_size = new_value

    tile_size = property(get_tile_size, set_tile_size)

    def get_scale(self):
        return self._scale

    def set_scale(self, new_value):
        self._scale = new_value
        self.recreate_screeens()

    scale = property(get_scale, set_scale)

    def get_real_screen_dimensions(self):
        return (int(self.screen_dimensions[0] * self.scale),
                int(self.screen_dimensions[1] * self.scale))
    real_screen_dimensions = property(get_real_screen_dimensions)

    def calc_screen_dimensions(self):
        self.screen_dimensions = (self._screen_width, self._screen_height)

    def calc_object_dimensions(self):
        self.object_dimensions = (self._object_width, self._object_height)

    def calc_map_border_width(self):
        self.map_border_width = self._screen_width / 2

    def calc_map_border_height(self):
        self.map_border_height = self._screen_height / 2

    def recreate_screeens(self):
        virtualscreen.screen_container.create_screen(
                                                    self.real_screen_dimensions,
                                                    self.display_mode,
                                                    self.screen_dimensions,
                                                    self.scale)


class DialogConfig(Config):

    """
    The DialogConfig contains attributes related to dialog rendering.
    
    :attr:`font_name`
        Name of the font or font file to be used in dialogs.
    
    :attr:`font_size`
        Size to render the font in dialogs.
    
    :attr:`border_width`
        Space in pixels between the screen edge and the text box and
        between the text box and the text.
    
    :attr:`line_spacing`
        Space in pixels between text lines.
    
    :attr:`choice_line_spacing`
        Space in pixels between choice text lines.
    
    :attr:`bg_color`
        Tuple with the dialog's background colors.    
    
    :attr:`font_color`
        Tuple with the text font's color.
    
    :attr:`selected_font_color`
        Tuple with the text color to use for selected options in a
        ChoiceDialog.
    
    :attr:`not_selected_font_color`
        Tuple with the text color to use for options not selected in a
        ChoiceDialog.
    """

    font_name = 'Verdana'
    font_size = 12
    border_width = 15
    line_spacing = 2
    choice_line_spacing = 2
    bg_color = (128, 0, 128, 128)
    font_color = (255, 255, 255)
    selected_font_color = (255, 0, 0)
    not_selected_font_color = (128, 128, 128)


class GameConfig(Config):

    """
    The GameConfig contains attributes related to map and menu
    navigation and execution.

    :attr:`fps`
        How many frames per second the map will run (at most).

    :attr:`key_up`
        Set of keys that move the party up.

    :attr:`key_down`
        Set of keys that move the party down.

    :attr:`key_left`
        Set of keys that move the party left.

    :attr:`key_right`
        Set of keys that move the party right.

    :attr:`key_action`
        Set of keys that activate objects, advance or choose an option.

    :attr:`key_cancel`
        Set of keys that quit the game, cancel actions, go back.
    """
    
    fps = 30
    key_up = set([K_UP])
    key_down = set([K_DOWN])
    key_left = set([K_LEFT])
    key_right = set([K_RIGHT])
    key_action = set([K_RETURN, K_SPACE])
    key_cancel = set([K_ESCAPE])


class MenuConfig(Config):

    """
    The MenuConfig contains attributes related to menus.
    
    :attr:`theme`
        MenuTheme to use for menus, except when explicitly specified.
    """

    _theme = None

    def get_theme(self):
        if self._theme is None:
            theme = MenuTheme()
        return theme

    theme = property(get_theme)


graphics_config = GraphicsConfig()
dialog_config = DialogConfig()
game_config = GameConfig()
menu_config = MenuConfig()

from librpg.camera import PartyCentricCameraMode as DEFAULT_CAMERA_MODE
graphics_config.camera_mode = DEFAULT_CAMERA_MODE()
