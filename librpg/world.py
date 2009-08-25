"""
The :mod:`world` module is one of the main modules in LibRPG. Worlds are
entry points for LibRPG games, and they describe game's map structure,
so that maps have connections.
"""

import gc

from librpg.map import MapModel, MapController
from librpg.state import State
from librpg.maparea import MapArea
from librpg.util import Position
from librpg.context import ContextStack, get_context_stack
from librpg.party import CharacterReserve, default_party_factory
from librpg.locals import *

class BaseWorld(object):
    """
    *Abstract.*

    Worlds are the starting point for a LibRPG game.
    
    A World contains one or more maps around which the Party will walk
    and act. The BaseWorld is an abstract class, with the functionality
    that is common to all worlds. Instantiate MicroWorld or World to
    run a game.
    """

    def __init__(self, character_factory, party_factory=None, initial_map=None,
                 initial_position=None, state_file=None):
        assert (initial_map is not None and initial_position is not None)\
               or state_file is not None,\
               'BaseWorld.__init__ cannot determine the party\'s starting\
               position'

        self.party = None
        self.state_file = state_file
        self.state = State(state_file)
        self.party_pos = self.state.load_local(PARTY_POSITION_LOCAL_STATE)
        if self.party_pos is None:
            self.party_pos = (initial_map, initial_position, DOWN)

        if party_factory is not None:
            self.reserve = CharacterReserve(character_factory, party_factory)
        else:
            self.reserve = CharacterReserve(character_factory)
        self.reserve._initialize(self.state.locals)
        self.party = self.reserve.get_default_party()

    def save(self, filename):
        self.state.update(self.reserve._save())
        self.state.save(filename)

    def gameloop():
        """
        *Abstract.*
        
        This method will start the game's actual gameloop. From this
        point, LibRPG will have the control flow and will start from the
        initial state or loaded state as initialized in the world's
        constructor.
        """
        raise NotImplementedError, 'BaseWorld.gameloop() is abstract'


class World(BaseWorld):
    """
    A World contains several maps and is used as an entry point to a
    LibRPG game with more than one map, that is, most games.
    """

    def __init__(self, maps, character_factory, party_factory=None,
                 initial_map=None, initial_position=None, state_file=None):
        """
        *Constructor.*
        
        *maps* should be a dict mapping the map ids to the corresponding
        classes, inherited from MapModel. Map ids should be unique (no two
        maps should share the same id) and may be any hashable and immutable
        object, typically strings or integers.
        
        There are two ways of calling this constructor, concerning the
        initial state. If *state_file* is passed, the game will be run 
        from a save that was previously recorded with the World.save()
        method or MapModel.save_world().
        
        If *state_file* is not passed, *initial_map* and *initial_position*
        have to be passed. In this case, the game will be run from the
        beginning, with a brand new save.
        """
        
        BaseWorld.__init__(self, character_factory, party_factory, initial_map,
                           initial_position, state_file)
        self.maps = maps
        self.scheduled_teleport = (self.party_pos[0], self.party_pos[1], ())
        
    def create_map(self, map_id, *args):
        created_map = self.maps[map_id](*args)
        created_map.world = self
        created_map.id = map_id
        return created_map

    def schedule_teleport(self, position, map_id, *args):
        self.scheduled_teleport = (map_id, position, args)

    def gameloop(self):
        assert not self.party.empty(), 'Party is empty'
        prev_facing = None
        prev_party_movement = []

        while self.scheduled_teleport:
            print self.state.locals
        
            # Create new map
            map_id, position, args = self.scheduled_teleport
            map_model = self.create_map(map_id, *args)

            # Use data that was stored
            if prev_facing is None:
                if self.party_pos is not None:
                    prev_facing = self.party_pos[2]
                else:
                    prev_facing = DOWN
            map_model.add_party(self.party, position, prev_facing)
            map_model.party_movement = prev_party_movement
            local_state = self.state.load_local(map_id)

            # Transfer control to map
            self.scheduled_teleport = None
            get_context_stack().stack_context(MapController(map_model,
                                                            local_state,
                                                            self.state))
            get_context_stack().gameloop()

            # Store data that we wish to carry
            local_state = map_model.save()
            self.state.save_local(map_id, local_state)
            prev_facing = map_model.party_avatar.facing
            prev_party_movement = map_model.party_movement
            map_model.remove_party()
            
            gc.collect()


class MicroWorld(BaseWorld):

    """
    A MicroWorld is a world consisting in only one map. It is used
    for tiny games, tests or examples that don't want to spend the time
    defining a full World.
    """

    TEH_MAP_ID = 42
    PARTY_SIZE = 3

    def __init__(self, map, party_members, character_factory,
                 party_factory=default_party_factory,
                 initial_position=None, state_file=None):
        """
        *Constructor.*
        
        *map* should be an instantiated map inherited from MapModel,
        which will run as the single map in the world.
        
        There are two ways of calling this constructor, concerning the
        initial state. If *state_file* is passed, the game will be run 
        from a save that was previously recorded with the World.save()
        method or MapModel.save_world().
        
        If *state_file* is not passed, *initial_position* has to be passed.
        In this case, the game will be run from the beginning, with a brand
        new save.
        """

        BaseWorld.__init__(self, character_factory, party_factory,
                           MicroWorld.TEH_MAP_ID, initial_position,
                           state_file)
        self.only_map = map
        for char in party_members:
            self.reserve.add_char(char)
        self.party = party_factory(MicroWorld.PARTY_SIZE,
                                   self.reserve,
                                   party_members,
                                   party_members[0])
        print 'self.party =', self.party

    def gameloop(self):
        # Create new map
        map_id, position, facing = self.party_pos
        assert map_id == MicroWorld.TEH_MAP_ID, \
               'The loaded map id is not TEH map id.'

        # Use data that was stored
        self.only_map.add_party(self.party, position, facing)
        local_state = self.state.load_local(map_id)

        # Transfer control to map
        get_context_stack().stack_context(MapController(self.only_map,
                                                        local_state,
                                                        self.state))
        get_context_stack().gameloop()

        # Store data that we wish to carry
        local_state = self.only_map.save()
        self.state.save_local(map_id, local_state)
        self.only_map.remove_party()


class WorldMap(MapModel):
    """
    A WorldMap is merely a MapModel that belongs to a World (the world
    that contains multiple maps). 
    """

    def __init__(self, map_file, terrain_tileset_files,
                 scenario_tileset_files_list):
        """
        *Constructor.*
        
        A WorldMap's constructor does not differ from the base MapModel's,
        but it generally should not be called, except for by
        World.create_map().

        :attr:`id`
            Map id that represents that WorldMap to the World.

        :attr:`world`
            World to which the WorldMap to the WorldMap belongs.
        """
        MapModel.__init__(self, map_file, terrain_tileset_files,
                          scenario_tileset_files_list)
        self.world = None
        self.id = None

    def schedule_teleport(self, position, map_id=None, *map_args):
        """
        After the current iteration of the WorldMap's context stack, the
        party will be teleported to the WorldMap represented by *map_id*
        at *position*.
        
        This method may also be used to teleport to another place in the
        same map, by passing None. If the map id of the current map is
        passed, the party will be removed and added to the map, causing
        the state to be saved and the map to be reinitialized as if it
        were just entered.
        
        If the target map takes arguments for creation, pass them as
        *map_args*.
        """
        if map_id is not None:
            self.world.schedule_teleport(position, map_id, *map_args)
            self.controller.stop()
        else:
            self.teleport_object(self.party_avatar, position)


class TeleportArea(MapArea):
    """
    A TeleportArea is a MapArea that, when entered, will teleport the
    Party to *position* at the WorldMap with *map_id*.
    
    If *map_id* is not passed, the teleport will be internal to the map,
    preventing it from being reinitialized.
            
    If the target map takes arguments for creation, pass them as
    *map_args*.
    """

    def __init__(self, position, map_id=None, *map_args):
        MapArea.__init__(self)
        self.map_id = map_id
        self.position = position
        self.map_args = map_args

    def party_entered(self, party_avatar, position):
        party_avatar.map.schedule_teleport(self.position, self.map_id,
                                           *self.map_args)


class RelativeTeleportArea(MapArea):
    """
    A TeleportArea is a MapArea that, when entered, will teleport the
    Party to the WorldMap with *map_id*, to a position that is relative
    to party's current position in the current map.
    
    The position where the party will "land" is (cur_x + *x_offset*, 
    cur_y + *y_offset*), where (cur_x, cur_y) is the party's current
    position.
    
    This class is useful to create boundaries between maps, allowing the
    "landing" position to be consistent with the "leaving" position.
    
    If *map_id* is not passed, the teleport will be internal to the map,
    preventing it from being reinitialized.
    
    If the target map takes arguments for creation, pass them as
    *map_args*.
    """

    def __init__(self, x_offset=0, y_offset=0, map_id=None, *map_args):
        MapArea.__init__(self)
        self.map_id = map_id
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.map_args = map_args

    def party_entered(self, party_avatar, position):
        position = Position(position.x + self.x_offset,
                            position.y + self.y_offset)
        party_avatar.map.schedule_teleport(position,
                                           self.map_id,
                                           *self.map_args)
