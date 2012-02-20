# Contains the functions needed to load/process maps.

from librpg.util import Matrix, Position
import functools

# Process the addition of monsters or objects.

def obj(arg):
    return (False, functools.partial(arg))

def mon(arg):
    return (True, functools.partial(arg))

class MapLoader:

    def __init__(self):
        self.terrain_data = []
        self.object_data = []
        self.X = 0
        self.Y = 0
        self.scenario = 0
        self.map = None
        self.terrain = None
        self.objects = None

     # Call this to process the map into tuples of terrain info.

    def process_terrain(self):
       for y in (self.map.splitlines()):
           if y:
               self.X = 0
               self.terrain_data.append([])
               for x in y:
                   if x:
                       self.terrain_data[self.Y].append(self.terrain.get(x))
                       self.X += 1
               self.Y += 1

    # Call this to process the map into object functions.
    def process_objects(self, map):
       X = 0
       Y = 0
       for y in (self.map.splitlines()):
           if y:
               X = 0
               self.object_data.append([])
               for x in y:
                   if x:
                       call = self.objects.get(x)
                       if call is not None:
                           print call
                           monster, function = call
                           if call is not None:
                               if monster is False:
                                   object = function(map)
                               else:
                                   object = function(1)
                               map.add_object(object, Position(X, Y))
                       X += 1
               Y += 1

#self.object_data[self.Y].append()
#               self.Y += 1
