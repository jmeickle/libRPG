from librpg.map import MapModel, MapController
from librpg.state import State
from librpg.maparea import MapArea
from librpg.util import Position
from librpg.locals import *

class World(object):

    def __init__(self, maps, initial_map=None, initial_position=None,
                 state_file=None):
        assert (initial_map is not None and initial_position is not None)\
               or state_file is not None,\
               'World.__init__ cannot determine the party\'s starting position'
        self.maps = maps
        self.party = None
        self.state_file = state_file
        self.state = State(state_file)
        self.party_pos = self.state.load_local(PARTY_POSITION_LOCAL_STATE)
        if self.party_pos is not None:
            self.scheduled_teleport = (self.party_pos[0], self.party_pos[1])
        else:
            self.scheduled_teleport = (initial_map, initial_position)

    def create_map(self, map_id):
        created_map = self.maps[map_id]()
        created_map.world = self
        created_map.id = map_id
        return created_map

    def schedule_teleport(self, map_id, position):
        self.scheduled_teleport = (map_id, position)

    def gameloop(self):
        prev_facing = None
        prev_party_movement = []

        while self.scheduled_teleport:
            print self.state.locals
        
            # Create new map
            map_id, position = self.scheduled_teleport
            map_model = self.create_map(map_id)

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
            MapController(map_model, local_state).gameloop()

            # Store data that we wish to carry
            local_state = map_model.save()
            self.state.save_local(map_id, local_state)
            prev_facing = map_model.party_avatar.facing
            prev_party_movement = map_model.party_movement
            map_model.remove_party()

    def save(self, filename):
        self.state.save(filename)


class WorldMap(MapModel):

    def __init__(self, map_file, terrain_tileset_files,
                 scenario_tileset_files_list):
        MapModel.__init__(self, map_file, terrain_tileset_files,
                          scenario_tileset_files_list)
        self.world = None
        self.id = None

    def schedule_teleport(self, map_id, position):
        self.world.schedule_teleport(map_id, position)
        self.leave()

    def save_world(self, filename):
        self.world.state.save_local(self.id, self.save())
        party_local_state = (self.id, self.party_avatar.position,
                             self.party_avatar.facing)
        self.world.state.save_local(PARTY_POSITION_LOCAL_STATE,
                                    party_local_state)
        self.world.save(filename)


class TeleportArea(MapArea):

    def __init__(self, position, map_id=None):
        MapArea.__init__(self)
        self.map_id = map_id
        self.position = position

    def party_entered(self, party_avatar, position):
        party_avatar.map.schedule_teleport(self.map_id,
                                           self.position)


class RelativeTeleportArea(MapArea):

    def __init__(self, x_offset=0, y_offset=0, map_id=None):
        MapArea.__init__(self)
        self.map_id = map_id
        self.x_offset = x_offset
        self.y_offset = y_offset

    def party_entered(self, party_avatar, position):
        position = Position(position.x + self.x_offset, position.y + self.y_offset)
        party_avatar.map.schedule_teleport(self.map_id,
                                           position)
