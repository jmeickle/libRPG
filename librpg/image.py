import pygame

from locals import *
from config import *

class Image:

    def __init__(self, surface):
    
        self.surface = surface
        self.width, self.height = self.surface.get_width(), self.surface.get_height()
        
    def get_surface(self, object=None):
    
        return self.surface

class TileImage(Image):

    """
    This class represents a Tile image, which may include simple animation cycles.
    """
    
    pass

class ObjectImage(Image):

    """
    This class represents a MapObject image, which may include simple animation cycles and movement animation.
    """

    DEFAULT_OBJECT_IMAGE_BASIC_ANIMATION = [[1, 2], [1, 0]]
        
    DIRECTION_TO_INDEX_MAP = {UP: 0, RIGHT: 1, DOWN: 2, LEFT: 3}

    def __init__(self, filename, index=0, basic_animation=DEFAULT_OBJECT_IMAGE_BASIC_ANIMATION, frame_number=None):
    
        # Calculate frame count
        if frame_number is None:
            self.frame_number = max([max(i) for i in basic_animation]) + 1
        else:
            self.frame_number = frame_number
    
        # Load file
        file_surface = pygame.image.load(filename)
        
        object_chunk_width, object_chunk_height = self.frame_number * graphics_config.object_width, 4 * graphics_config.object_height
        chunks_per_line = file_surface.get_width() / object_chunk_width
        
        x = index % chunks_per_line
        y = index / chunks_per_line
    
        Image.__init__(self, file_surface.subsurface((x * object_chunk_width, y * object_chunk_height), (object_chunk_width, object_chunk_height)))
        
        # Create a sprite matrix [facing x frame]
        self.frames = []
        for facing in [UP, RIGHT, DOWN, LEFT]:
            y = ObjectImage.DIRECTION_TO_INDEX_MAP[facing]
            phases = []
            self.frames.append(phases)
            for x in range(self.frame_number):
                phases.append(self.surface.subsurface(pygame.Rect((x * graphics_config.object_width, y * graphics_config.object_height), graphics_config.object_dimensions)))
                
        self.width, self.height = graphics_config.object_width, graphics_config.object_height
        
        # Build animation maps
        self.basic_animation = basic_animation
        self.animation_maps = [(dict((speed, [animation[(phase*len(animation))/speed] for phase in range(speed)]) for speed in SPEEDS)) for animation in basic_animation]
        self.current_animation = 0
        self.last_observed_movement_phase = 0

    def get_surface(self, object=None, facing=None, phase=None):
    
        if object is not None:
            if object.sliding:
                return self.frames[ObjectImage.DIRECTION_TO_INDEX_MAP[object.facing]][1]
            else:
                self.next_animation(object)
                return self.frames[ObjectImage.DIRECTION_TO_INDEX_MAP[object.facing]][self.animation_maps[self.current_animation][object.speed][object.movement_phase]]
        elif facing is not None and phase is not None:
            return self.frames[ObjectImage.DIRECTION_TO_INDEX_MAP[facing]][self.animation_maps[self.current_animation][NORMAL_SPEED][phase]]
        else:
            raise Exception('object_image.get_surface() must either be called with object set OR with facing and phase parameters.')

    def next_animation(self, object):
    
        if object.movement_phase > self.last_observed_movement_phase:
            self.current_animation = (self.current_animation + 1) % len(self.basic_animation)
        self.last_observed_movement_phase = object.movement_phase
        