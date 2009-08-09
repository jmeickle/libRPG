from librpg.world import World
from librpg.util import Position

from worldtest.mymaps import *

class MyWorld(World):

    def __init__(self):
    
        maps = {1: Map1, 2: Map2, 3: Map3}
        World.__init__(self, maps, 1, Position(5, 4))
        