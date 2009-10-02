:mod:`world` -- Game world
==========================

.. automodule:: librpg.world
   :members:
   :show-inheritance:

Usage
-----

A World is necessary for any game that makes full use of LibRPG.

For tiny games than only need one map:
   
    1. Instantiate the MapModel corresponding to that map.
    2. Instantiate a MicroWorld passing that MapModel.
    3. Call MicroWorld.initial_state() passing the starting position and characters.
    4. Call the MicroWorld's gameloop().
   
For games that need more than one map:

    1. Define your WorldMaps, inheriting a class from it for each map.
    2. Instantiate the World. As parameter, pass a dict attributing a unique map id to each WorldMap-inherited class.
    3. Call World.initial_state(), passing the starting map id, the starting position and the characters.
    4. Call the World's gameloop().

After a world's gameloop ends, to quit the program it is good to call exit(). This will terminate pygame gracefully.

Note: to load from a save, in step 3 call load_state() instead, passing the name of the save file.

Examples
--------

A MicroWorld example::

    import librpg

    librpg.init('Boulder Test')
    librpg.config.graphics_config.config(tile_size=32,
                                         object_height=32,
                                         object_width=32,
                                         scale=1.7)

    from librpg.map import MapModel
    from librpg.mapobject import ScenarioMapObject
    from librpg.util import Position
    from librpg.party import Character, CharacterReserve
    from librpg.movement import Slide
    from librpg.world import MicroWorld

    class Boulder(ScenarioMapObject):

        def __init__(self, map):
        
            ScenarioMapObject.__init__(self, map, 0, 3)
            
        def activate(self, party_avatar, direction):
        
            self.schedule_movement(Slide(direction))


    class BoulderMaze(MapModel):
        
        MAZE = [
        [1,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,1,2,0,0,0,0],
        [0,1,1,2,2,1,1,2,1,0],
        [0,1,2,1,1,1,2,1,2,0],
        [0,2,1,1,1,2,1,1,2,0],
        [0,1,2,2,2,1,1,2,1,0],
        [0,2,2,1,1,1,2,2,1,0],
        [0,1,1,1,2,2,1,1,1,0],
        [0,0,0,0,1,1,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1]]

        def __init__(self):
            MapModel.__init__(self, 'bouldertest.map',
                              ('lower_tileset32.png', 'lower_tileset32.bnd'),
                              [('upper_tileset32.png', 'upper_tileset32.bnd')])
            
        def initialize(self, local_state, global_state):
            for y, line in enumerate(BoulderMaze.MAZE):
                for x, cell in enumerate(line):
                    if cell == 2:
                        self.add_object(Boulder(self), Position(x, y))


    def char_factory(name, char_state):
        return Character('Andy', 'char_alex32.png')

    world = MicroWorld(BoulderMaze(), char_factory)
    world.initial_state(Position(4, 9),
                         ['Andy'])
    world.gameloop()
    exit()

A (macro) World example::

    import librpg
    from librpg.world import WorldMap, RelativeTeleportArea
    from librpg.mapobject import ScenarioMapObject, MapObject
    from librpg.maparea import RectangleArea, MapArea
    from librpg.util import Position
    from librpg.movement import Face, Wait
    from librpg.dialog import MessageDialog
    from librpg.world import World
    from librpg.party import Character
    from librpg.locals import *

    librpg.init()

    SAVE_FILE = 'save.sav'

    class SavePoint(ScenarioMapObject):

        def __init__(self, map):
            ScenarioMapObject.__init__(self, map, 0, 7)

        def activate(self, party_avatar, direction):
            self.map.schedule_message(MessageDialog('You game will be saved to %s.'
                                      % SAVE_FILE, block_movement=True))
            self.map.save_world(SAVE_FILE)
            self.map.schedule_message(MessageDialog('Game saved.',
                                                    block_movement=True))


    class Chest(MapObject):

        def __init__(self, closed=True):
            MapObject.__init__(self, MapObject.OBSTACLE, image_file='chest2.png',
                               image_index=6)
            if closed:
                self.facing = UP
            self.closed = closed

        def activate(self, party_avatar, direction):
            if self.closed:
                self.closed = False
                self.schedule_movement(Face(RIGHT))
                self.schedule_movement(Wait(2))
                self.schedule_movement(Face(DOWN))
                self.schedule_movement(Wait(2))
                self.schedule_movement(Face(LEFT))
                self.map.sync_movement([self])
            else:
                self.schedule_movement(Face(UP))
                self.closed = True


    class AreaAroundWell(MapArea):

        def party_entered(self, party_avatar, position):
            print 'party_entered(%s, %s)' % (party_avatar, position)

        def party_moved(self, party_avatar, left_position, entered_position,
                        from_outside):
            print 'party_moved(%s, %s, %s, %s)' % (party_avatar, left_position,
                                                   entered_position, from_outside)

        def party_left(self, party_avatar, position):
            print 'party_left(%s, %s)' % (party_avatar, position)

        
    class Map1(WorldMap):

        def __init__(self):
            WorldMap.__init__(self, 'worldtest/map1.map',
                              ('lower_tileset32.png', 'lower_tileset32.bnd'),
                              [('upper_tileset32.png', 'upper_tileset32.bnd'),])

        def initialize(self, local_state, global_state):
            self.add_area(RelativeTeleportArea(x_offset=-8, map_id=2),
                          RectangleArea((9, 0), (9, 9)))

            if local_state is not None:
                self.chest = Chest(local_state['chest_closed'])
            else:
                self.chest = Chest()
            self.add_object(self.chest, Position(5, 5))

            self.add_object(SavePoint(self), Position(6, 7))

        def save_state(self):
            return {'chest_closed': self.chest.closed}


    class Map2(WorldMap):

        def __init__(self):
            WorldMap.__init__(self, 'worldtest/map2.map',
                              ('lower_tileset32.png', 'lower_tileset32.bnd'),
                              [('upper_tileset32.png', 'upper_tileset32.bnd'),])

        def initialize(self, local_state, global_state):
            self.add_area(RelativeTeleportArea(x_offset=+8, map_id=1),
                          RectangleArea((0, 0), (0, 9)))
                          
            self.add_area(RelativeTeleportArea(x_offset=-8, map_id=3),
                          RectangleArea((9, 0), (9, 9)))

            if local_state is not None:
                self.chest = Chest(local_state['chest_closed'])
            else:
                self.chest = Chest()
            self.add_object(self.chest, Position(5, 5))

            self.add_object(SavePoint(self), Position(3, 4))
            self.add_area(AreaAroundWell(), RectangleArea((2, 3), (4, 5)))

        def save_state(self):
            return {'chest_closed': self.chest.closed}


    class Map3(WorldMap):

        def __init__(self):
            WorldMap.__init__(self, 'worldtest/map3.map',
                              ('lower_tileset32.png', 'lower_tileset32.bnd'),
                              [('upper_tileset32.png', 'upper_tileset32.bnd'),])

        def initialize(self, local_state, global_state):
            self.add_area(RelativeTeleportArea(x_offset=+8, map_id=2),
                          RectangleArea((0, 0), (0, 9)))
                          
            self.add_area(RelativeTeleportArea(y_offset=+8),
                          RectangleArea((0, 0), (9, 0)))
            self.add_area(RelativeTeleportArea(y_offset=-8),
                          RectangleArea((0, 9), (9, 9)))


    def char_factory(name, char_state):
        return Character('Andy', 'char_alex32.png')


    class MyWorld(World):

        def __init__(self, save_file=None):
            maps = {1: Map1, 2: Map2, 3: Map3}
            World.__init__(self, maps=maps, character_factory=char_factory)
            if save_file is None:
                self.initial_state(map=1, position=Position(5, 4), chars=['Andy'])
            else:
                self.load_state(save_file)


    # Config graphics
    librpg.config.graphics_config.config(tile_size=32,
                                         object_height=32,
                                         object_width=32)

    # Create world and run
    try:
        w = MyWorld(SAVE_FILE)
    except IOError:
        w = MyWorld()

    w.gameloop()

    # Terminate
    exit()
