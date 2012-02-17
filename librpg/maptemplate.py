# Skeleton map file. Copy it to make new maps!
# After an import, load a map with:
#
#        MapVar = MapClassName()
#        MapLoader.process(MapVar)

from librpg.maploader import MapLoader

class MapTemplate(MapLoader):

    def __init__(self):
        MapLoader.__init__(self)

        # Number of scenario layers (minimum 1).

        self.scenario = 1

        # Set of glyphs that compose the map, which will be redefined.
        # Must be a rectangle! Bad things will happen otherwise.

        self.map ='''
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaazzaaaaaaaaaaaaaaaaaazaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaazzaaaaaaaaaqqqaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaazzzzzzaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaazzzaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaazaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaazaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaqqqaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaazaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
'''
        # You need a sprite index for the terrain layer and one for each
        # scenario layer. For example, if you have 3 scenarios:
        #
        #     'a' : {5, 3, 5, 2}

        self.repl = {
            'a' : (9, 112),
            'q' : (9, 112),
            'z' : (9, 112),
        }
