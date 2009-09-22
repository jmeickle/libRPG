import librpg
from librpg.locals import *

librpg.init()

librpg.config.graphics_config.config(tile_size=32,
                                     object_height=32,
                                     object_width=32)
camera = camera_mode=librpg.camera.PartyConfinementCameraMode(50, 40)
librpg.config.graphics_config.config(camera_mode=camera,
                                     screen_width=500,
                                     screen_height=400)
librpg.config.game_config.config(key_up=set([K_w]),
                                 key_left=set([K_a]),
                                 key_down=set([K_s]),
                                 key_right=set([K_d]),
                                 key_action=set([K_e]),
                                 key_cancel=set([K_q]))

m = librpg.map.MapModel('city.map',
                        (librpg.util.data_path('tileset/city_lower.png'),
                         librpg.util.data_path('tileset/city_lower.bnd')),
                        [(librpg.util.data_path('tileset/city_upper.png'),
                          librpg.util.data_path('tileset/city_upper.bnd'))])
m.set_music('park_1.ogg')

def char_factory(name):
    return librpg.party.Character('Andy', librpg.util.data_path('charset/naked_man.png'), 0)

world = librpg.world.MicroWorld(m, char_factory)
world.initial_state(librpg.util.Position(10, 10), ['Andy'])
world.gameloop()

exit()
