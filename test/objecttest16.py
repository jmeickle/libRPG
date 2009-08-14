#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import librpg
import pygame

librpg.init()
librpg.config.graphics_config.config(tile_size=16, object_height=32, object_width=24)

from librpg.map import MapModel, MapController
from librpg.mapobject import MapObject, ScenarioMapObject
from librpg.util import Position, inverse
from librpg.party import Character, CharacterReserve
from librpg.movement import Slide, Wait, ForcedStep, Face
from librpg.dialog import MessageDialog
from librpg.context import ContextStack, get_context_stack
from librpg.locals import *

class ObjectTestNPC(MapObject):

    def __init__(self, index):
    
        MapObject.__init__(self, MapObject.OBSTACLE, image_file='chara1.png', image_index=index)
        for dir in [LEFT, DOWN, RIGHT, UP]:
            self.movement_behavior.movements.extend([Wait(30), ForcedStep(dir)])

    def activate(self, party_avatar, direction):
    
        print 'GLOMPed NPC'
        self.map.schedule_message(MessageDialog('GLOMP'))
        self.map.remove_object(self)

class ObjectTestRock(ScenarioMapObject):

    def __init__(self, map):
    
        ScenarioMapObject.__init__(self, map, 0, 57)
        
    def collide_with_party(self, party_avatar, direction):
    
        print 'Pushed rock'
        self.schedule_movement(Slide(direction))
        
    def activate(self, party_avatar, direction):

        print 'Grabbed and pulled rock'
        party_avatar.schedule_movement(Slide(inverse(direction)))
        party_avatar.schedule_movement(Face(direction))
        self.schedule_movement(ForcedStep(inverse(direction)))

class ObjectTestMap(MapModel):
    
    def __init__(self):
    
        MapModel.__init__(self, 'objecttest16.map', ('lower_tileset.png', 'lower_tileset.bnd'), [('upper_tileset.png', 'upper_tileset.bnd'),])
        
    def initialize(self, local_state):
    
        index = 0
        for i in range(6, 2, -1):
            for j in range(3, 1, -1):
                self.add_object(ObjectTestNPC(index), Position(i, j))
                index = (index + 1) % 8
                
        self.add_object(ObjectTestRock(self), Position(7, 2))


a = librpg.party.Character('Andy', 'chara1.png', 3)
r = librpg.party.CharacterReserve([a])

librpg.world.MicroWorld(ObjectTestMap(), r.create_party(3, [a]), Position(8, 8)).gameloop()
exit()
