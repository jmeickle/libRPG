import pygame

import librpg
import virtual_screen

class GraphicsConfig(object):

    DEFAULT_SCREEN_WIDTH = 400
    DEFAULT_SCREEN_HEIGHT = 300
    DEFAULT_TILE_SIZE = 16
    DEFAULT_OBJECT_HEIGHT = 32
    DEFAULT_OBJECT_WIDTH = 24
    DEFAULT_SCALE = 2
    DEFAULT_DISPLAY_MODE = 0
    #DEFAULT_DISPLAY_MODE = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN
    
    def __init__(self):
    
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
        self.calc_object_x_adjustment()
        self.calc_object_y_adjustment()
        
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
        self.calc_object_x_adjustment()
        self.calc_object_dimensions()
    
    def get_object_height(self):
    
        return self._object_height
        
    def set_object_height(self, new_value):
    
        self._object_height = new_value
        self.calc_object_y_adjustment()
        self.calc_object_dimensions()
    
    def get_tile_size(self):
    
        return self._tile_size
    
    def set_tile_size(self, new_value):
    
        self._tile_size = new_value
        self.calc_object_x_adjustment()
        self.calc_object_y_adjustment()
    
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
    
    def calc_object_x_adjustment(self):
    
        self.object_x_adjustment = - (self._object_width - self._tile_size) / 2
        
    def calc_object_y_adjustment(self):
    
        self.object_y_adjustment = - (self._object_height - self._tile_size)
    
    def recreate_screeens(self):
    
        librpg.screen = librpg.init_virtual_screen(self.screen_dimensions, librpg.real_screen, self.scale)
        librpg.real_screen = librpg.init_real_screen(self.real_screen_dimensions, self.display_mode)
    
    screen_width = property(get_screen_width, set_screen_width)
    screen_height = property(get_screen_height, set_screen_height)
    object_width = property(get_object_width, set_object_width)
    object_height = property(get_object_height, set_object_height)
    tile_size = property(get_tile_size, set_tile_size)
    scale = property(get_scale, set_scale)
    real_screen_dimensions = property(get_real_screen_dimensions)

graphics_config = GraphicsConfig()

from camera import PartyCentricCameraMode as DEFAULT_CAMERA_MODE
graphics_config.camera_mode = DEFAULT_CAMERA_MODE()
