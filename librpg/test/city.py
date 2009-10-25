import librpg
from librpg.locals import *


def char_factory(name):
    return librpg.party.Character('Andy',
                                  librpg.path.charset_path('naked_man.png'), 0)


def main():
    librpg.init()

    librpg.config.graphics_config.config(tile_size=32,
                                         object_height=32,
                                         object_width=32)
    camera = librpg.camera.PartyConfinementCameraMode(50, 40)
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
                            (librpg.path.tileset_path('city_lower.png'),
                             librpg.path.tileset_path('city_lower.bnd')),
                            [(librpg.path.tileset_path('city_upper.png'),
                              librpg.path.tileset_path('city_upper.bnd'))])
    m.set_music('park_1.ogg')

    world = librpg.world.MicroWorld(m, char_factory)
    world.initial_state(librpg.util.Position(10, 10), ['Andy'])
    world.gameloop()

    exit()


if __name__ == '__main__':
    main()
