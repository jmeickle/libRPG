import csv
import operator

import pygame
from pygame.locals import *

from librpg.mapobject import *
from librpg.mapview import *
from librpg.util import *
from librpg.image import *
from librpg.tile import *
from librpg.config import *
from librpg.locals import *
from librpg.movement import Step
from librpg.dialog import MessageQueue


class MapController(object):

    # Read-Only Attributes:
    # map_view - MapView (View component of MVC)
    # map_model - MapModel (Model component of MVC)

    KEY_TO_DIRECTION = {K_DOWN:DOWN, K_UP:UP, K_LEFT:LEFT, K_RIGHT:RIGHT}
    FPS = 30

    def __init__(self, map_model, local_state=None):
        self.map_model = map_model
        self.map_model.controller = self
        self.map_model.initialize(local_state)
        self.map_view = MapView(self.map_model)

    def gameloop(self):
        # Locals for optimization
        map_model = self.map_model
        map_view_draw = self.map_view.draw
        party_avatar = map_model.party_avatar
        party_movement = map_model.party_movement
        self.party_movement_append = party_movement.append
        self.party_movement_remove = party_movement.remove

        map_view_draw()

        self.clock = pygame.time.Clock()
        while map_model.keep_going:
            self.clock.tick(MapController.FPS)

            if map_model.pause_delay > 0:
                map_model.pause_delay -= 1
            else:
                if not map_model.message_queue.is_busy():
                    self.flow_object_movement()

                self.process_input()

                map_model.message_queue.pop_next()

                if party_movement and not party_avatar.scheduled_movement and\
                   not party_avatar.movement_phase and\
                   not map_model.message_queue.is_busy():
                    party_avatar.schedule_movement(Step(party_movement[0]))

            map_view_draw()

    def process_input(self):
        for event in pygame.event.get():
            #print event
            if event.type == QUIT:
                self.map_model.leave()
            elif event.type == KEYDOWN:
                if not self.map_model.message_queue.is_active():
                    direction = MapController.KEY_TO_DIRECTION.get(event.key)
                    if direction is not None and\
                       not direction in self.map_model.party_movement:
                        self.party_movement_append(direction)
                    elif event.key == K_SPACE or event.key == K_RETURN:
                        self.map_model.party_action()
                    elif event.key == K_ESCAPE:
                        self.map_model.leave()
                else:
                    direction = MapController.KEY_TO_DIRECTION.get(event.key)
                    if direction is not None and\
                       not direction in self.map_model.party_movement:
                        self.party_movement_append(direction)
                    elif event.key == K_SPACE or event.key == K_RETURN:
                        self.map_model.message_queue.close()
            elif event.type == KEYUP:
                direction = MapController.KEY_TO_DIRECTION.get(event.key)
                if direction is not None and\
                   direction in self.map_model.party_movement:
                    self.party_movement_remove(direction)

    def flow_object_movement(self):
        party_avatar = self.map_model.party_avatar

        for o in self.map_model.objects:
            if o is not party_avatar:
                o.flow()

        party_avatar.flow()
        self.trigger_collisions()

    def trigger_collisions(self):
        party_avatar = self.map_model.party_avatar
        if party_avatar.just_completed_movement:
            party_avatar.just_completed_movement = False

            # Trigger below objects' collide_with_party()
            for obj in self.map_model.object_layer.\
                       get_pos(party_avatar.position).below:
                obj.collide_with_party(party_avatar, party_avatar.facing)

            # Trigger above objects' collide_with_party()
            for obj in self.map_model.object_layer.\
                       get_pos(party_avatar.position).above:
                obj.collide_with_party(party_avatar, party_avatar.facing)

            # Trigger areas' party_entered and party_moved()
            for area in self.map_model.area_layer.get_pos(party_avatar.position):
                if area not in party_avatar.prev_areas:
                    coming_from_outside = True
                    area.party_entered(party_avatar, party_avatar.position)
                else:
                    coming_from_outside = False
                
                area.party_moved(party_avatar, party_avatar.prev_position,
                                 party_avatar.position, coming_from_outside)

    def sync_movement(self, objects):

        while any([o.scheduled_movement for o in objects]):
            self.clock.tick(MapController.FPS)
            for o in objects:
                o.flow()
            self.map_view.draw()


class MapModel(object):

    """
    party: Party (read-only)
    Active Party on this map.

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
    Pair of names of the files that contain the terrain tileset image
    and boundaries.

    scenario_tileset_files_list: [(string, string)] (read-only)
    List of pairs of names of the files that contain the scenario
    tileset image and boundaries.

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
    Local state to store persistent data about that map. It may be read
    after the gameloop() is broken.
    """

    def __init__(self, map_file, terrain_tileset_files,
                 scenario_tileset_files_list):
        self.party = None
        self.party_avatar = None
        self.party_movement = []

        self.map_file = map_file

        self.terrain_tileset_files = terrain_tileset_files
        self.scenario_tileset_files_list = scenario_tileset_files_list

        self.terrain_tileset = Tileset(self.terrain_tileset_files[0],
                                       self.terrain_tileset_files[1])
        self.scenario_tileset = [Tileset(i, j) for i, j in\
                                 self.scenario_tileset_files_list]

        self.load_from_map_file()

        self.local_state = None

        self.objects = []
        self.below_objects = []
        self.obstacle_objects = []
        self.above_objects = []
        self.object_layer = Matrix(self.width, self.height)
        object_layer_set = self.object_layer.set
        for x in range(self.width):
            for y in range(self.height):
                object_layer_set(x, y, ObjectCell())

        self.areas = []
        self.area_layer = Matrix(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                self.area_layer.set(x, y, [])

        self.message_queue = MessageQueue()

        self.keep_going = True
        self.pause_delay = 0

    def load_from_map_file(self):
        layout_file = open(self.map_file)
        r = csv.reader(layout_file, delimiter=',')

        first_line = r.next()
        self.width = int(first_line[0])
        self.height = int(first_line[1])
        self.scenario_number = int(first_line[2])

        self.terrain_layer = Matrix(self.width, self.height)
        self.scenario_layer = [Matrix(self.width, self.height) for i in\
                               range(self.scenario_number)]

        y = 0
        for line in r:
            if len(line) == self.width:
                for x, value in enumerate(line):
                    self.terrain_layer.set(x, y, self.terrain_tileset.\
                                           tiles[int(value)])
                y += 1
            if y >= self.height:
                break

        for i in xrange(self.scenario_number):
            y = 0
            for line in r:
                if len(line) == self.width:
                    for x, value in enumerate(line):
                        tile = self.scenario_tileset[i].tiles[int(value)]
                        self.scenario_layer[i].set(x, y, tile)
                    y += 1
                if y >= self.height:
                    break

        layout_file.close()

    # Virtual, should be implemented.
    def initialize(self, local_state):
        pass

    # Virtual, should be implemented.
    def save(self):
        return None

    def add_party(self, party, position, facing=DOWN, speed=NORMAL_SPEED):
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

    def add_object(self, obj, position):
        self.object_layer.get_pos(position).add_object(obj)

        self.objects.append(obj)
        if obj.is_below():
            self.below_objects.append(obj)
        elif obj.is_obstacle():
            self.obstacle_objects.append(obj)
        elif obj.is_above():
            self.above_objects.append(obj)
        else:
            raise Exception('Object is neither below, obstacle or above')

        obj.position = position
        obj.areas = self.area_layer.get_pos(position)
        obj.map = self
        return True

    def remove_object(self, obj):
        self.objects.remove(obj)
        if obj.is_below():
            self.below_objects.remove(obj)
        elif obj.is_obstacle():
            self.obstacle_objects.remove(obj)
        elif obj.is_above():
            self.above_objects.remove(obj)
        else:
            raise Exception('Object is neither below, obstacle or above')

        self.object_layer.get_pos(obj.position).remove_object(obj)
        result = obj.position
        obj.position, obj.map = None, None
        return result

    def add_area(self, area, positions):
        self.areas.append(area)
        for pos in positions:
            self.area_layer.get_pos(pos).append(area)
        area.area = positions

    def remove_area(self, area, positions):
        self.areas.remove(area)
        for pos in area.area:
            self.area_layer.get_pos(pos).remove(area)
        area.area = list(set(area.area) - set(positions))

    def try_to_move_object(self, obj, direction, slide=False):
        if obj.movement_phase > 0:
            return False

        obj.facing = direction

        old_pos = obj.position
        desired = obj.position.step(direction)
        if not self.terrain_layer.valid_pos(desired):
            return False

        old_terrain = self.terrain_layer.get_pos(old_pos)
        new_terrain = self.terrain_layer.get_pos(desired)
        old_scenario = [self.scenario_layer[i].get_pos(old_pos) for i in\
                        range(self.scenario_number)]
        new_scenario = [self.scenario_layer[i].get_pos(desired) for i in\
                        range(self.scenario_number)]
        old_object = self.object_layer.get_pos(old_pos)
        new_object = self.object_layer.get_pos(desired)

        if not (obj.is_obstacle() and
                self.is_obstructed(old_terrain, old_scenario, new_terrain,
                                   new_scenario, new_object, direction)):
            # Move
            self.move_object(obj, old_object, new_object, desired, slide)
            if obj is self.party_avatar:
                for area in self.area_layer.get_pos(old_pos):
                    if area not in self.area_layer.get_pos(desired):
                        area.party_left(self.party_avatar, old_pos)
            return True
        else:
            # Do not move, something is on the way
            if obj is self.party_avatar and new_object.obstacle is not None:
                new_object.obstacle.collide_with_party(self.party_avatar,
                                                       direction)
            return False

    def is_obstructed(self, old_terrain, old_scenario_list, new_terrain,
                      new_scenario_list, new_object, direction):
        cannot_leave_old = True
        for old_scenario in reversed(old_scenario_list):
            if old_scenario.is_below() and\
               not old_scenario.cannot_be_entered(direction):
                cannot_leave_old = False
        if cannot_leave_old and\
           old_terrain.cannot_be_entered(direction):
            return True

        inv = inverse(direction)

        if new_object.obstacle is not None:
            return True
        for new_scenario in reversed(new_scenario_list):
            if new_scenario.is_obstacle():
                return True
            elif new_scenario.is_below() and\
                    not new_scenario.cannot_be_entered(inv):
                return False
        return new_terrain.is_obstacle() or new_terrain.cannot_be_entered(inv)

    def move_object(self, obj, old_object, new_object, new_pos, slide):

        obj.movement_phase = obj.speed - 1
        obj.sliding = slide

        old_object.remove_object(obj)
        new_object.add_object(obj)
        obj.prev_position = obj.position
        obj.position = new_pos
        obj.prev_areas = obj.areas
        obj.areas = self.area_layer.get_pos(new_pos)

    def teleport_object(self, obj, new_pos):

        old_pos = obj.position
        old_object = self.object_layer.get_pos(old_pos)
        new_object = self.object_layer.get_pos(new_pos)
        
        old_object.remove_object(obj)
        new_object.add_object(obj)
        obj.prev_position = old_pos
        obj.position = new_pos
        obj.prev_areas = obj.areas
        obj.areas = self.area_layer.get_pos(new_pos)

    def party_action(self):

        old_pos = self.party_avatar.position
        desired = old_pos.step(self.party_avatar.facing)

        # Activate object that the party is looking at
        if self.terrain_layer.valid_pos(desired):
            obj_in_front = self.object_layer.get_pos(desired).obstacle
            if obj_in_front is not None:
               obj_in_front.activate(self.party_avatar,
                                     self.party_avatar.facing)
            across_pos = desired.step(self.party_avatar.facing)
            if (self.terrain_layer.valid_pos(across_pos) and
               ((obj_in_front is not None and obj_in_front.is_counter()) or
               any([layer.get_pos(desired).is_counter() for layer in\
                    self.scenario_layer]))):
                # Counter attribute
                obj_across = self.object_layer.get_pos(across_pos).obstacle
                if obj_across is not None:
                    obj_across.activate(self.party_avatar,
                                        self.party_avatar.facing)

        # Activate objects that the party is standing on or under
        old_object = self.object_layer.get_pos(old_pos)
        for obj in old_object.below:
            obj.activate(self.party_avatar, self.party_avatar.facing)
        for obj in old_object.above:
            obj.activate(self.party_avatar, self.party_avatar.facing)

    def schedule_message(self, message):
        self.message_queue.push(message)

    def leave(self):
        self.keep_going = False

    def pause(self, length):
        self.pause_delay = length

    def __repr__(self):
        return '(Map width=%s height=%s file=%s)' % (str(self.width),
                                                     str(self.height),
                                                     self.map_file)

    def __str__(self):
        result = ''
        result += '+' + '-' * self.width + '+\n'
        for y in range(self.height):
            result += '|'
            for x in range(self.width):
                if self.party_avatar is not None and\
                   self.party_avatar.position == Position(x, y):
                    result += 'P'
                else:
                    result += ' '
            result += '|\n'
        result += '+' + '-' * self.width + '+\n'
        return result

    def sync_movement(self, objects):
    
        self.controller.sync_movement(objects)

class ObjectCell(object):

    def __init__(self):
        self.below = []
        self.obstacle = None
        self.above = []

        # Reduce the access time of these functions,
        self.below_append = self.below.append
        self.below_remove = self.below.remove
        self.above_append = self.above.append
        self.above_remove = self.above.remove

    def add_object(self, obj):
        if obj.is_obstacle():
            self.obstacle = obj
        elif obj.is_below():
            self.below_append(obj)
        else:
            self.above_append(obj)

    def remove_object(self, obj):
        if obj.is_obstacle():
            self.obstacle = None
        elif obj.is_below():
            self.below_remove(obj)
        else:
            self.above_remove(obj)

