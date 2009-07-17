import librpg
import pygame

librpg.init()
librpg.graphics_config.config(tile_size=32, object_height=32, object_width=32)

from librpg.map import MapModel, Map
from librpg.mapobject import MapObject
from librpg.util import Position, Direction
from librpg.party import Character, CharacterReserve
from librpg.image import ObjectImage

class ObjectTestNPC(MapObject):

    def __init__(self):
    
        MapObject.__init__(self, MapObject.OBSTACLE, ObjectImage(pygame.image.load('char_alex32.png')))
        
    def activate(self, party):
    
        print 'Activated NPC'
        
    def collide_with_party(self, party):
    
        print 'Collided NPC'


class ObjectTestChest(MapObject):

    def __init__(self):

        MapObject.__init__(self, MapObject.OBSTACLE, ObjectImage(pygame.image.load('chest.png')))
        self.closed = True
        self.facing = Direction.UP
        
    def activate(self, party):
    
        if self.closed:
            self.closed = False
            print 'Opened chest and added item'
            self.facing = Direction.LEFT
        else:
            print 'Chest is closed'

class ObjectTestMap(MapModel):
    
    def __init__(self):
    
        MapModel.__init__(self, 'objecttest.map', ('lower_tileset32.png', 'lower_tileset32.bnd'), ('upper_tileset32.png', 'upper_tileset32.bnd'))
        
    def initialize(self, local_state):
    
        self.add_object(ObjectTestNPC(), Position(2, 2))
        self.add_object(ObjectTestChest(), Position(8, 4))

a = librpg.party.Character('Andy', 'char_alex32.png')
r = librpg.party.CharacterReserve([a])

model = ObjectTestMap()
model.add_party(r.create_party(3, [a]), Position(0, 0))
Map(model).gameloop()
exit()
