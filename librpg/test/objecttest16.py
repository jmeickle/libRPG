#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librpg
import pygame

from librpg.map import MapModel
from librpg.mapobject import MapObject, ScenarioMapObject
from librpg.util import Position, inverse
from librpg.party import Character, CharacterReserve
from librpg.movement import Slide, Wait, ForcedStep
from librpg.dialog import MessageDialog
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
        self.destroy()


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


class ObjectTestMap(MapModel):

    def __init__(self):
        MapModel.__init__(self, 'objecttest16.map',
                          ('test16_lower_tileset.png',
                           'test16_lower_tileset.bnd'),
                          [('test16_upper_tileset.png',
                            'test16_upper_tileset.bnd')])

    def initialize(self, local_state, global_state):
        index = 0
        for i in range(6, 2, -1):
            for j in range(3, 1, -1):
                self.add_object(ObjectTestNPC(index), Position(i, j))
                index = (index + 1) % 8

        self.add_object(ObjectTestRock(self), Position(7, 2))


def char_factory(name):
    return librpg.party.Character('Andy', 'test16_charset.png', 3)


def main():
    librpg.init()
    librpg.config.graphics_config.config(tile_size=16,
                                         object_height=32,
                                         object_width=24)

    world = librpg.world.MicroWorld(ObjectTestMap(), char_factory)
    world.initial_state(Position(8, 8), ['Andy'])
    world.gameloop()

    exit()

if __name__ == '__main__':
    main()
