# Contains the functions needed to load/process maps.

from librpg.util import Matrix

class MapLoader:

    def __init__(self):
        self.data = []
        self.X = 0
        self.Y = 0
        self.scenario = 0
        self.map = None
        self.repl = None

     # Call this to process the map into tuples.

    def process(self):
       for y in (self.map.splitlines()):
           if y:
               self.X = 0
               self.data.append([])
               for x in y:
                   if x:
                       self.X += 1
                       self.data[self.Y].append(self.repl.get(x))
               self.Y += 1
