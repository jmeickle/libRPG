from librpg.world import WorldMap
from librpg.mapobject import ScenarioMapObject
from librpg.util import Position

class Teleport(ScenarioMapObject):

    def __init__(self, map, map_id, position):
       
        ScenarioMapObject.__init__(self, map, 0, 0)
        self.target_map_id, self.target_position = map_id, position
        
    def collide_with_party(self, party_avatar, direction):
    
        self.map.schedule_teleport(self.target_map_id, self.target_position)


class Map1(WorldMap):

    def __init__(self):
    
        WorldMap.__init__(self, 'worldtest/map1.map', ('lower_tileset32.png', 'lower_tileset32.bnd'), [('upper_tileset32.png', 'upper_tileset32.bnd'),])

    def initialize(self, local_state):
    
        for y in range(10):
            self.add_object(Teleport(self, 2, Position(1, y)), Position(9, y))


class Map2(WorldMap):

    def __init__(self):
    
        WorldMap.__init__(self, 'worldtest/map2.map', ('lower_tileset32.png', 'lower_tileset32.bnd'), [('upper_tileset32.png', 'upper_tileset32.bnd'),])

    def initialize(self, local_state):
    
        for y in range(10):
            self.add_object(Teleport(self, 1, Position(8, y)), Position(0, y))
            self.add_object(Teleport(self, 3, Position(1, y)), Position(9, y))

class Map3(WorldMap):

    def __init__(self):
    
        WorldMap.__init__(self, 'worldtest/map3.map', ('lower_tileset32.png', 'lower_tileset32.bnd'), [('upper_tileset32.png', 'upper_tileset32.bnd'),])

    def initialize(self, local_state):
    
        for y in range(10):
            self.add_object(Teleport(self, 2, Position(8, y)), Position(0, y))
