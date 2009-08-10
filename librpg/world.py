from librpg.map import MapModel, MapController
from librpg.state import State
from librpg.locals import *

class World(object):

    def __init__(self, maps, initial_map, initial_position, state_file=None):
        self.maps = maps
        self.party = None
        self.scheduled_teleport = (initial_map, initial_position)
        self.state_file = state_file
        self.state = State(state_file)

    def create_map(self, map_id):
        created_map = self.maps[map_id]()
        created_map.world = self
        created_map.id = map_id
        return created_map

    def schedule_teleport(self, map_id, position):
        self.scheduled_teleport = (map_id, position)

    def gameloop(self):
        prev_facing = DOWN
        prev_party_movement = []

        while self.scheduled_teleport:
            print self.state.locals
        
            # Create new map
            map_id, position = self.scheduled_teleport
            map_model = self.create_map(map_id)

            # Use data that was stored
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
        self.world.save(filename)
