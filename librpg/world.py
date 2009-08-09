from map import MapModel, MapController
from locals import *

class World:

    def __init__(self, maps, initial_map, initial_position):
        
        self.maps = maps
        self.party = None
        self.state = None
        self.scheduled_teleport = (initial_map, initial_position)

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
            map_id, position = self.scheduled_teleport
            map_model = self.create_map(map_id)
            map_model.add_party(self.party, position, prev_facing)
            map_model.party_movement = prev_party_movement
            self.scheduled_teleport = None
            MapController(map_model).gameloop()
            prev_facing = map_model.party_avatar.facing
            prev_party_movement = map_model.party_movement
            map_model.remove_party()


class WorldMap(MapModel):

    def __init__(self, map_file, terrain_tileset_files, scenario_tileset_files_list):
    
        MapModel.__init__(self, map_file, terrain_tileset_files, scenario_tileset_files_list)
        self.world = None
        self.id = None
    
    def schedule_teleport(self, map_id, position):
    
        self.world.schedule_teleport(map_id, position)
        self.leave()
        