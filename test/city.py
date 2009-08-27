import librpg

librpg.init()

librpg.config.graphics_config.config(tile_size=32, object_height=32, object_width=32)
librpg.config.graphics_config.config(camera_mode=librpg.camera.PartyConfinementCameraMode(50, 40), screen_width=500, screen_height=400)

m = librpg.map.MapModel('city.map', ('city32.png', 'city32.bnd'), [('city_upper32.png', 'city_upper32.bnd')])

def char_factory(name, char_state):
    return librpg.party.Character('Andy', 'actor1.png', 0)

world = librpg.world.MicroWorld(m, char_factory)
world.initial_config(librpg.util.Position(10, 10), ['Andy'])
world.gameloop()

exit()
