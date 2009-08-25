from librpg.world import World
from librpg.util import Position
from librpg.party import Character, Party

from worldtest.mymaps import *


def char_factory(name, char_state):
    return Character('Andy', 'char_alex32.png')

class MyWorld(World):

    def __init__(self, save_file=None):
        maps = {1: Map1, 2: Map2, 3: Map3}
        World.__init__(self, maps=maps, character_factory=char_factory,
                       initial_map=1, initial_position=Position(5, 4),
                       state_file=save_file)
        if save_file is None:
            self.reserve.add_char('Andy')
            self.party = Party(3, self.reserve, ['Andy'])
            print self.party
