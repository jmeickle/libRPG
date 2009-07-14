import pygame

from util import Direction
from mapobject import *
from config import *

class Image:

    def __init__(self, surface):
        self.surface = surface
        
    def get_surface(self):
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

    DIRECTION_TO_INDEX_MAP = {Direction.UP: 0, Direction.RIGHT: 1, Direction.DOWN: 2, Direction.LEFT: 3}

    ANIMATION_MAPS = dict((speed, [OBJECT_IMAGE_BASIC_ANIMATION_MAP[(phase*4)/speed] for phase in range(speed)]) for speed in MapObject.SPEEDS)
    #ANIMATION_MAPS = dict((speed, [OBJECT_IMAGE_BASIC_ANIMATION_MAP[phase%4] for phase in range(speed)]) for speed in MapObject.SPEEDS)
    
    def __init__(self, surface):
        Image.__init__(self, surface)
        self.frames = []
        for facing in [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]:
            y = ObjectImage.DIRECTION_TO_INDEX_MAP[facing]
            phases = []
            self.frames.append(phases)
            for x in range(3):
                phases.append(self.surface.subsurface(pygame.Rect((x * GraphicsConfig.OBJECT_WIDTH, y * GraphicsConfig.OBJECT_HEIGHT), (GraphicsConfig.OBJECT_WIDTH, GraphicsConfig.OBJECT_HEIGHT))))

    def get_surface(self, object=None, facing=None, phase=None):
        if object is not None:
            return self.frames[ObjectImage.DIRECTION_TO_INDEX_MAP[object.facing]][ObjectImage.ANIMATION_MAPS[object.speed][object.movement_phase]]
        elif facing is not None and phase is not None:
            return self.frames[ObjectImage.DIRECTION_TO_INDEX_MAP[facing]][ObjectImage.ANIMATION_MAPS[MapObject.NORMAL_SPEED][phase]]
        else:
            raise Exception('object_image.get_surface() must either be called with object set OR with facing and phase parameters.')
    