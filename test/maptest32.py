import sys

if len(sys.argv) < 2:
    print 'Pass a number from 1 to 5 for the screen and camera mode.'
    exit()

import librpg
from librpg.map import *
from librpg.util import *
from librpg.party import *
from librpg.camera import *

librpg.init()

librpg.graphics_config.config(tile_size=32, object_height=32, object_width=32)

mode = int(sys.argv[1])
if mode == 1:
    pass
elif mode == 2:
    librpg.graphics_config.config(camera_mode=FixedCameraMode(50, 50), screen_width=480, screen_height=480, scale=1)
elif mode == 3:
    librpg.graphics_config.config(camera_mode=PartyConfinementCameraMode(50, 40), screen_width=400, screen_height=300)
elif mode == 4:
    librpg.graphics_config.config(camera_mode=ScreenConfinementCameraMode(), screen_width=200, screen_height=200, scale=3)
elif mode == 5:
    librpg.graphics_config.config(camera_mode=ScreenConfinementCameraMode(), screen_width=400, screen_height=400)
else:
    print 'Pass a number from 1 to 5 for the screen and camera mode.'
    exit()

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
