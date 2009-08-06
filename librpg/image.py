import pygame

from locals import *
from config import *

class Image:

    def __init__(self, surface):
    
        self.surface = surface
        
    def get_surface(self, object=None):
    
        return self.surface

class TileImage(Image):

    """
    This class represents a Tile image, which may include simple animation cycles.
    """
    
    pass

OBJECT_IMAGE_BASIC_ANIMATION_MAP = [1, 2, 1, 0]
    
class ObjectImage(Image):

    """
    This class represents a MapObject image, which may include simple animation cycles and movement animation.
    """

    DIRECTION_TO_INDEX_MAP = {UP: 0, RIGHT: 1, DOWN: 2, LEFT: 3}

    ANIMATION_MAPS = dict((speed, [OBJECT_IMAGE_BASIC_ANIMATION_MAP[(phase*4)/speed] for phase in range(speed)]) for speed in SPEEDS)
    
    def __init__(self, filename, index=0):
    
        file_surface = pygame.image.load(filename)
        
        object_chunk_width, object_chunk_height = 3 * graphics_config.object_width, 4 * graphics_config.object_height
        chunks_per_line = file_surface.get_width() / object_chunk_width
        
        x = index % chunks_per_line
        y = index / chunks_per_line
    
        Image.__init__(self, file_surface.subsurface((x * object_chunk_width, y * object_chunk_height), (object_chunk_width, object_chunk_height)))
        self.frames = []
        for facing in [UP, RIGHT, DOWN, LEFT]:
            y = ObjectImage.DIRECTION_TO_INDEX_MAP[facing]
            phases = []
            self.frames.append(phases)
            for x in range(3):
                phases.append(self.surface.subsurface(pygame.Rect((x * graphics_config.object_width, y * graphics_config.object_height), graphics_config.object_dimensions)))

    def get_surface(self, object=None, facing=None, phase=None):
    
        if object is not None:
            if object.sliding:
                return self.frames[ObjectImage.DIRECTION_TO_INDEX_MAP[object.facing]][1]
            else:
                return self.frames[ObjectImage.DIRECTION_TO_INDEX_MAP[object.facing]][ObjectImage.ANIMATION_MAPS[object.speed][object.movement_phase]]
        elif facing is not None and phase is not None:
            return self.frames[ObjectImage.DIRECTION_TO_INDEX_MAP[facing]][ObjectImage.ANIMATION_MAPS[NORMAL_SPEED][phase]]
        else:
            raise Exception('object_image.get_surface() must either be called with object set OR with facing and phase parameters.')
    