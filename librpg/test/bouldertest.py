import librpg

from librpg.map import MapModel
from librpg.mapobject import ScenarioMapObject
from librpg.util import Position
from librpg.party import Character, CharacterReserve
from librpg.movement import Slide
from librpg.dialog import MessageDialog
from librpg.world import MicroWorld
from librpg.path import *


class Boulder(ScenarioMapObject):

    def __init__(self, map):

        ScenarioMapObject.__init__(self, map, 0, 5)

    def activate(self, party_avatar, direction):

        self.schedule_movement(Slide(direction))


class Victory(ScenarioMapObject):

    def __init__(self, map):

        ScenarioMapObject.__init__(self, map, 0, 0)

    def collide_with_party(self, party_avatar, direction):

        self.map.pause(30)
        self.map.schedule_message(MessageDialog('Gratz! You won!'))


class BoulderMaze(MapModel):

    MAZE = [
    [1, 1, 1, 1, 3, 3, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 2, 0, 0, 0, 0],
    [0, 1, 1, 2, 2, 1, 1, 2, 1, 0],
    [0, 1, 2, 1, 1, 1, 2, 1, 2, 0],
    [0, 2, 1, 1, 1, 2, 1, 1, 2, 0],
    [0, 1, 2, 2, 2, 1, 1, 2, 1, 0],
    [0, 2, 2, 1, 1, 1, 2, 2, 1, 0],
    [0, 1, 1, 1, 2, 2, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    def __init__(self):
        MapModel.__init__(self, 'bouldertest.map',
                          (tileset_path('city_lower.png'),
                           tileset_path('city_lower.bnd')),
                          [(tileset_path('world_upper.png'),
                            tileset_path('world_upper.bnd'))])

    def initialize(self, local_state, global_state):
        for y, line in enumerate(BoulderMaze.MAZE):
            for x, cell in enumerate(line):
                if cell == 2:
                    self.add_object(Boulder(self), Position(x, y))
                elif cell == 3:
                    self.add_object(Victory(self), Position(x, y))


def char_factory(name):
    return librpg.party.Character('Andy', charset_path('naked_man.png'))


def main():
    librpg.init('Boulder Test')
    librpg.config.graphics_config.config(tile_size=32,
                                         object_height=32,
                                         object_width=32,
                                         scale=1.7)

    world = librpg.world.MicroWorld(BoulderMaze(), char_factory)
    world.initial_state(position=Position(4, 9),
                         chars=['Andy'])
    world.gameloop()
    exit()

if __name__ == '__main__':
    main()
