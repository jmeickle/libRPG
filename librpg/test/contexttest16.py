import librpg
import pygame

from librpg.map import MapModel
from librpg.mapobject import MapObject, ScenarioMapObject
from librpg.util import Position, inverse
from librpg.party import Character, CharacterReserve
from librpg.movement import Slide, Wait, ForcedStep, Face
from librpg.dialog import MessageDialog
from librpg.config import dialog_config, game_config
from librpg.context import Context
from librpg.virtualscreen import get_screen
from librpg.locals import *


class ObjectTestNPC(MapObject):

    def __init__(self, index):
        MapObject.__init__(self, MapObject.OBSTACLE,
                           image_file='test16_charset.png', image_index=index)
        for dir in [LEFT, DOWN, RIGHT, UP]:
            self.movement_behavior.movements.extend([Wait(30),
                                                     ForcedStep(dir)])

    def activate(self, party_avatar, direction):
        print 'GLOMPed NPC'
        self.map.schedule_message(MessageDialog('GLOMP'))
        self.map.remove_object(self)


class ObjectTestRock(ScenarioMapObject):

    def __init__(self, map):
        ScenarioMapObject.__init__(self, map, 0, 11)

    def collide_with_party(self, party_avatar, direction):
        if not self.scheduled_movement:
            print 'Pushed rock'
            self.schedule_movement(Slide(direction))

    def activate(self, party_avatar, direction):
        if not self.scheduled_movement:
            print 'Grabbed and pulled rock'
            pulling_direction = inverse(direction)
            party_avatar.schedule_movement(Slide(pulling_direction, back=True),
                                           override=True)
            self.schedule_movement(Slide(pulling_direction), override=True)


class CounterContext(Context):

    def __init__(self, map):
        Context.__init__(self, map)
        self.map = map
        self.amount = 0
        self.font = pygame.font.SysFont(dialog_config.font_name,
                                        dialog_config.font_size)

    def update(self):
        self.amount = len(self.map.objects)
        self.party_pos = self.map.party_avatar.position
        return False

    def draw(self):
        surface = self.font.render("Object#: %d" % (self.amount), True,
                                   dialog_config.font_color)
        get_screen().blit(surface, (20, 20))

        surface = self.font.render("Party: (%d, %d)" % (self.party_pos.x,
                                                        self.party_pos.y),
                                   True,
                                   dialog_config.font_color)
        get_screen().blit(surface, (20, 40))


class ObjectTestMap(MapModel):

    def __init__(self):
        MapModel.__init__(self, 'objecttest16.map',
                          ('test16_lower_tileset.png',
                           'test16_lower_tileset.bnd'),
                          [('test16_upper_tileset.png',
                            'test16_upper_tileset.bnd'), ])

    def initialize(self, local_state, global_state):
        # Add yummy NPCs
        index = 0
        for i in range(6, 2, -1):
            for j in range(3, 1, -1):
                self.add_object(ObjectTestNPC(index), Position(i, j))
                index = (index + 1) % 8

        # Add rock
        self.add_object(ObjectTestRock(self), Position(7, 2))

        # Add counter
        self.object_counter = CounterContext(self)
        self.add_context(self.object_counter)


def char_factory(name):
    return librpg.party.Character('Andy', 'test16_charset.png', 3)


def main():
    librpg.init()
    librpg.config.graphics_config.config(tile_size=16,
                                         object_height=32,
                                         object_width=24)

    game_config.config(fps=40)
    world = librpg.world.MicroWorld(ObjectTestMap(), char_factory)
    world.initial_state(Position(8, 8), ['Andy'])
    world.gameloop()

    exit()

if __name__ == '__main__':
    main()
