from librpg.world import WorldMap
from librpg.mapobject import ScenarioMapObject, MapObject
from librpg.util import Position
from librpg.movement import Face, Wait
from librpg.dialog import MessageDialog
from librpg.locals import *

SAVE_FILE = 'save.sav'

class Teleport(ScenarioMapObject):

    def __init__(self, map, map_id, position):
       
        ScenarioMapObject.__init__(self, map, 0, 0)
        self.target_map_id = map_id
        self.target_position = position
        
    def collide_with_party(self, party_avatar, direction):
    
        self.map.schedule_teleport(self.target_map_id, self.target_position)


class SavePoint(ScenarioMapObject):

    def __init__(self, map):
       
        ScenarioMapObject.__init__(self, map, 0, 7)

    def activate(self, party_avatar, direction):
    
        self.map.schedule_message(MessageDialog('You game will be saved to %s.'
                                  % SAVE_FILE, block_movement=True))
        self.map.save_world(SAVE_FILE)
        self.map.schedule_message(MessageDialog('Game saved.',
                                                block_movement=True))


class Chest(MapObject):

    def __init__(self, closed=True):

        MapObject.__init__(self, MapObject.OBSTACLE, image_file='chest2.png',
                           image_index=6)
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
                          ('lower_tileset32.png', 'lower_tileset32.bnd'),
                          [('upper_tileset32.png', 'upper_tileset32.bnd'),])

    def initialize(self, local_state):
    
        for y in range(10):
            self.add_object(Teleport(self, 2, Position(1, y)), Position(9, y))

        if local_state is not None:
            self.chest = Chest(local_state['chest_closed'])
        else:
            self.chest = Chest()
        self.add_object(self.chest, Position(5, 5))

        self.add_object(SavePoint(self), Position(6, 7))

    def save(self):
    
        return {'chest_closed': self.chest.closed}


class Map2(WorldMap):

    def __init__(self):
    
        WorldMap.__init__(self, 'worldtest/map2.map',
                          ('lower_tileset32.png', 'lower_tileset32.bnd'),
                          [('upper_tileset32.png', 'upper_tileset32.bnd'),])

    def initialize(self, local_state):
    
        for y in range(10):
            self.add_object(Teleport(self, 1, Position(8, y)), Position(0, y))
            self.add_object(Teleport(self, 3, Position(1, y)), Position(9, y))

        if local_state is not None:
            self.chest = Chest(local_state['chest_closed'])
        else:
            self.chest = Chest()
        self.add_object(self.chest, Position(5, 5))

        self.add_object(SavePoint(self), Position(3, 4))

    def save(self):

        return {'chest_closed': self.chest.closed}


class Map3(WorldMap):

    def __init__(self):
    
        WorldMap.__init__(self, 'worldtest/map3.map',
                          ('lower_tileset32.png', 'lower_tileset32.bnd'),
                          [('upper_tileset32.png', 'upper_tileset32.bnd'),])

    def initialize(self, local_state):
    
        for y in range(10):
            self.add_object(Teleport(self, 2, Position(8, y)), Position(0, y))
