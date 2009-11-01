#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import choice, randint

import librpg
import pygame

from librpg.map import MapModel
from librpg.mapobject import MapObject, ScenarioMapObject
from librpg.world import MicroWorld
from librpg.util import Position, inverse
from librpg.party import Character, CharacterReserve
from librpg.movement import Step, ForcedStep, Face, Wait, Slide, PathMovement
from librpg.dialog import (MessageDialog, ChoiceDialog, MultiMessageDialog,
                           ElasticMessageDialog)
from librpg.sound import play_sfx
from librpg.image import ObjectImage
from librpg.locals import *
from librpg.path import *


class ObjectTestNPC(MapObject):

    def __init__(self):
        MapObject.__init__(self, MapObject.OBSTACLE,
                           image_file='man_undies.png')
        self.movement_behavior.movements.extend([Wait(30), ForcedStep(UP),
                                                 Wait(30), ForcedStep(DOWN)])

    def activate(self, party_avatar, direction):
        print 'Activated NPC'
        for i in xrange(2):
            step = Step(inverse(direction), back=True)
            party_avatar.schedule_movement(step)

        dialog = MessageDialog(u"Ouch!", block_movement=False)
        self.map.schedule_message(dialog)

        dialog = MessageDialog(u"Hey, why are you hitting me?",
                               block_movement=False)
        self.map.schedule_message(dialog)

        def on_choice(user_data, choice):
            map = user_data
            map.schedule_message(MessageDialog('Chose %d' % (choice + 1)))
        dialog = ChoiceDialog(u"Choose NOW:",
                              ["Choice 1", "Choice 2", "Choice 3", "Choice 4"],
                              user_data=self.map,
                              completion_callback=on_choice,
                              block_movement=False)
        self.map.schedule_message(dialog)

        movement = PathMovement(self.map, party_avatar, Position(9, 4))
        party_avatar.schedule_movement(movement)


class ObjectTestRock(ScenarioMapObject):

    def __init__(self, map):
        ScenarioMapObject.__init__(self, map, 0, 5)

    def activate(self, party_avatar, direction):
        print 'Activated rock'
        for i in xrange(3):
            self.schedule_movement(Step(direction))
        self.schedule_movement(Face(inverse(direction)))

    def collide_with_party(self, party_avatar, direction):
        if not self.scheduled_movement:
            print 'Collided rock'
            self.schedule_movement(Slide(direction))


class ObjectTestChest(MapObject):

    def __init__(self):
        MapObject.__init__(self, MapObject.OBSTACLE,
                           image_file=charset_path('chest.png'),
                           image_index=0, facing=UP,
                           basic_animation=[[0]])
        self.closed = True
        self.filled = True
        self.shapeshift = 0

    def activate(self, party_avatar, direction):
        play_sfx('sound6.wav')
        if self.closed:
            self.closed = False
            self.schedule_movement(Face(RIGHT))
            self.schedule_movement(Wait(2))
            self.schedule_movement(Face(DOWN))
            self.schedule_movement(Wait(2))
            self.schedule_movement(Face(LEFT))
            self.map.sync_movement([self])
            if self.filled:
                print 'Opened chest and added item'
                self.map.schedule_message(MessageDialog(u"You got Hookshot!"))
                self.filled = False
            else:
                print 'Opened chest but it was empty'
                self.map.schedule_message(MessageDialog(u"The chest is empty\
                                                        =("))
        else:
            print 'Chest is open, closing'
            self.schedule_movement(Face(UP))
            self.closed = True

    def update(self):
        self.shapeshift += 1
        if self.shapeshift > 40:
            self.image = ObjectImage(charset_path('chest.png'),
                                     randint(0, 1), [[0]])
            self.shapeshift = 0


class ObjectTestTowerUpper(ScenarioMapObject):

    def __init__(self, map):
        ScenarioMapObject.__init__(self, map, 0, 12)

    def activate(self, party_avatar, direction):
        print 'Activated upper tower object'

    def collide_with_party(self, party_avatar, direction):
        print 'Collided upper tower object'


class ObjectTestTowerLower(ScenarioMapObject):

    RANDOM_TEXTS = ['Life is 10 percent what you make it, and 90 percent how\
                    you take it. - Irving Berlin',
                    'My imagination can picture no fairer happiness than to\
                    continue living for art. - Clara Schumann',
                    'I used to jog but the ice cubes kept falling out of my\
                    glass. - David Lee Roth',
                    'One does not fall in love; one grows into love, and love\
                    grows in him. - Karl A. Menninger',
                    'Mother Nature is not sweet. - John Shelby Spong',
                    'All major religious traditions carry basically the same\
                    message, that is love, compassion and forgiveness the\
                    important thing is they should be part of our daily lives.\
                    - Dalai Lama ',
                    'A good compromise, a good piece of legislation, is like a\
                    good sentence; or a good piece of music. Everybody can\
                    recognize it. They say, \'Huh. It works. It makes sense.\'\
                    - Barack Obama',
                    'We can\'t solve problems by using the same kind of\
                    thinking we used when we created them. - Albert Einstein',
                    'When I am getting ready to reason with a man, I spend\
                    one-third of my time thinking about myself and what I am\
                    going to say and two-thirds about him and what he is going\
                    to say. - Abraham Lincoln']

    def __init__(self, map):
        ScenarioMapObject.__init__(self, map, 0, 22)

    def activate(self, party_avatar, direction):
        print 'Activated lower tower object'
        text = choice(ObjectTestTowerLower.RANDOM_TEXTS)
        self.map.schedule_message(ElasticMessageDialog(text))

    def collide_with_party(self, party_avatar, direction):
        print 'Collided lower tower object'


class ObjectTestCity(ScenarioMapObject):

    TEXT = 'Python is an easy to learn, powerful programming language. It '\
           'has efficient high-level data structures and a simple but '\
           'effective approach to object-oriented programming. Python\'s '\
           'elegant syntax and dynamic typing, together with its interpreted '\
           'nature, make it an ideal language for scripting and rapid '\
           'application development in many areas on most platforms. '\
           'The Python interpreter and the extensive standard library are '\
           'freely available in source or binary form for all major '\
           'platforms from the Python Web site, http://www.python.org/, and '\
           'may be freely distributed. The same site also contains '\
           'distributions of and pointers to many free third party Python '\
           'modules, programs and tools, and additional documentation. '\
           'The Python interpreter is easily extended with new functions and '\
           'data types implemented in C or C++ (or other languages callable '\
           'from C). Python is also suitable as an extension language for '\
           'customizable applications. '\
           'This tutorial introduces the reader informally to the basic '\
           'concepts and features of the Python language and system. It '\
           'helps to have a Python interpreter handy for hands-on '\
           'experience, but all examples are self-contained, so the tutorial '\
           'can be read off-line as well. '\
           'For a description of standard objects and modules, see the '\
           'Python Library Reference document. The Python Reference Manual '\
           'gives a more formal definition of the language. To write '\
           'extensions in C or C++, read Extending and Embedding the Python '\
           'Interpreter and Python/C API Reference. There are also several '\
           'books covering Python in depth. '\
           'This tutorial does not attempt to be comprehensive and cover '\
           'every single feature, or even every commonly used feature. '\
           'Instead, it introduces many of Python\'s most noteworthy '\
           'features, and will give you a good idea of the language\'s '\
           'flavor and style. '\
           'After reading it, you will be able to read and write Python '\
           'modules and programs, and you will be ready to learn more about '\
           'the various Python library modules described in the Python '\
           'Library Reference.'

    def __init__(self, map):
        ScenarioMapObject.__init__(self, map, 0, 30)

    def activate(self, party_avatar, direction):
        print 'Activated city object'
        self.map.schedule_message(MultiMessageDialog(ObjectTestCity.TEXT))

    def collide_with_party(self, party_avatar, direction):
        print 'Collided city object'


class ObjectTestGameOverBarrel(ScenarioMapObject):

    def __init__(self, map):
        ScenarioMapObject.__init__(self, map, 0, 4)

    def activate(self, party_avatar, direction):
        print 'The barrel explodes and you die.'
        self.map.gameover()


class ObjectTestMap(MapModel):

    def __init__(self):
        map_file = 'objecttest.map'
        lower_tile_image = tileset_path('town2.png')
        lower_bnd_file = tileset_path('town2.bnd')
        upper_tile_image = tileset_path('world_upper.png')
        upper_bnd_file = tileset_path('world_upper.bnd')
        MapModel.__init__(self, 'objecttest.map',
                          (lower_tile_image, lower_bnd_file),
                          [(upper_tile_image, upper_bnd_file), ])

    def initialize(self, local_state, global_state):
        self.add_object(ObjectTestNPC(), Position(2, 2))
        self.add_object(ObjectTestChest(), Position(8, 4))
        self.add_object(ObjectTestRock(self), Position(7, 2))
        self.add_object(ObjectTestTowerUpper(self), Position(6, 0))
        self.add_object(ObjectTestTowerLower(self), Position(6, 1))
        self.add_object(ObjectTestCity(self), Position(7, 1))
        self.add_object(ObjectTestGameOverBarrel(self), Position(9, 9))

    def custom_gameover(self):
        print 'Map says: You probably messed with a barrel. Don\'t.'


def char_factory(name):
    return librpg.party.Character('Andy', charset_path('naked_man.png'))

if __name__ == '__main__':
    librpg.init('Object Test')
    librpg.config.graphics_config.config(tile_size=32, object_height=32,
                                         object_width=32)

    world = MicroWorld(ObjectTestMap(), char_factory)
    world.initial_state(Position(0, 0), ['Andy'])
    world.gameloop()

    exit()
