import pygame

import librpg
import virtual_screen

class Config(object):

    def __init__(self, late_attributions=None):
    
        if late_attributions == None:
            self.late_attributions = []
        else:
            self.late_attributions = late_attributions

    def config(self, **kv):
    
        scheduled = {}
    
        for key, value in kv.iteritems():
            if hasattr(self, key):
                if key not in self.late_attributions:
                    setattr(self, key, value)
                else:
                    scheduled[key] = value
            else:
                raise Exception('config() does not take ' + key + ' as parameter.')
                
        for key, value in scheduled.iteritems():
            setattr(self, key, value)        


class GraphicsConfig(Config):

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
        self.camera_mode = None # Has to be None here to avoid circular import problems
        self.display_mode = GraphicsConfig.DEFAULT_DISPLAY_MODE
        
        self.calc_screen_dimensions()
        self.calc_object_dimensions()
        self.calc_map_border_width()
        self.calc_map_border_height()
        
    def config(self, **kv):
    
        scheduled = {}
    
        for key, value in kv.iteritems():
            if hasattr(self, key):
                if key != 'display_mode':
                    setattr(self, key, value)
                else:
                    scheduled[key] = value
            else:
                raise Exception('GraphicsConfig.config() does not take ' + key + ' as parameter.')
                
        for key, value in scheduled.iteritems():
            setattr(self, key, value)        

    def get_screen_width(self):
    
        return self._screen_width
        
    def set_screen_width(self, new_value):
    
        self._screen_width = new_value
        self.calc_map_border_width()
        self.calc_screen_dimensions()
        self.recreate_screeens()
    
    def get_screen_height(self):
    
        return self._screen_height
        
    def set_screen_height(self, new_value):
    
        self._screen_height = new_value
        self.calc_map_border_height()
        self.calc_screen_dimensions()
        self.recreate_screeens()
    
    def get_object_width(self):
    
        return self._object_width
        
    def set_object_width(self, new_value):
    
        self._object_width = new_value
        self.calc_object_dimensions()
    
    def get_object_height(self):
    
        return self._object_height
        
    def set_object_height(self, new_value):
    
        self._object_height = new_value
        self.calc_object_dimensions()
    
    def get_tile_size(self):
    
        return self._tile_size
    
    def set_tile_size(self, new_value):
    
        self._tile_size = new_value
    
    def get_scale(self):
    
        return self._scale
    
    def set_scale(self, new_value):
    
        self._scale = new_value
        self.recreate_screeens()
        
    def get_real_screen_dimensions(self):
    
        return (self.screen_dimensions[0] * self.scale, self.screen_dimensions[1] * self.scale)
    
    def calc_screen_dimensions(self):
    
        self.screen_dimensions = (self._screen_width, self._screen_height)
    
    def calc_object_dimensions(self):
    
        self.object_dimensions = (self._object_width, self._object_height)
    
    def calc_map_border_width(self):
    
        self.map_border_width = self._screen_width / 2        
    
    def calc_map_border_height(self):
    
        self.map_border_height = self._screen_height / 2        
    
    def recreate_screeens(self):
    
        virtual_screen.screen_container.create_screen(self.real_screen_dimensions, self.display_mode, self.screen_dimensions, self.scale)
    
    screen_width = property(get_screen_width, set_screen_width)
    screen_height = property(get_screen_height, set_screen_height)
    object_width = property(get_object_width, set_object_width)
    object_height = property(get_object_height, set_object_height)
    tile_size = property(get_tile_size, set_tile_size)
    scale = property(get_scale, set_scale)
    real_screen_dimensions = property(get_real_screen_dimensions)

class DialogConfig(Config):
    
    DEFAULT_FONT_NAME = 'Verdana'
    DEFAULT_FONT_SIZE = 12
    DEFAULT_BORDER_WIDTH = 15
    DEFAULT_LINE_SPACING = 2
    DEFAULT_BG_COLOR = (128, 0, 128, 128)
    DEFAULT_FONT_COLOR = (255, 255, 255)
    
    def __init__(self):
    
        self.font_name = DialogConfig.DEFAULT_FONT_NAME
        self.font_size = DialogConfig.DEFAULT_FONT_SIZE
        self.border_width = DialogConfig.DEFAULT_BORDER_WIDTH
        self.line_spacing = DialogConfig.DEFAULT_LINE_SPACING
        self.bg_color = DialogConfig.DEFAULT_BG_COLOR
        self.font_color = DialogConfig.DEFAULT_FONT_COLOR

graphics_config = GraphicsConfig()
dialog_config = DialogConfig()

from camera import PartyCentricCameraMode as DEFAULT_CAMERA_MODE
graphics_config.camera_mode = DEFAULT_CAMERA_MODE()
