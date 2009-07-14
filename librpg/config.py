import pygame

import librpg
from camera import PartyCentricCameraMode

class GraphicsConfig(object):

    DEFAULT_SCREEN_WIDTH = 640
    DEFAULT_SCREEN_HEIGHT = 480
    DEFAULT_TILE_SIZE = 16
    DEFAULT_OBJECT_HEIGHT = 32
    DEFAULT_OBJECT_WIDTH = 24
    DEFAULT_FIXED_CAMERA_WHERE_POSSIBLE = True
    DEFAULT_VERTICAL_CAMERA_TOLERANCE = 0
    DEFAULT_HORIZONTAL_CAMERA_TOLERANCE = 0
    
    def __init__(self):
        self._screen_width = GraphicsConfig.DEFAULT_SCREEN_WIDTH
        self._screen_height = GraphicsConfig.DEFAULT_SCREEN_HEIGHT
        self.tile_size = GraphicsConfig.DEFAULT_TILE_SIZE
        self.object_height = GraphicsConfig.DEFAULT_OBJECT_HEIGHT
        self.object_width = GraphicsConfig.DEFAULT_OBJECT_WIDTH
        self.fixed_camera_where_possible = GraphicsConfig.DEFAULT_FIXED_CAMERA_WHERE_POSSIBLE # Whether, when in a small map, the camera will stay fixed.
        self.vertical_camera_tolerance = GraphicsConfig.DEFAULT_VERTICAL_CAMERA_TOLERANCE # How many pixels the party can move away from the center of the screen before the camera starts to follow.
        self.horizontal_camera_tolerance = GraphicsConfig.DEFAULT_HORIZONTAL_CAMERA_TOLERANCE
        
    def get_screen_width(self):
        return self._screen_width
        
    def set_screen_width(self, new_value):
        self._screen_width = new_value
        librpg.screen = pygame.display.set_mode(self.screen_dimensions)
    
    def get_screen_height(self):
        return self._screen_height
        
    def set_screen_height(self, new_value):
        self._screen_height = new_value
        librpg.screen = pygame.display.set_mode(self.screen_dimensions)
    
    def get_screen_dimensions(self):
        return (self.screen_width, self.screen_height)
    
    screen_width = property(get_screen_width, set_screen_width)
    screen_height = property(get_screen_height, set_screen_height)
    screen_dimensions = property(get_screen_dimensions)

graphics_config = GraphicsConfig()
