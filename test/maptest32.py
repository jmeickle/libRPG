from librpg.map import *
from librpg.util import *
from librpg.party import *
from librpg.config import *
from librpg.camera import *

import pygame

pygame.init()

graphics_config.config(tile_size=32, object_height=32, object_width=32)

#graphics_config.config(camera_mode=FixedCameraMode(0, 0), screen_width=480, screen_height=480)
#graphics_config.config(camera_mode=PartyConfinementCameraMode(40, 50), screen_width=300, screen_height=400)
#graphics_config.config(camera_mode=ScreenConfinementCameraMode(), screen_width=200, screen_height=200)
#graphics_config.config(camera_mode=ScreenConfinementCameraMode(), screen_width=400, screen_height=400)

m = Map(MapModel('maptest32.map', ('lower_tileset32.png', 'lower_tileset32.bnd'), ('upper_tileset32.png', 'upper_tileset32.bnd')))

a = Character('Andy', 'char_alex32.png')
r = CharacterReserve([a])
p = r.create_party(3, [a])

print 'Adding', str(p)
m.map_model.add_party(p, Position(0, 0))
print 'Added'
print

print 'Starting gameloop()'
m.gameloop()
print 'Finished gameloop()'

exit()
