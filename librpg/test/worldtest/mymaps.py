from librpg.world import WorldMap
from librpg.mapobject import ScenarioMapObject, MapObject
from librpg.maparea import RectangleArea, MapArea
from librpg.util import Position
from librpg.movement import Face, Wait
from librpg.dialog import MessageDialog
from librpg.locals import *
from librpg.path import *
from librpg.collection.maparea import RelativeTeleportArea

SAVE_FILE = 'save'
LOWER_TILESET = (tileset_path('city_lower.png'),
                 tileset_path('city_lower.bnd'))
UPPER_TILESET = [(tileset_path('world_upper.png'),
                  tileset_path('world_upper.bnd'))]

class SavePoint(ScenarioMapObject):

    def __init__(self, map):
        ScenarioMapObject.__init__(self, map, 0, 1)

    def activate(self, party_avatar, direction):
        self.map.schedule_message(MessageDialog('You game will be saved to %s.'
                                  % SAVE_FILE, block_movement=True))
        self.map.save_world(SAVE_FILE)
        self.map.schedule_message(MessageDialog('Game saved.',
                                                block_movement=True))


class Chest(MapObject):

    def __init__(self, closed=True):
        MapObject.__init__(self, MapObject.OBSTACLE,
                           image_file=charset_path('chest.png'),
                           image_index=0,
                           basic_animation=[[0]])
        if closed:
            self.facing = UP
        self.closed = closed

    def activate(self, party_avatar, direction):
        if self.closed:
            self.closed = False
            self.schedule_movement(Face(RIGHT))
            self.schedule_movement(Wait(2))
            self.schedule_movement(Face(DOWN))
            self.schedule_movement(Wait(2))
            self.schedule_movement(Face(LEFT))
            self.map.sync_movement([self])
        else:
            self.schedule_movement(Face(UP))
            self.closed = True


class Map1(WorldMap):

    def __init__(self):
        WorldMap.__init__(self, 'worldtest/map1.map',
                          LOWER_TILESET,
                          UPPER_TILESET)

    def initialize(self, local_state, global_state):
        self.add_area(RelativeTeleportArea(x_offset=-8, map_id=2),
                      RectangleArea((9, 0), (9, 9)))

        if local_state is not None:
            self.chest = Chest(local_state['chest_closed'])
        else:
            self.chest = Chest()
        self.add_object(self.chest, Position(5, 5))

        self.add_object(SavePoint(self), Position(6, 7))

    def save_state(self):
        return {'chest_closed': self.chest.closed}


class AreaAroundWell(MapArea):

    def party_entered(self, party_avatar, position):
        print 'party_entered(%s, %s)' % (party_avatar, position)

    def party_moved(self, party_avatar, left_position, entered_position,
                    from_outside):
        print 'party_moved(%s, %s, %s, %s)' % (party_avatar, left_position,
                                               entered_position, from_outside)

    def party_left(self, party_avatar, position):
        print 'party_left(%s, %s)' % (party_avatar, position)


class Map2(WorldMap):

    def __init__(self):
        WorldMap.__init__(self, 'worldtest/map2.map',
                          LOWER_TILESET,
                          UPPER_TILESET)

    def initialize(self, local_state, global_state):
        self.add_area(RelativeTeleportArea(x_offset=+8, map_id=1),
                      RectangleArea((0, 0), (0, 9)))

        self.add_area(RelativeTeleportArea(x_offset=-8, map_id=3),
                      RectangleArea((9, 0), (9, 9)))

        if local_state is not None:
            self.chest = Chest(local_state['chest_closed'])
        else:
            self.chest = Chest()
        self.add_object(self.chest, Position(5, 5))

        self.add_object(SavePoint(self), Position(3, 4))
        self.add_area(AreaAroundWell(), RectangleArea((2, 3), (4, 5)))

    def save_state(self):
        return {'chest_closed': self.chest.closed}


class GameOverBarrel(ScenarioMapObject):

    def __init__(self, map):
        ScenarioMapObject.__init__(self, map, 0, 4)

    def activate(self, party_avatar, direction):
        print 'The barrel explodes and you die.'
        self.map.gameover()


class Map3(WorldMap):

    def __init__(self):
        WorldMap.__init__(self, 'worldtest/map3.map',
                          LOWER_TILESET,
                          UPPER_TILESET)

    def initialize(self, local_state, global_state):
        self.add_object(GameOverBarrel(self), Position(6, 4))

        self.add_area(RelativeTeleportArea(x_offset=+8, map_id=2),
                      RectangleArea((0, 0), (0, 9)))

        self.add_area(RelativeTeleportArea(y_offset=+8),
                      RectangleArea((0, 0), (9, 0)))
        self.add_area(RelativeTeleportArea(y_offset=-8),
                      RectangleArea((0, 9), (9, 9)))

    def custom_gameover(self):
        print 'Map3.custom_gameover()'
