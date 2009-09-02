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

    **map_config**
        MapConfig object

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
    """

    DEFAULT_SCREEN_WIDTH = 400
    DEFAULT_SCREEN_HEIGHT = 300
    DEFAULT_TILE_SIZE = 16
    DEFAULT_OBJECT_HEIGHT = 32
    DEFAULT_OBJECT_WIDTH = 24
    DEFAULT_SCALE = 2
    DEFAULT_DISPLAY_MODE = 0
    #DEFAULT_DISPLAY_MODE = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN

    def __init__(self):
        Config.__init__(self, late_attributions=['display_mode'])
        self._screen_width = GraphicsConfig.DEFAULT_SCREEN_WIDTH
        self._screen_height = GraphicsConfig.DEFAULT_SCREEN_HEIGHT
        self._tile_size = GraphicsConfig.DEFAULT_TILE_SIZE
        self._object_height = GraphicsConfig.DEFAULT_OBJECT_HEIGHT
        self._object_width = GraphicsConfig.DEFAULT_OBJECT_WIDTH
        self._scale = GraphicsConfig.DEFAULT_SCALE
        self.camera_mode = None # avoid circular import problems
        self.display_mode = GraphicsConfig.DEFAULT_DISPLAY_MODE

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

    DEFAULT_FONT_NAME = 'Verdana'
    DEFAULT_FONT_SIZE = 12
    DEFAULT_BORDER_WIDTH = 15
    DEFAULT_LINE_SPACING = 2
    DEFAULT_BG_COLOR = (128, 0, 128, 128)
    DEFAULT_FONT_COLOR = (255, 255, 255)
    DEFAULT_SELECTED_FONT_COLOR = (255, 0, 0)
    DEFAULT_NOT_SELECTED_FONT_COLOR = (128, 128, 128)

    def __init__(self):
        Config.__init__(self)
        self.font_name = DialogConfig.DEFAULT_FONT_NAME
        self.font_size = DialogConfig.DEFAULT_FONT_SIZE
        self.border_width = DialogConfig.DEFAULT_BORDER_WIDTH
        self.line_spacing = DialogConfig.DEFAULT_LINE_SPACING
        self.bg_color = DialogConfig.DEFAULT_BG_COLOR
        self.font_color = DialogConfig.DEFAULT_FONT_COLOR
        self.selected_font_color = DialogConfig.DEFAULT_SELECTED_FONT_COLOR
        self.not_selected_font_color = \
                                    DialogConfig.DEFAULT_NOT_SELECTED_FONT_COLOR


class MapConfig(Config):

    """
    The MapConfig contains attributes related to map navigation and
    execution.

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
    
    DEFAULT_KEY_UP = set([K_UP])
    DEFAULT_KEY_DOWN = set([K_DOWN])
    DEFAULT_KEY_LEFT = set([K_LEFT])
    DEFAULT_KEY_RIGHT = set([K_RIGHT])
    DEFAULT_KEY_ACTION = set([K_RETURN, K_SPACE])
    DEFAULT_KEY_CANCEL = set([K_ESCAPE])
    
    def __init__(self):
        Config.__init__(self)
        self.key_up = MapConfig.DEFAULT_KEY_UP
        self.key_down = MapConfig.DEFAULT_KEY_DOWN
        self.key_left = MapConfig.DEFAULT_KEY_LEFT
        self.key_right = MapConfig.DEFAULT_KEY_RIGHT
        self.key_action = MapConfig.DEFAULT_KEY_ACTION
        self.key_cancel = MapConfig.DEFAULT_KEY_CANCEL


graphics_config = GraphicsConfig()
dialog_config = DialogConfig()
map_config = MapConfig()

from librpg.camera import PartyCentricCameraMode as DEFAULT_CAMERA_MODE
graphics_config.camera_mode = DEFAULT_CAMERA_MODE()
