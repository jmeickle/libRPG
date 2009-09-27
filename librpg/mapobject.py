"""
The :mod:`mapobject` module contains the definition of MapObject, which
will provide interaction to your maps. It also contains PartyAvatar,
which is the MapObject controlled by the player that represents the Party
in the map.
"""

import pygame

from librpg.locals import *
from librpg.movement import MovementQueue, MovementCycle
from librpg.image import ObjectImage

class MapObject(object):

    """
    MapObjects represent interactive objects on the map, such as NPCs,
    chests and switches. For it to be interactive, overload its activate()
    or collide_with_party() methods, which will be called as callbacks
    when those events happen.
    """

    BELOW, OBSTACLE, COUNTER, ABOVE = 0, 1, 2, 3

    def __init__(self, obstacle, image=None, facing=DOWN, speed=NORMAL_SPEED,
                 image_file=None, image_index=0,
                 basic_animation=DEFAULT_OBJECT_IMAGE_BASIC_ANIMATION,
                 frame_number=None):
        """
        *Constructor*

        *obstacle* should be one of {BELOW, OBSTACLE, COUNTER, ABOVE}
        indicating the vertical position of the object.

        If *image* or *image_file* are specified, the object will be
        displayed with that image. *image* should be an ObjectImage and
        *image_file* should be the filename of a bitmap with the intended
        image. Only one of them may be specified.

        If *image_file* is specified and the file holds more than one object
        image, *image_index* has to be passed indicating which of them should
        be loaded. Also, *basic_animation* and *frame_number* will customize
        the object's animation in that case.

        *facing* is the object's starting facing, and *speed* is its
        starting speed.

        :attr:`map`
            MapModel in which the object is.

        :attr:`position`
            Position of the object in the map.

        :attr:`obstacle`
            - BELOW if the object can be walked over
            - OBSTACLE if the object will collide if another OBSTACLE object
              tries to move to its tile.
            - ABOVE if OBSTACLES would walk under the object
            - COUNTER if it is an OBSTACLE and activate events coming from one
              side will be routed to the position on the opposite side.
              
        :attr:`facing`
            Direction that the object is facing.
            
        :attr:`speed`
            Object speed, in the number of frames to move that object by 1 tile.
            Use VERY_FAST_SPEED, FAST_SPEED, NORMAL_SPEED, SLOW_SPEED and
            VERY_SLOW_SPEED.

        :attr:`scheduled_movement`
            MovementQueue with the Movements that are waiting for the object to
            execute.

        :attr:`movement_behavior`
            MovementCycle with the Movements routinely executed by the object.
        
        :attr:`areas`
            MapAreas in which the object currently is.
        """
        assert obstacle in range(0, 4), ('MapObject cannot be created with an'
                                         ' `obstacle` as %s' % str(obstacle))
        assert (image is None or image_file is None),\
                'Only one of (image, image_file) can be specified.'

        self.map = None
        self.position = None
        self.prev_positon = None
        self.obstacle = obstacle

        self.movement_phase = 0
        self.facing = facing
        self.speed = speed
        self.scheduled_movement = MovementQueue()
        self.movement_behavior = MovementCycle()
        self.sliding = False
        self.going_back = False
        self.just_completed_movement = False

        self.areas = []
        self.prev_areas = []
        
        if image is not None:
            self.image = image
        elif image_file is not None:
            self.image = ObjectImage(image_file, image_index, basic_animation,
                                     frame_number)

    # Virtual
    def activate(self, party_avatar, direction):
        """
        *Virtual*
        
        Callback called when the player, through a PartyAvatar, activates
        the object. This happens when he presses the action button and
        is in the same tile as the object (for BELOW and ABOVE objects)
        or facing the object (for OBSTACLE and COUNTER objects).
        
        For example, for a chest, this routine will award the party's
        inventory some items, while for an NPC, this routine will trigger
        a message dialog.
        """
        pass

    # Virtual
    def collide_with_party(self, party_avatar, direction):
        """
        *Virtual*
        
        Callback called when the player, through a PartyAvatar, collides
        with the object. This happens when he walks over the object
        (for BELOW and ABOVE objects), when the party tries to move towards
        the object (for OBSTACLE and COUNTER objects).
        """
        pass

    def is_counter(self):
        """
        Return whether the object is a counter - that is, if activate
        events coming from one side affect objects on the opposite side.
        """
        return self.obstacle == MapObject.COUNTER

    def is_obstacle(self):
        """
        Return whether the object is an obstacle.
        """
        return (self.obstacle == MapObject.OBSTACLE or
                self.obstacle == MapObject.COUNTER)

    def is_below(self):
        """
        Return whether the tile is drawn below party level.
        """
        return self.obstacle == MapObject.BELOW

    def is_above(self):
        """
        Return whether the tile is drawn above party level.
        """
        return self.obstacle == MapObject.ABOVE

    def get_surface(self):
        """
        Return a pygame Surface with the image as the object should be
        drawn.
        """
        return self.image.get_surface(self)

    def flow(self):
        just_completed_movement = False

        if self.movement_phase == 1:
            self.just_completed_movement = True

        if self.movement_phase > 0:
            self.movement_phase -= 1
        else:
            no_scheduled_movement = self.scheduled_movement.flow(self)
            if no_scheduled_movement:
                self.movement_behavior.flow(self)

    def schedule_movement(self, movement, override=False):
        """
        Enqueue a Movement for the object to execute after the ones
        already requested.
        
        If *override* is passed as True, this movement will cancel
        whatever other scheduled movements there are already in the
        queue.
        """
        if override:
            self.scheduled_movement.clear()
        
        self.scheduled_movement.append(movement)

    def destroy(self):
        """
        Remove the object from its map, effectively destroying it.
        """
        assert self.map is not None, 'The object must be in a map to be ' \
                                     'destroyed.'
        self.map.remove_object(self)


class PartyAvatar(MapObject):
    """
    PartyAvatar is a MapObject that represents the Party in the map.
    It is controlled by the player input, and triggers the *activate*
    and *collide_with_party* callbacks that usually do the most
    important interactions in the map.
    
    :attr:`party`
        Party represented by the avatar.
    """

    def __init__(self, party, facing=DOWN, speed=NORMAL_SPEED):
        MapObject.__init__(self, MapObject.OBSTACLE, party.get_image(self),
                           facing, speed)
        self.party = party
        party.avatar = self

    def reload_image(self):
        self.image = self.party.get_image(self)


class ScenarioMapObject(MapObject):
    """
    ScenarioMapObject is a MapObject that has its image loaded from the
    scenario layer tileset of the map.
    """

    def __init__(self, map, scenario_number, scenario_index, obstacle=None,
                 facing=DOWN, speed=NORMAL_SPEED):
        """
        *Constructor.*
        
        *map* is the MapModel from which the scenario tile image will be
        taken. *scenario_number* is the number of the scenario layer and
        *scenario_index* is the tile index containing the image.
        
        *obstacle*, *facing* and *speed* are the same as in MapObject.
        """
        tile = map.scenario_tileset[scenario_number].tiles[scenario_index]
        if obstacle is None:
            MapObject.__init__(self, tile.obstacle, tile.image, facing, speed)
        else:
            MapObject.__init__(self, obstacle, tile.image, facing, speed)

