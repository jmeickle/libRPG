import librpg

librpg.init()

librpg.config.graphics_config.config(screen_width=200, screen_height=200, scale=3)

m = librpg.map.MapModel('maptest.map', ('lower_tileset.png', 'lower_tileset.bnd'), [('upper_tileset.png', 'upper_tileset.bnd'), ('upper_tileset.png','upper_tileset.bnd')] )

print m

print 'Terrain layer:'
print m.terrain_layer

print 'Scenario layer:'
print m.scenario_layer

def char_factory(name, char_state):
    return librpg.party.Character('Andy', 'char_alex.png')

world = librpg.world.MicroWorld(m, ['Andy'], char_factory,
                                initial_position=librpg.util.Position(0, 0))

print 'Starting gameloop()'
world.gameloop()
print 'Finished gameloop()'

exit()
