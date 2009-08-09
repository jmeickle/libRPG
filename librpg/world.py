from map import MapModel, Map

class World:

    def __init__(self, initial_map, initial_position):
        
        self.party = None
        self.state = None
        self.scheduled_teleport = (initial_map, initial_position)

    def create_map(self, map_id):
    
        raise NotImplementedError, 'World.create_map() is abstract'

    def schedule_teleport(self, map_id, position):
    
        self.scheduled_teleport = (map_id, position)
        
    def gameloop(self):
    
        while self.scheduled_teleport:
            map_id, position = self.scheduled_teleport
            map_model = self.create_map(map_id)
            map_model.add_party(self.party, position)
            self.scheduled_teleport = None
            Map(map_model).gameloop()


class WorldMap(MapModel):

    def __init__(self, map_file, terrain_tileset_files, scenario_tileset_files_list, world, id):
    
        MapModel.__init__(self, map_file, terrain_tileset_files, scenario_tileset_files_list)
        self.world = world
        self.id = id
    
    def schedule_teleport(self, map_id, position):
    
        self.world.schedule_teleport(map_id, position)
