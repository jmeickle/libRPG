# Contains the functions needed to load/process maps.

from librpg.util import Matrix, Position
import functools

class MapLoader:

    def __init__(self, map):
        # Passed in: the MapModel object we're loading data for.
        self.map = map

        # Redefinable map 'settings'
        self.combat = False
        self.music = None
        self.scenario = 1

        # The ASCII textmap and replacement dictionaries for it.
        self.textmap = None
        self.terrain = None
        self.objects = None
        self.actors = None

        # Calculated when the map is processed, so don't override them.
        self.X = 0
        self.Y = 0
        self.glyphs = []

    # Calculate X/Y and store all glyphs.
    def process_textmap(self):
       for y in (self.textmap.splitlines()):
           if y:
               self.X = 0
               self.glyphs.append([])
               for x in y:
                   if x:
                       self.glyphs[self.Y].append(x)
                       self.X += 1
               self.Y += 1

    # Use appropriate terrain and scenario tiles based on textmap and replacements.
    def process_terrain(self):
        self.map.terrain_layer = Matrix(self.X, self.Y)
        self.map.scenario_layer = [Matrix(self.X, self.Y) for i in range(self.scenario)]

        for y in range(self.Y):
            for x in range(self.X):
                self.map.terrain_layer[x, y] = self.map.terrain_tileset.tiles[self.terrain.get(self.glyphs[y][x])[0]]
                for i in range(self.scenario):
                    self.map.scenario_layer[i][x, y] = self.map.scenario_tileset[i].tiles[self.terrain.get(self.glyphs[y][x])[self.scenario]]

    # Add objects (including NPCs) based on textmap and replacements.
    def process_objects(self):
        for y in range(self.Y):
            for x in range(self.X):
                func_call = self.objects.get(self.glyphs[y][x])
                if func_call is not None:
                    npc, function = func_call
                    if func_call is not None:
                        if npc is False:
                            object = function(self.map)
                        else:
                            object = function(1)
                        self.map.add_object(object, Position(x, y))

    # Stub. This will eventually process the textmap for combat actors and then start a combat.
    def process_actors(self):
        return False

# Helper functions to process the addition of NPCs or objects.
def obj(arg):
    return (False, functools.partial(arg))

def npc(arg):
    return (True, functools.partial(arg))
