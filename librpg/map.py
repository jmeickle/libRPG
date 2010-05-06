"""
The :mod:`map` module is one of the main modules in LibRPG. It contains
the definition of MapModel, which is the class representing a map in
which a party will walk, act, etc.
"""

import csv

from librpg.mapobject import PartyAvatar
from librpg.mapview import MapView
from librpg.sound import MapMusic
from librpg.util import (check_direction, determine_facing, Position,
                         Matrix, inverse)
from librpg.tile import Tileset
from librpg.config import game_config
from librpg.locals import (ACTIVATE, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, DOWN,
                           NORMAL_SPEED, PARTY_POSITION_LOCAL_STATE, UP,
                           LEFT, RIGHT)
from librpg.movement import Step, PathMovement
from librpg.context import Context, Model, get_context_stack
from librpg.dialog import MessageQueue
from librpg.input import Input


class MapController(Context):

    # Read-Only Attributes:
    # map_view - MapView (View component of MVC)
    # map_model - MapModel (Model component of MVC)

    def __init__(self, map_model, parent=None):
        Context.__init__(self, parent)
        self.map_model = map_model
        self.map_model.controller = self
        self.map_model.initialize(self.map_model.local_state,
                                  self.map_model.global_state)
        self.map_view = MapView(self.map_model)
        self.map_music = MapMusic(self.map_model)
        self.__moving_sync = False
        self.message_queue = MessageQueue(self)

    def initialize(self):
        map_model = self.map_model
        self.__map_view_draw = self.map_view.draw
        self.party_avatar = map_model.party_avatar

        # Initialize contexts
        context_stack = get_context_stack()
        context_stack.stack_context(self.message_queue)
        for context in map_model.contexts:
            context_stack.stack_context(context)

    def update(self):
        if self.map_model.pause_delay > 0:
            self.map_model.pause_delay -= 1
            return False

        if self.__moving_sync:
            sync_stopped = self.sync_movement_step()
            if not sync_stopped:
                return False

        if not self.message_queue.is_busy():
            self.flow_object_movement()
            self.update_objects()

        if not self.party_avatar.scheduled_movement \
           and not self.party_avatar.movement_phase \
           and not self.message_queue.is_busy():
                self.__update_input()

        return False

    def __update_input(self):
        for key in game_config.key_cancel:
            if Input.down(key):
                get_context_stack().stop()
                return
            
        for key in game_config.key_action:
            if Input.down(key):
                self.map_model.party_action()
                return
        
        for key in game_config.key_up:
            if Input.motion(key):
                self.party_avatar.schedule_movement(Step(UP))
                return

        for key in game_config.key_down:
            if Input.motion(key):
                self.party_avatar.schedule_movement(Step(DOWN))
                return

        for key in game_config.key_left:
            if Input.motion(key):
                self.party_avatar.schedule_movement(Step(LEFT))
                return

        for key in game_config.key_right:
            if Input.motion(key):
                self.party_avatar.schedule_movement(Step(RIGHT))
                return

        if (game_config.map_mouse_enabled
            and Input.down('MB1')):
            print 'mouse'
            if not self.party_avatar.scheduled_movement:
                self.mouse_movement(Input.get('MB1')[0].pos)
                return

    def draw(self):
        self.__map_view_draw()
        self.map_music.update()

    def flow_object_movement(self):
        party_avatar = self.map_model.party_avatar

        for o in self.map_model.objects:
            if o is not party_avatar:
                o.flow()

        party_avatar.flow()
        self.trigger_collisions()

    def trigger_collisions(self):
        avatar = self.map_model.party_avatar
        if avatar.just_completed_movement:
            avatar.just_completed_movement = False
            coming_from_direction = determine_facing(avatar.position,
                                                     avatar.prev_position)

            # Trigger below objects' collide_with_party()
            for obj in self.map_model.object_layer[avatar.position].below:
                obj.collide_with_party(avatar,
                                       coming_from_direction)

            # Trigger above objects' collide_with_party()
            for obj in self.map_model.object_layer[avatar.position].above:
                obj.collide_with_party(avatar,
                                       coming_from_direction)

            # Trigger areas' party_entered and party_moved()
            for area in self.map_model.area_layer[avatar.position]:
                if area not in avatar.prev_areas:
                    coming_from_outside = True
                    area.party_entered(avatar, avatar.position)
                else:
                    coming_from_outside = False

                area.party_moved(avatar, avatar.prev_position,
                                 avatar.position, coming_from_outside)

    def sync_movement(self, objects):
        self.__sync_objects = objects
        self.__moving_sync = True

    def sync_movement_step(self):
        if all([not o.scheduled_movement for o in self.__sync_objects]):
            self.__moving_sync = False
            return True
        for o in self.__sync_objects:
            o.flow()
        return False

    def update_objects(self):
        for o in self.map_model.updatable_objects:
            o.update()

    def gameover(self):
        get_context_stack().stop()

    def mouse_movement(self, pos):
        target_x, target_y = self.map_view.calc_pos_from_mouse(pos)
        if self.map_model.terrain_layer.valid((target_x, target_y)):
            movement = PathMovement(self.map_model,
                                    self.map_model.party_avatar,
                                    Position(target_x, target_y))
            self.map_model.party_avatar.schedule_movement(movement)


class MapModel(Model):

    """
    The MapModel is the class that models a map's data and behaviour. It
    is the Model component of the MVC pattern. MapModel is a class made to
    be inherited, so that specific behavior (objects, areas, parallel
    processes) may be added.
    """

    def __init__(self, map_file, terrain_tileset_files,
                 scenario_tileset_files_list):
        """
        *Constructor:*

        Initialize the MapModel with a layout defined by *map_file* (a .map
        file).

        The terrain tileset is specified by *terrain_tileset_files*, which
        is a tuple (tileset image filename, tileset boundaries filename).
        Tileset image filename should be a bitmap file (.png typically)
        and tileset boundaries filename) should be a .bnd file.

        The scenario tilesets are specified by
        *scenario_tileset_files_list*, a list of tuples like the one passed
        as *terrain_tileset_files*. Each will correspond to a scenario
        layer.
        """
        Model.__init__(self)

        self.world = None
        self.id = None

        self.music = None

        # Set up party
        self.party = None
        self.party_avatar = None

        # Load file data
        self.map_file = map_file
        self.terrain_tileset_files = terrain_tileset_files
        self.scenario_tileset_files_list = scenario_tileset_files_list

        self.terrain_tileset = Tileset(self.terrain_tileset_files[0],
                                       self.terrain_tileset_files[1])
        self.scenario_tileset = [Tileset(i, j) for i, j in\
                                 self.scenario_tileset_files_list]

        self.load_from_map_file()

        # Set up local state
        self.local_state = None

        # Set up objects
        self.objects = []
        self.below_objects = []
        self.obstacle_objects = []
        self.above_objects = []
        self.updatable_objects = []
        self.object_layer = Matrix(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                self.object_layer[x, y] = ObjectCell()

        # Set up areas
        self.areas = []
        self.area_layer = Matrix(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                self.area_layer[x, y] = []

        # Set up context system
        self.pause_delay = 0
        self.contexts = []

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
                    self.terrain_layer[x, y] = self.terrain_tileset.\
                                               tiles[int(value)]
                y += 1
            if y >= self.height:
                break

        for i in xrange(self.scenario_number):
            y = 0
            for line in r:
                if len(line) == self.width:
                    for x, value in enumerate(line):
                        tile = self.scenario_tileset[i].tiles[int(value)]
                        self.scenario_layer[i][x, y] = tile
                    y += 1
                if y >= self.height:
                    break

        layout_file.close()

    # Virtual, should be implemented.
    def initialize(self, local_state, global_state):
        """
        *Virtual*

        Put the map in an initial, virgin state if the *local_state*
        specified is None. Puts the map in a state loaded from the
        *local_state*, and the *global_state* otherwise.

        *local_state* is the serializable object returned by
        MapModel.save_state() when this map was saved. *global_state*
        is a dict mapping all feature strings to their local states.
        """
        pass

    # Virtual, should be implemented.
    def save_state(self):
        """
        *Virtual*

        Save the map's state to a local state and return it.
        """
        return None

    def add_party(self, party, position, facing=DOWN, speed=NORMAL_SPEED):
        """
        Add a *party* (Party instance) to the Map at the given *position*.
        Optionally, the starting *facing* and *speed* may be specified. The
        defaults are *facing* down and normal *speed*.
        """
        assert self.party is None, 'Map already has a party'
        self.party = party
        self.party_avatar = PartyAvatar(party, facing, speed)
        self.add_object(self.party_avatar, position)

    def remove_party(self):
        """
        Remove the party from the Map, returning a 2-tuple with it as first
        element and its position as second element. Return (None, None) if
        there is no party in the map.
        """
        if self.party is None:
            return None, None
        result = self.party, self.party_avatar.position
        self.remove_object(self.party_avatar)
        self.party = None
        self.party_avatar = None
        return result

    def add_object(self, obj, position):
        """
        Add an object to the map at the specified position. Returns whether
        the operation was successful (it can fail when the position is
        occupied by an obstacle and the object to be added is also an
        obstacle).
        """
        self.object_layer[position].add_object(obj)

        self.objects.append(obj)
        if obj.is_below():
            self.below_objects.append(obj)
        elif obj.is_obstacle():
            self.obstacle_objects.append(obj)
        elif obj.is_above():
            self.above_objects.append(obj)
        else:
            raise Exception('Object is neither below, obstacle or above')
        if hasattr(obj, 'update'):
            self.updatable_objects.append(obj)

        obj.position = position
        obj.areas = self.area_layer[position]
        obj.map = self
        return True

    def remove_object(self, obj):
        """
        Remove an object from the map and returns the Position where it was.
        Return None if the object was not in the map.
        """
        self.objects.remove(obj)
        if obj.is_below():
            self.below_objects.remove(obj)
        elif obj.is_obstacle():
            self.obstacle_objects.remove(obj)
        elif obj.is_above():
            self.above_objects.remove(obj)
        else:
            raise Exception('Object is neither below, obstacle or above')
        if hasattr(obj, 'update'):
            self.updatable_objects.remove(obj)

        self.object_layer[obj.position].remove_object(obj)
        result = obj.position
        obj.position, obj.map = None, None
        return result

    def add_area(self, area, positions):
        """
        Add a MapArea to the map at the specified positions. *Positions*
        should be an iterable that returns the Positions over which the
        MapArea extends.
        """
        self.areas.append(area)
        for pos in positions:
            self.area_layer[pos].append(area)
        area.area = positions

    def remove_area(self, area, positions):
        """
        Remove a MapArea from the map at the specified positions.
        *Positions* should be an iterable that returns the Positions from
        which the area should be removed.
        """
        self.areas.remove(area)
        for pos in area.area:
            self.area_layer[pos].remove(area)
        area.area = list(set(area.area) - set(positions))

    def try_to_move_object(self, obj, direction, slide=False, back=False):
        """
        Try to move an object to the specified direction (UP, DOWN, LEFT or
        RIGHT). Return whether the object could be moved.

        If *slide* is True, the movement will use only the static frame of
        the object. If *back* is True, the movement will be backwards.
        """
        if obj.movement_phase > 0:
            return False

        if back:
            obj.facing = inverse(direction)
        else:
            obj.facing = direction

        old_pos = obj.position
        desired = obj.position.step(direction)
        if not self.terrain_layer.valid(desired):
            return False

        if not obj.is_obstacle() or self.can_move(old_pos, desired, direction):
            # Move
            old_object = self.object_layer[old_pos]
            new_object = self.object_layer[desired]
            self.move_object(obj, old_object, new_object, desired, slide, back)
            if obj is self.party_avatar:
                for area in self.area_layer[old_pos]:
                    if area not in self.area_layer[desired]:
                        area.party_left(self.party_avatar, old_pos)
            return True
        else:
            # Do not move, something is on the way
            new_object = self.object_layer[desired]
            if obj is self.party_avatar and new_object.obstacle is not None:
                new_object.obstacle.collide_with_party(self.party_avatar,
                                                       direction)
            return False

    def can_move(self, old_pos, desired, direction):
        if not self.terrain_layer.valid(desired):
            return False

        old_terrain = self.terrain_layer[old_pos]
        new_terrain = self.terrain_layer[desired]
        old_scenario = [self.scenario_layer[i][old_pos] for i in\
                        range(self.scenario_number)]
        new_scenario = [self.scenario_layer[i][desired] for i in\
                        range(self.scenario_number)]
        new_object = self.object_layer[desired]

        return not self.is_obstructed(old_terrain, old_scenario, new_terrain,
                                      new_scenario, new_object, direction)

    def is_obstructed(self, old_terrain, old_scenario_list, new_terrain,
                      new_scenario_list, new_object, direction):

        if new_object.obstacle is not None:
            return True

        if self.direction_obstructed(old_terrain, old_scenario_list, \
           direction):
            return True

        inv = inverse(direction)
        if self.direction_obstructed(new_terrain, new_scenario_list, inv):
            return True

        return False

    def direction_obstructed(self, terrain, scenario_list, direction):
        for scenario in reversed(scenario_list):
            if scenario.cannot_be_entered(direction)\
               or scenario.is_obstacle():
                return True
            elif scenario.is_below():
                return False

        if terrain.is_obstacle() or terrain.cannot_be_entered(direction):
            return True
        else:
            return False

    def move_object(self, obj, old_object, new_object, new_pos, slide, back):
        obj.movement_phase = obj.speed - 1
        obj.sliding = slide
        obj.going_back = back

        old_object.remove_object(obj)
        new_object.add_object(obj)
        obj.prev_position = obj.position
        obj.position = new_pos
        obj.prev_areas = obj.areas
        obj.areas = self.area_layer[new_pos]

    def teleport_object(self, obj, new_pos):
        old_pos = obj.position
        old_object = self.object_layer[old_pos]
        new_object = self.object_layer[new_pos]

        old_object.remove_object(obj)
        new_object.add_object(obj)
        obj.prev_position = old_pos
        obj.position = new_pos
        obj.prev_areas = obj.areas
        obj.areas = self.area_layer[new_pos]

    def party_action(self):
        old_pos = self.party_avatar.position
        desired = old_pos.step(self.party_avatar.facing)

        # Activate object that the party is looking at
        if self.terrain_layer.valid(desired):
            obj_in_front = self.object_layer[desired].obstacle
            if obj_in_front is not None:
                obj_in_front.activate(self.party_avatar,
                                      self.party_avatar.facing)
            across_pos = desired.step(self.party_avatar.facing)
            if (self.terrain_layer.valid(across_pos) and
               ((obj_in_front is not None and obj_in_front.is_counter()) or
               any([layer[desired].is_counter() for layer in\
                    self.scenario_layer]))):
                # Counter attribute
                obj_across = self.object_layer[across_pos].obstacle
                if obj_across is not None:
                    obj_across.activate(self.party_avatar,
                                        self.party_avatar.facing)

        # Activate objects that the party is standing on or under
        old_object = self.object_layer[old_pos]
        for obj in old_object.below:
            obj.activate(self.party_avatar, self.party_avatar.facing)
        for obj in old_object.above:
            obj.activate(self.party_avatar, self.party_avatar.facing)

    def schedule_message(self, message):
        """
        Add a Dialog to the message queue, displaying it as soon as the
        messages that were previously there are done.
        """
        self.controller.message_queue.push(message)

    def pause(self, length):
        """
        Stop movement and acting in the map for *length* frames.
        """
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
        """
        Stop movement and acting in the map, except for the movement
        already scheduled or in progress in the objects specified.
        *objects* should be a list of those MapObjects.
        """
        self.controller.sync_movement(objects)

    def save_world(self, filename):
        """
        Save the game to the given file.
        """
        self.world.state.save_local(self.id, self.save_state())
        party_local_state = (self.id, self.party_avatar.position,
                             self.party_avatar.facing)
        self.world.state.save_local(PARTY_POSITION_LOCAL_STATE,
                                    party_local_state)
        self.world.save(filename)

    def add_context(self, context):
        """
        Add a context to be run over this map and the message queue
        context.
        """
        self.contexts.append(context)

    def set_music(self, music_file):
        """
        Set the background for the map.
        """
        self.music = music_file

    def gameover(self):
        """
        End the game.
        """
        self.custom_gameover()
        self.controller.gameover()
        self.world.custom_gameover()

    def custom_gameover(self):
        """
        *Virtual.*

        Overload to perform any reaction necessary to a MapModel.gameover()
        call.
        """
        pass

    def create_controller(self):
        return MapController(self, self.controller_parent)

    def set_states(self, local_state, global_state):
        self.local_state = local_state
        self.global_state = global_state


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
