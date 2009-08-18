import librpg

librpg.init()

librpg.config.graphics_config.config(tile_size=32, object_height=32, object_width=32)
librpg.config.graphics_config.config(camera_mode=librpg.camera.PartyConfinementCameraMode(50, 40), screen_width=500, screen_height=400)

m = librpg.map.MapModel('city.map', ('city32.png', 'city32.bnd'), [('city_upper32.png', 'city_upper32.bnd')])

a = librpg.party.Character('Andy', 'actor1.png', 0)
r = librpg.party.CharacterReserve([a])
p = r.create_party(3, [a])

librpg.world.MicroWorld(m, p, librpg.util.Position(10, 10)).gameloop()

exit()
