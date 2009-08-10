import librpg
librpg.init()

from worldtest.myworld import MyWorld

# Config graphics
librpg.config.graphics_config.config(tile_size=32, object_height=32, object_width=32)

# Create char and char reserve
a = librpg.party.Character('Andy', 'char_alex32.png')
r = librpg.party.CharacterReserve([a])

# Create world and run
try:
    w = MyWorld('save.sav')
except IOError:
    w = MyWorld()
w.party = r.create_party(3, [a])
w.gameloop()

# Terminate
exit()
