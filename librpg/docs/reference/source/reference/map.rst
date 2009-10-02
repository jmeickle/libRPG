:mod:`map` -- Map core
======================

.. automodule:: librpg.map
   :members:
   :show-inheritance:
   
Usage
-----

To use a map, three things must be done:

1) Create a .map file with the layout of that map. Pass this file's name to the MapModel constructor.
2) Define the tileset that will be used for drawing the map's terrain and scenario layers. Pass the image and boundaries files' names to the MapModel constructor.
3) Write a class that inherits from MapModel (for example MyMapModel), overriding only the initialize() method with a routine that places the objects and area of the map to an initial state.

When this is done, create a world and insert that MapModel into it. The way this is done depends on the world created:

- In case of a MicroWorld - which is a world with a single map -, instantiate the MapModel and pass it as parameter to the MicroWorld constructor, along with the Party::

    world = MicroWorld(MyMapModel(), party, Position(1, 2))

- In case of a World - which allows any amount of maps -, first define a unique map_id for that map. Pass it inside the *maps* parameter of the constructor, as a value associated to its map_id as key::

    class MyWorld(World):
        def __init__(self):
            World.__init__(self,
                           maps={1: MyMapModel},
                           initial_map=1,
                           initial_position=Position(1, 2))
    world = MyWorld()
    
Then, with the world created, call its gameloop() method::

    world.gameloop()

To add and remove objects from the map, use add_object() and remove_object(). To add and remove areas, use add_area() and remove_area().

Example
-------

::

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
    from librpg.locals import *

    class ObjectTestNPC(MapObject):

        def __init__(self, index):
        
            MapObject.__init__(self, MapObject.OBSTACLE,
                               image_file='chara1.png', image_index=index)
            for dir in [LEFT, DOWN, RIGHT, UP]:
                self.movement_behavior.movements.extend([Wait(30),
                                                         ForcedStep(dir)])

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
        
            MapModel.__init__(self, 'objecttest16.map',
                              ('lower_tileset.png', 'lower_tileset.bnd'),
                              [('upper_tileset.png', 'upper_tileset.bnd'),])
            
        def initialize(self, local_state):
        
            index = 0
            for i in range(6, 2, -1):
                for j in range(3, 1, -1):
                    self.add_object(ObjectTestNPC(index), Position(i, j))
                    index = (index + 1) % 8
                    
            self.add_object(ObjectTestRock(self), Position(7, 2))


    a = librpg.party.Character('Andy', 'chara1.png', 3)
    r = librpg.party.CharacterReserve([a])

    librpg.world.MicroWorld(ObjectTestMap(),
                            r.create_party(3, [a]), Position(8, 8)).gameloop()
    exit()
