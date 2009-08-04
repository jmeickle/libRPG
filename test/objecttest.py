#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import librpg
import pygame

librpg.init()
librpg.graphics_config.config(tile_size=32, object_height=32, object_width=32)

from librpg.map import MapModel, Map
from librpg.mapobject import MapObject, ScenarioMapObject
from librpg.util import Position, Direction
from librpg.party import Character, CharacterReserve
from librpg.image import ObjectImage
from librpg.movement import MovementCycle, Step, Face, Wait, Slide
from librpg.dialog import Dialog

class ObjectTestNPC(MapObject):

    def __init__(self):
    
        MapObject.__init__(self, MapObject.OBSTACLE, image_file='char_alex32.png')
        self.movement_behavior.movements.extend([Wait(30), Step(Direction.UP), Wait(30), Step(Direction.DOWN)])
        
    def activate(self, party_avatar, direction):
    
        print 'Activated NPC'
        for i in xrange(2):
            party_avatar.schedule_movement(Step(librpg.util.Direction.INVERSE[direction]))
        party_avatar.schedule_movement(Face(direction))
        party_avatar.schedule_message(Dialog(u"aiai!"))
        party_avatar.schedule_message(Dialog(u"Fala sério tio, tah me batendo pq?!"))
        
class ObjectTestRock(ScenarioMapObject):

    def __init__(self, map):
    
        ScenarioMapObject.__init__(self, map, 0, 3)
        
    def activate(self, party_avatar, direction):
    
        print 'Activated Rock'
        for i in xrange(3):
            self.schedule_movement(Step(direction))
        self.schedule_movement(Face(librpg.util.Direction.INVERSE[direction]))
        
    def collide_with_party(self, party_avatar, direction):
    
        print 'Collided Rock'
        self.schedule_movement(Slide(direction))


class ObjectTestChest(MapObject):

    def __init__(self):

        MapObject.__init__(self, MapObject.OBSTACLE, image_file='chest.png')
        self.closed = True
        self.facing = Direction.UP
        
    def activate(self, party_avatar, direction):
    
        if self.closed:
            self.closed = False
            print 'Opened chest and added item'
            self.schedule_movement(Face(Direction.RIGHT))
            self.schedule_movement(Wait(2))
            self.schedule_movement(Face(Direction.DOWN))
            self.schedule_movement(Wait(2))
            self.schedule_movement(Face(Direction.LEFT))
        else:
            print 'Chest is open, closing'
            self.schedule_movement(Face(Direction.UP))
            self.closed = True


class ObjectTestMap(MapModel):
    
    def __init__(self):
    
        MapModel.__init__(self, 'objecttest.map', ('lower_tileset32.png', 'lower_tileset32.bnd'), [('upper_tileset32.png', 'upper_tileset32.bnd'),])
        
    def initialize(self, local_state):
    
        self.add_object(ObjectTestNPC(), Position(2, 2))
        self.add_object(ObjectTestChest(), Position(8, 4))
        self.add_object(ObjectTestRock(self), Position(7, 2))


a = librpg.party.Character('Andy', 'char_alex32.png')
r = librpg.party.CharacterReserve([a])

model = ObjectTestMap()
model.add_party(r.create_party(3, [a]), Position(0, 0))
Map(model).gameloop()
exit()
