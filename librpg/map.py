import csv

import pygame
from pygame.locals import *

from mapobject import *
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
    
    def __init__(self, map_model, local_state = None):
        self.map_model = map_model
        self.map_model.initialize(local_state)
        self.map_view = MapView(self.map_model)
        
    def gameloop(self):
        self.map_view.draw()
        
        clock = pygame.time.Clock()
        keep_going = True
        while keep_going:
            clock.tick(Map.FPS)
            self.flow_object_movement()
            
            pos = self.map_model.party_avatar.position
            keep_going = self.process_input()
            if self.map_model.party_movement:
                moved = self.map_model.try_to_move_object(self.map_model.party_avatar, self.map_model.party_movement)
                    
            # debug
            if pos != self.map_model.party_avatar.position:
                print self.map_model
                
            self.map_view.draw()
            
    def process_input(self):
        for event in pygame.event.get():
            # print event
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key in Map.KEY_TO_DIRECTION.keys():
                    self.map_model.party_movement = Map.KEY_TO_DIRECTION[event.key]
                elif event.key == K_ESCAPE:
                    return False
            elif event.type == KEYUP:
                if event.key in Map.KEY_TO_DIRECTION.keys() and Map.KEY_TO_DIRECTION[event.key] == self.map_model.party_movement:
                    self.map_model.party_movement = None
        return True
        
    def flow_object_movement(self):
        for o in self.map_model.objects:
            if o.movement_phase > 0:
                o.movement_phase -= 1

#=================================================================================

class MapView:

    """
    map_model: MapModel (read-only)
    MapModel with the information to be drawn.

    screen: Surface (read-only)
    Screen surface to blit to.

    background: Surface (private)
    Surface containing the static terrain and scenario layers that are drawn at the lower level.

    foreground: Surface (private)
    Surface containing the static scenario tiles that are drawn at the upper level.
    """
    
    def __init__(self, map_model):
        self.map_model = map_model
        
        self.screen = pygame.display.set_mode((GraphicsConfig.SCREEN_WIDTH, GraphicsConfig.SCREEN_HEIGHT))
        self.init_background()
        self.init_foreground()
    
    def init_background(self):
        background_width = GraphicsConfig.TILE_SIZE * self.map_model.width + GraphicsConfig.SCREEN_WIDTH
        background_height = GraphicsConfig.TILE_SIZE * self.map_model.height + GraphicsConfig.SCREEN_HEIGHT
        self.background = pygame.Surface((background_width, background_height))
        
        BLACK = (0, 0, 0)
        self.background.fill(BLACK)
        
        for y in xrange(self.map_model.height):
            for x in xrange(self.map_model.width):
                bg_x = GraphicsConfig.SCREEN_WIDTH / 2 + x * GraphicsConfig.TILE_SIZE
                bg_y = GraphicsConfig.SCREEN_HEIGHT / 2 + y * GraphicsConfig.TILE_SIZE
                terrain_tile_surface = self.map_model.terrain_layer.get(x, y).get_surface()
                self.background.blit(terrain_tile_surface, (bg_x, bg_y))
                
                scenario_tile = self.map_model.scenario_layer.get(x, y)
                if scenario_tile.obstacle != Tile.ABOVE:
                    scenario_tile_surface = scenario_tile.get_surface()
                    self.background.blit(scenario_tile_surface, (bg_x, bg_y))

    def init_foreground(self):
        foreground_width = GraphicsConfig.TILE_SIZE * self.map_model.width + GraphicsConfig.SCREEN_WIDTH
        foreground_height = GraphicsConfig.TILE_SIZE * self.map_model.height + GraphicsConfig.SCREEN_HEIGHT
        self.foreground = pygame.Surface((foreground_width, foreground_height), SRCALPHA, 32)
        
        for y in xrange(self.map_model.height):
            for x in xrange(self.map_model.width):
                scenario_tile = self.map_model.scenario_layer.get(x, y)
                if scenario_tile.obstacle == Tile.ABOVE:
                    fg_x = GraphicsConfig.SCREEN_WIDTH / 2 + x * GraphicsConfig.TILE_SIZE
                    fg_y = GraphicsConfig.SCREEN_HEIGHT / 2 + y * GraphicsConfig.TILE_SIZE
                    scenario_tile_surface = scenario_tile.get_surface()
                    self.foreground.blit(scenario_tile_surface, (fg_x, fg_y))

    def draw(self):
        party_avatar = self.map_model.party_avatar
    
        # Draw the background
        x_offset, y_offset = 0, 0
        if party_avatar:
            party_pos = party_avatar.position
            if party_avatar.movement_phase > 0:
                offset = party_avatar.movement_phase * GraphicsConfig.TILE_SIZE / party_avatar.speed
                if party_avatar.facing == Direction.UP:
                    y_offset = offset
                elif party_avatar.facing == Direction.RIGHT:
                    x_offset = -offset
                elif party_avatar.facing == Direction.DOWN:
                    y_offset = -offset
                elif party_avatar.facing == Direction.LEFT:
                    x_offset = offset
        else:
            party_pos = Position(0, 0)
            
        bg_area = pygame.Rect((party_pos.x * GraphicsConfig.TILE_SIZE + x_offset, party_pos.y * GraphicsConfig.TILE_SIZE + y_offset), (GraphicsConfig.SCREEN_WIDTH, GraphicsConfig.SCREEN_HEIGHT))
        self.screen.blit(self.background, (0, 0), bg_area)
        
        # Draw the party avatar
        if party_avatar:
            party_place = (GraphicsConfig.SCREEN_WIDTH - GraphicsConfig.OBJECT_WIDTH + GraphicsConfig.TILE_SIZE) / 2, (GraphicsConfig.SCREEN_HEIGHT / 2 - GraphicsConfig.OBJECT_HEIGHT + GraphicsConfig.TILE_SIZE)
            self.screen.blit(party_avatar.get_surface(), pygame.Rect(party_place, (GraphicsConfig.OBJECT_WIDTH, GraphicsConfig.OBJECT_HEIGHT)))
        
        # Draw the foreground
        self.screen.blit(self.foreground, (0, 0), bg_area)
        
        # Flip display
        pygame.display.flip()
        
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
        self.party, self.party_avatar, self.party_movement = None, None, None
        
        self.map_file = map_file
        
        self.terrain_tileset_files = terrain_tileset_files
        self.scenario_tileset_files = scenario_tileset_files
        
        self.terrain_tileset = Tileset(self.terrain_tileset_files[0], self.terrain_tileset_files[1])
        self.scenario_tileset = Tileset(self.scenario_tileset_files[0], self.scenario_tileset_files[1])
        
        self.load_from_map_file()
        
        self.local_state = None
        
        self.objects = []
        self.object_layer = Matrix(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                self.object_layer.set(x, y, ObjectCell())

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
        
    def add_party(self, party, position, facing = Direction.DOWN, speed = MapObject.NORMAL_SPEED):
        assert self.party == None, 'Map already has a party'
        self.party = party
        self.party_avatar = PartyAvatar(party, facing, speed)
        self.add_object(self.party_avatar, position)
    
    def remove_party(self):
        if self.party == None:
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
            
        desired = object.position.step(direction)
        if not self.terrain_layer.valid_pos(desired):
            return False

        object.facing = direction
        old_terrain = self.terrain_layer.get_pos(object.position)
        new_terrain = self.terrain_layer.get_pos(desired)
        old_scenario = self.scenario_layer.get_pos(object.position)
        new_scenario = self.scenario_layer.get_pos(desired)
        old_object = self.object_layer.get_pos(object.position)
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
               new_object.obstacle != None

    def tile_boundaries_obstructed(self, old_terrain, new_terrain, old_scenario, new_scenario, direction):
        inverse = Direction.INVERSE[direction]
        if (old_scenario.cannot_be_entered(direction) or
           (old_terrain.cannot_be_entered(inverse) and not old_scenario.is_below())):
            return True
        if (new_scenario.cannot_be_entered(direction) or
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
                if self.party_avatar != None and self.party_avatar.position == Position(x, y):
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
    
    def add_object(self, object):
        if object.is_obstacle():
            self.obstacle = object
        elif object.is_below():
            self.below.append(object)
        else:
            self.above.append(object)
    
    def remove_object(self, object):
        if object.is_obstacle():
            self.obstacle = None
        elif object.is_below():
            self.below.remove(object)
        else:
            self.above.remove(object)
            