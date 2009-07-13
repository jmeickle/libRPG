from librpg.map import *
from librpg.util import *
from librpg.party import *
from librpg.config import *

import pygame

pygame.init()

GraphicsConfig.TILE_SIZE = 32
GraphicsConfig.OBJECT_HEIGHT = 32
GraphicsConfig.OBJECT_WIDTH = 32

m = Map(MapModel('maptest32.map', ('lower_tileset32.png', 'lower_tileset32.bnd'), ('upper_tileset32.png', 'upper_tileset32.bnd')))

r = CharacterReserve()
a = Character('Andy', 'char_alex32.png')
r.add_char(a)
p = r.create_party(3)
p.add_char(a)

print 'Adding', str(p)
m.map_model.add_party(p, Position(0, 0), Direction.RIGHT, MapObject.NORMAL_SPEED)
print 'Added'
print

print 'Starting gameloop()'
m.gameloop()
print 'Finished gameloop()'

exit()
