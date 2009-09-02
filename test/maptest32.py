import sys

import librpg

librpg.init()

librpg.config.graphics_config.config(tile_size=32, object_height=32, object_width=32)

if len(sys.argv) < 2:
    print 'Pass a number from 1 to 5 for the screen and camera mode.'
    exit()

mode = int(sys.argv[1])
if mode == 1:
    pass
elif mode == 2:
    librpg.config.graphics_config.config(camera_mode=librpg.camera.FixedCameraMode(50, 50), screen_width=480, screen_height=480, scale=1)
elif mode == 3:
    librpg.config.graphics_config.config(camera_mode=librpg.camera.PartyConfinementCameraMode(50, 40), screen_width=400, screen_height=300)
elif mode == 4:
    librpg.config.graphics_config.config(camera_mode=librpg.camera.ScreenConfinementCameraMode(), screen_width=200, screen_height=200, scale=3)
elif mode == 5:
    librpg.config.graphics_config.config(camera_mode=librpg.camera.ScreenConfinementCameraMode(), screen_width=400, screen_height=400)
else:
    print 'Pass a number from 1 to 5 for the screen and camera mode.'
    exit()

m = librpg.map.MapModel('maptest32.map', ('lower_tileset32.png', 'lower_tileset32.bnd'), [('upper_tileset32.png', 'upper_tileset32.bnd')])

def char_factory(name):
    return librpg.party.Character('Andy', 'actor1.png', 0)

print 'Starting gameloop()'
world = librpg.world.MicroWorld(m, char_factory)
world.initial_config(librpg.util.Position(0, 0), ['Andy'])
world.gameloop()
print 'Finished gameloop()'

exit()
