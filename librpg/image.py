import pygame

from librpg.locals import *
from librpg.config import *


class Image(object):

    """
    A simple static image.
    
    This is the base class for more complex and animated images.
    """

    def __init__(self, surface):
        """
        *Constructor.*
        
        Pass the *surface* that will be stored in the image. Note
        that the surface is not copied, which means it should not be
        altered after being passed to this class.
    
        :attr:`surface`
            Pygame Surface containing the image.
            
        :attr:`width`
            Image width in pixels.

        :attr:`height`
            Image height in pixels.
        """
        self.surface = surface
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

    def get_surface(self, obj=None):
        """
        *Virtual.*
        
        Return a surface with how the image is to be rendered at the
        moment.
        """
        return self.surface


class TileImage(Image):

    """
    A scenario or terrain tile image.

    This class represents a Tile image, which will include simple
    animation cycles in the future. For now it is just a static image.
    """

    pass


class ObjectImage(Image):

    """
    A MapObject image.

    This class represents a MapObject image, which may include simple
    animation cycles and movement animation.
    """

    DEFAULT_OBJECT_IMAGE_BASIC_ANIMATION = [[1, 2], [1, 0]]
    DIRECTION_TO_INDEX_MAP = {UP: 0, RIGHT: 1, DOWN: 2, LEFT: 3}

    def __init__(self, filename, index=0,
                 basic_animation=DEFAULT_OBJECT_IMAGE_BASIC_ANIMATION,
                 frame_number=None):
        """
        *Constructor.*
        
        The frames will be loaded from *filename*, which should be a
        map object image file - a bitmap with a special format for the
        frames. Since there can be more than one map object image in
        the file, which of them should be loaded is specified by the
        *index* parameter.
        
        The image's animation is described by *basic_animation*.
        The animation of an object during a step is described by a list
        of the ids of the frames to be shown. *basic_animation*
        should be a list of these lists with the order in which these
        animations will represent a step.
        
        The default animation map is [[1, 2], [1, 0]], which means that
        every other step will be animated with [1, 2] and the others
        with [1, 0]. [1, 2] means half of the frames will show frame[2]
        then the other half will show frame[1]. [1, 0] is analogous.
        This default animation will cause the object to take each step
        with a leg, provided 0 and 2 are frames of it walking with
        opposite legs and 1 is a frame of it standing.
        
        The frame number, important to slice correctly the image file
        into object images, is determined automatically by looking at the
        highest number in the animation map. If there are frames beyond
        that number, that is, not all of them are used, *frame_number*
        should be passed.
        """
        # Calculate frame count
        if frame_number is None:
            self.frame_number = max([max(i) for i in basic_animation]) + 1
        else:
            self.frame_number = frame_number

        # Load file
        file_surface = pygame.image.load(filename)

        object_chunk_width = self.frame_number * graphics_config.object_width
        object_chunk_height = 4 * graphics_config.object_height
        chunks_per_line = file_surface.get_width() / object_chunk_width

        x = index % chunks_per_line
        y = index / chunks_per_line

        #FIXME: this is unreadable!
        Image.__init__(self, file_surface.subsurface((x * object_chunk_width,
                                                      y * object_chunk_height),
                                                     (object_chunk_width,
                                                      object_chunk_height)))

        # Create a sprite matrix [facing x frame]
        self.frames = []
        for facing in [UP, RIGHT, DOWN, LEFT]:
            y = ObjectImage.DIRECTION_TO_INDEX_MAP[facing]
            phases = []
            self.frames.append(phases)
            for x in range(self.frame_number):
                width = x * graphics_config.object_width
                height = y * graphics_config.object_height
                rect = pygame.Rect((width, height),
                                   graphics_config.object_dimensions)
                phases.append(self.surface.subsurface(rect))

        self.width = graphics_config.object_width
        self.height = graphics_config.object_height

        # Build animation maps
        self.basic_animation = basic_animation
        self.animation_maps = [(dict((speed, [animation[(phase*len(animation))/\
                                                        speed] for phase in\
                                              range(speed)]) for speed in\
                                     SPEEDS)) for animation in basic_animation]
        self.current_animation = 0
        self.last_observed_movement_phase = 0

    def get_surface(self, obj=None, facing=None, phase=None):
        assert obj is not None or (facing is not None and phase is not None),\
                ('get_surface() must be called with either `obj` or (`facing` '
                 'AND `phase`) parameters set')

        if obj is not None:
            if obj.sliding:
                di = ObjectImage.DIRECTION_TO_INDEX_MAP[obj.facing]
                return self.frames[di][1]
            else:
                self.next_animation(obj)
                di = ObjectImage.DIRECTION_TO_INDEX_MAP[obj.facing]
                am = self.animation_maps[self.current_animation]
                return self.frames[di][am[obj.speed][obj.movement_phase]]
        else:
            di = ObjectImage.DIRECTION_TO_INDEX_MAP[facing]
            am = self.animation_maps[self.current_animation]
            return self.frames[di][am[NORMAL_SPEED][phase]]

    def next_animation(self, obj):
        if obj.movement_phase > self.last_observed_movement_phase:
            self.current_animation = (self.current_animation + 1) %\
                    len(self.basic_animation)
        self.last_observed_movement_phase = obj.movement_phase

