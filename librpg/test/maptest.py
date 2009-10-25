import librpg


def char_factory(name):
    return librpg.party.Character('Andy', 'test16_charset.png', 0)


def main():
    librpg.init()

    librpg.config.graphics_config.config(screen_width=200,
                                         screen_height=200,
                                         scale=3)

    m = librpg.map.MapModel('maptest.map',
                            ('test16_lower_tileset.png',
                             'test16_lower_tileset.bnd'),
                            [('test16_upper_tileset.png',
                              'test16_upper_tileset.bnd'),
                             ('test16_upper_tileset.png',
                              'test16_upper_tileset.bnd')])

    print m

    print 'Terrain layer:'
    print m.terrain_layer

    print 'Scenario layer:'
    print m.scenario_layer

    world = librpg.world.MicroWorld(m, char_factory)
    world.initial_state(librpg.util.Position(0, 0), ['Andy'])

    print 'Starting gameloop()'
    world.gameloop()
    print 'Finished gameloop()'

    exit()


if __name__ == '__main__':
    main()
