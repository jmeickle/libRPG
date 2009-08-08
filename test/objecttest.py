#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from random import choice

import librpg
import pygame

librpg.init()
librpg.config.graphics_config.config(tile_size=32, object_height=32, object_width=32)

from librpg.map import MapModel, Map
from librpg.mapobject import MapObject, ScenarioMapObject
from librpg.util import Position, inverse
from librpg.party import Character, CharacterReserve
from librpg.movement import MovementCycle, Step, ForcedStep, Face, Wait, Slide
from librpg.dialog import MessageDialog
from librpg.locals import *

class ObjectTestNPC(MapObject):

    def __init__(self):
    
        MapObject.__init__(self, MapObject.OBSTACLE, image_file='actor1.png', image_index=7)
        self.movement_behavior.movements.extend([Wait(30), ForcedStep(UP), Wait(30), ForcedStep(DOWN)])
        
    def activate(self, party_avatar, direction):
    
        print 'Activated NPC'
        for i in xrange(2):
            party_avatar.schedule_movement(Step(inverse(direction)))
        party_avatar.schedule_movement(Face(direction))
        self.map.schedule_message(MessageDialog(u"Ouch!"))
        self.map.schedule_message(MessageDialog(u"Hey, why are you hitting me?!"))


class ObjectTestRock(ScenarioMapObject):

    def __init__(self, map):
    
        ScenarioMapObject.__init__(self, map, 0, 3)
        
    def activate(self, party_avatar, direction):
    
        print 'Activated rock'
        for i in xrange(3):
            self.schedule_movement(Step(direction))
        self.schedule_movement(Face(inverse(direction)))
        
    def collide_with_party(self, party_avatar, direction):
    
        print 'Collided rock'
        self.schedule_movement(Slide(direction))


class ObjectTestChest(MapObject):

    def __init__(self):

        MapObject.__init__(self, MapObject.OBSTACLE, image_file='chest2.png', image_index=5)
        self.closed = True
        self.filled = True
        self.facing = UP
        
    def activate(self, party_avatar, direction):
    
        if self.closed:
            self.closed = False
            self.schedule_movement(Face(RIGHT))
            self.schedule_movement(Wait(2))
            self.schedule_movement(Face(DOWN))
            self.schedule_movement(Wait(2))
            self.schedule_movement(Face(LEFT))
            if self.filled:
                print 'Opened chest and added item'
                self.map.schedule_message(MessageDialog(u"You got Hookshot!"))
                self.filled = False
            else:
                print 'Opened chest but it was empty'
                self.map.schedule_message(MessageDialog(u"The chest is empty =("))
                
        else:
            print 'Chest is open, closing'
            self.schedule_movement(Face(UP))
            self.closed = True


class ObjectTestTowerUpper(ScenarioMapObject):

    def __init__(self, map):

        ScenarioMapObject.__init__(self, map, 0, 4)
        
    def activate(self, party_avatar, direction):
        
        print 'Activated upper tower object'
        
    def collide_with_party(self, party_avatar, direction):
    
        print 'Collided upper tower object'


class ObjectTestTowerLower(ScenarioMapObject):

    RANDOM_TEXTS = ['Life is 10 percent what you make it, and 90 percent how you take it. - Irving Berlin',
                    'My imagination can picture no fairer happiness than to continue living for art. - Clara Schumann',
                    'I used to jog but the ice cubes kept falling out of my glass. - David Lee Roth',
                    'One does not fall in love; one grows into love, and love grows in him. - Karl A. Menninger',
                    'Mother Nature is not sweet. - John Shelby Spong',
                    'All major religious traditions carry basically the same message, that is love, compassion and forgiveness the important thing is they should be part of our daily lives. - Dalai Lama ',
                    'A good compromise, a good piece of legislation, is like a good sentence; or a good piece of music. Everybody can recognize it. They say, \'Huh. It works. It makes sense.\' - Barack Obama',
                    'We can\'t solve problems by using the same kind of thinking we used when we created them. - Albert Einstein',
                    'When I am getting ready to reason with a man, I spend one-third of my time thinking about myself and what I am going to say and two-thirds about him and what he is going to say. - Abraham Lincoln']

    def __init__(self, map):

        ScenarioMapObject.__init__(self, map, 0, 8)
        
    def activate(self, party_avatar, direction):
        
        print 'Activated lower tower object'
        self.map.schedule_message(MessageDialog(choice(ObjectTestTowerLower.RANDOM_TEXTS)))
        
    def collide_with_party(self, party_avatar, direction):
    
        print 'Collided lower tower object'


class ObjectTestCity(ScenarioMapObject):

    def __init__(self, map):

        ScenarioMapObject.__init__(self, map, 0, 13)
        
    def activate(self, party_avatar, direction):
        
        print 'Activated city object'
        
    def collide_with_party(self, party_avatar, direction):
    
        print 'Collided city object'


class ObjectTestMap(MapModel):
    
    def __init__(self):
    
        MapModel.__init__(self, 'objecttest.map', ('lower_tileset32.png', 'lower_tileset32.bnd'), [('upper_tileset32.png', 'upper_tileset32.bnd'),])
        
    def initialize(self, local_state):
    
        self.add_object(ObjectTestNPC(), Position(2, 2))
        self.add_object(ObjectTestChest(), Position(8, 4))
        self.add_object(ObjectTestRock(self), Position(7, 2))
        self.add_object(ObjectTestTowerUpper(self), Position(6, 0))
        self.add_object(ObjectTestTowerLower(self), Position(6, 1))
        self.add_object(ObjectTestCity(self), Position(7, 1))


a = librpg.party.Character('Andy', 'char_alex32.png')
r = librpg.party.CharacterReserve([a])

model = ObjectTestMap()
model.add_party(r.create_party(3, [a]), Position(0, 0))
Map(model).gameloop()
exit()
