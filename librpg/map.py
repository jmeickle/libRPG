import csv

import pygame
from pygame.locals import *

from mapobject import *
from mapview import *
from util import *
from image import *
from tile import *
from config import *

#=================================================================================
    
class Map:

    # Read-Only Attributes:
    # map_view - MapView (View component of MVC)
    # map_model - MapModel (Model component of MVC)
    
    KEY_TO_DIRECTION = {K_DOWN:Direction.DOWN, K_UP:Direction.UP, K_LEFT:Direction.LEFT, K_RIGHT:Direction.RIGHT}
    
    FPS = 30
    
    def __init__(self, map_model, local_state=None):
    
        self.map_model = map_model
        self.map_model.initialize(local_state)
        self.map_view = MapView(self.map_model)
        
    def gameloop(self):
    
        # Locals for optimization
        map_model = self.map_model
        map_view_draw = self.map_view.draw
        party_avatar = map_model.party_avatar
        party_movement = map_model.party_movement
        map_model_try_to_move_object = map_model.try_to_move_object
        self.party_movement_append = party_movement.append
        self.party_movement_remove = party_movement.remove
    
        map_view_draw()
        
        clock = pygame.time.Clock()
        keep_going = True
        while keep_going:
            clock.tick(Map.FPS)
            self.flow_object_movement()
            
            pos = party_avatar.position
            keep_going = self.process_input()
            if party_movement:
                moved = map_model_try_to_move_object(party_avatar, party_movement[0])
                    
            # debug
            if pos != party_avatar.position:
                print map_model
                
            map_view_draw()
            
    def process_input(self):
    
        for event in pygame.event.get():
            # print event
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                direction = Map.KEY_TO_DIRECTION.get(event.key)
                if direction is not None and not direction in self.map_model.party_movement:
                    self.party_movement_append(direction)
                elif event.key == K_ESCAPE:
                    return False
            elif event.type == KEYUP:
                direction = Map.KEY_TO_DIRECTION.get(event.key)
                if direction is not None and direction in self.map_model.party_movement:
                    self.party_movement_remove(direction)
        return True
        
    def flow_object_movement(self):
    
        for o in self.map_model.objects:
            if o.movement_phase > 0:
                o.movement_phase -= 1

#=================================================================================

class MapModel:

    """
    party: Party (read-only)
    Active Party on this Map.

    party_avatar: PartyAvatar (read-only)
    MapObject representation of the active Party.

    party_movement: Direction (private)
    Direction to which the party is currently moving.

    width: int (read-only)
    Map width in tiles.

    height: int (read-only)
    Map height in tiles.

    map_file: string (read-only)
    Name of the file that contains the map layout.

    terrain_tileset_files: (string, string) (read-only)
    Pair of names of the files that contain the terrain tileset image and boundaries.

    scenario_tileset_files: (string, string) (read-only)
    Pair of names of the files that contain the scenario tileset image and boundaries.

    terrain_tileset: TileSet (read-only)
    Tileset to draw terrain layer.

    scenario_tileset: Tileset (read-only)
    Tileset to draw scenario layer.

    terrain_layer: Matrix<Tile> (read-only)
    Matrix with the tiles that compose the terrain layer.

    scenario_layer: Matrix<Tile> (read-only)
    Matrix with the tiles that compose the scenario layer.

    object_layer: Matrix<ObjectCell> (read-only)
    Matrix with the objects that each tile contains.

    area_layer: Matrix<MapArea> (read-only)
    Matrix with the area to which each tile belongs.

    areas: [MapArea] (read-only)
    All areas in the map.

    objects: [MapObject] (read-only)
    All objects in the map.

    local_state: object (read-only)
    Local state to store persistent data about that map. It may be read after the gameloop() is broken.
    """
    
    def __init__(self, map_file, terrain_tileset_files, scenario_tileset_files):
    
        self.party, self.party_avatar, self.party_movement = None, None, []
        
        self.map_file = map_file
        
        self.terrain_tileset_files = terrain_tileset_files
        self.scenario_tileset_files = scenario_tileset_files
        
        self.terrain_tileset = Tileset(self.terrain_tileset_files[0], self.terrain_tileset_files[1])
        self.scenario_tileset = Tileset(self.scenario_tileset_files[0], self.scenario_tileset_files[1])
        
        self.load_from_map_file()
        
        self.local_state = None
        
        self.objects = []
        self.object_layer = Matrix(self.width, self.height)
        object_layer_set = self.object_layer.set
        for x in range(self.width):
            for y in range(self.height):
                object_layer_set(x, y, ObjectCell())

    def load_from_map_file(self):
    
        layout_file = open(self.map_file)
        r = csv.reader(layout_file, delimiter=',')

        first_line = r.next()
        self.width, self.height = int(first_line[0]), int(first_line[1])

        self.terrain_layer = Matrix(self.width, self.height)
        self.scenario_layer = Matrix(self.width, self.height)
        
        y = 0
        for line in r:
            if len(line) == self.width:
                for value, x in zip(line, xrange(self.width)):
                    self.terrain_layer.set(x, y, self.terrain_tileset.tiles[int(value)])
                y += 1
            if y >= self.height:
                break
                
        y = 0
        for line in r:
            if len(line) == self.width:
                for value, x in zip(line, xrange(self.width)):
                    self.scenario_layer.set(x, y, self.scenario_tileset.tiles[int(value)])
                y += 1
            if y >= self.height:
                break

        layout_file.close()

    # Virtual, should be implemented.
    def initialize(self, local_state):
        pass
        
    def add_party(self, party, position, facing=Direction.DOWN, speed=MapObject.NORMAL_SPEED):
    
        assert self.party is None, 'Map already has a party'
        self.party = party
        self.party_avatar = PartyAvatar(party, facing, speed)
        self.add_object(self.party_avatar, position)
    
    def remove_party(self):
    
        if self.party is None:
            return None, None
        result = self.party, self.party_avatar.position
        self.remove_object(self.party_avatar)
        self.party = None
        self.party_avatar = None
        return result

    def add_object(self, object, position):
    
        self.object_layer.get_pos(position).add_object(object)
        self.objects.append(object)
        object.position, object.map = position, self
        return True
    
    def remove_object(self, object):
    
        self.objects.remove(object)
        self.object_layer.get_pos(object.position).remove_object(object)
        result = object.position
        object.position, object.map = None, None
        return result
        
    def try_to_move_object(self, object, direction):
    
        if object.movement_phase > 0:
            return False
            
        object.facing = direction
        
        old_pos = object.position
        desired = object.position.step(direction)
        if not self.terrain_layer.valid_pos(desired):
            return False

        old_terrain = self.terrain_layer.get_pos(old_pos)
        new_terrain = self.terrain_layer.get_pos(desired)
        old_scenario = self.scenario_layer.get_pos(old_pos)
        new_scenario = self.scenario_layer.get_pos(desired)
        old_object = self.object_layer.get_pos(old_pos)
        new_object = self.object_layer.get_pos(desired)
        if not (object.is_obstacle and (self.is_obstructed(new_terrain, new_scenario, new_object) or self.tile_boundaries_obstructed(old_terrain, new_terrain, old_scenario, new_scenario, direction))):
            # Move
            self.move_object(object, old_object, new_object, desired)
            return True
        else:
            # Do not move
            return False
            
    def is_obstructed(self, new_terrain, new_scenario, new_object):
    
        return (new_terrain.is_obstacle() and not new_scenario.is_below()) or \
               new_scenario.is_obstacle() or \
               new_object.obstacle is not None

    def tile_boundaries_obstructed(self, old_terrain, new_terrain, old_scenario, new_scenario, direction):
    
        inverse = Direction.INVERSE[direction]
        if (old_scenario.cannot_be_entered(direction) or
           (old_terrain.cannot_be_entered(direction) and not old_scenario.is_below())):
            return True
        if (new_scenario.cannot_be_entered(inverse) or
           (new_terrain.cannot_be_entered(inverse) and not new_scenario.is_below())):
            return True
        return False

    def move_object(self, object, old_object, new_object, new_pos):
    
        object.movement_phase = object.speed - 1
        
        old_object.remove_object(object)
        new_object.add_object(object)
        object.position = new_pos

    def __repr__(self):
    
        return '(Map width=' + str(self.width) + ' height=' + str(self.height) + ' file=' + self.map_file + ')'
        
    def __str__(self):
    
        result = ''
        result += '+' + '-' * self.width + '+\n'
        for y in range(self.height):
            result += '|'
            for x in range(self.width):
                if self.party_avatar is not None and self.party_avatar.position == Position(x, y):
                    result += 'P'
                else:
                    result += ' '
            result += '|\n'
        result += '+' + '-' * self.width + '+\n'
        return result


#=================================================================================

class ObjectCell:
    
    def __init__(self):
    
        self.below = []
        self.obstacle = None
        self.above = []
        
        # Reduce the access time of these functions,
        self.below_append, self.below_remove = self.below.append, self.below.remove
        self.above_append, self.above_remove = self.above.append, self.above.remove
    
    def add_object(self, object):
    
        if object.is_obstacle():
            self.obstacle = object
        elif object.is_below():
            self.below_append(object)
        else:
            self.above_append(object)
    
    def remove_object(self, object):
    
        if object.is_obstacle():
            self.obstacle = None
        elif object.is_below():
            self.below_remove(object)
        else:
            self.above_remove(object)
            