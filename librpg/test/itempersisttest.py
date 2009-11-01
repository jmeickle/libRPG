# Imports

import librpg
from librpg.map import MapModel
from librpg.mapobject import ScenarioMapObject
from librpg.util import Position, IdFactory
from librpg.party import Character, CharacterReserve, Party
from librpg.world import MicroWorld
from librpg.item import OrdinaryInventory, OrdinaryItem
from librpg.dialog import MessageDialog
from librpg.context import Context
from librpg.path import *

from pygame.locals import *
import os

SAVE_FILE = "itempersisttest_save"

# Items

item_factory = IdFactory()


class LogItem(OrdinaryItem):

    id = 'log'

    def __init__(self):
        OrdinaryItem.__init__(self, 'Log')
item_factory.register(LogItem)


class LeafItem(OrdinaryItem):

    id = 'leaf'

    def __init__(self):
        OrdinaryItem.__init__(self, 'Leaf')
item_factory.register(LeafItem)


# Map objects

class LogPile(ScenarioMapObject):

    def __init__(self, map):
        ScenarioMapObject.__init__(self, map, 0, 2)

    def activate(self, party_avatar, direction):
        added = party_avatar.party.inventory.add_item_by_id('log')
        if added:
            self.map.schedule_message(MessageDialog("Got a Log."))
        else:
            self.map.schedule_message(MessageDialog("Inventory full of Logs."))


class Tree(ScenarioMapObject):

    def __init__(self, map):
        ScenarioMapObject.__init__(self, map, 0, 23)

    def activate(self, party_avatar, direction):
        added = party_avatar.party.inventory.add_item_by_id('leaf')
        if added:
            msg = "Got a Leaf."
        else:
            msg = "Inventory full of Leaves."
        self.map.schedule_message(msg)


class SavePoint(ScenarioMapObject):

    def __init__(self, map):
        ScenarioMapObject.__init__(self, map, 0, 1)

    def activate(self, party_avatar, direction):
        self.map.schedule_message(MessageDialog('You game will be saved to %s.'
                                  % SAVE_FILE, block_movement=True))
        self.map.save_world(SAVE_FILE)
        self.map.schedule_message(MessageDialog('Game saved.',
                                                block_movement=True))


# Map

class PersistTestMap(MapModel):

    def __init__(self):
        MapModel.__init__(self, 'itempersisttest.map',
                          (tileset_path('city_lower.png'),
                           tileset_path('city_lower.bnd')),
                          [(tileset_path('world_upper.png'),
                            tileset_path('world_upper.bnd'))])

    def initialize(self, local_state, global_state):
        self.add_object(LogPile(self), Position(4, 5))
        self.add_object(Tree(self), Position(6, 5))
        self.add_object(SavePoint(self), Position(5, 2))

        self.inventory_context = InventoryContext(self)
        self.add_context(self.inventory_context)


# Party

class TestParty(Party):

    def __init__(self, reserve):
        Party.__init__(self, reserve)
        self.inventory = OrdinaryInventory(item_factory)

    def custom_save(self):
        return self.inventory.save_state()

    def custom_load(self, party_state=None):
        self.inventory.load_state(party_state)
        print 'Loaded', self.inventory.get_items_with_amounts()


# Char and party factories

def char_factory(name):
    CHAR_IMAGES = {'Andy': (charset_path('naked_man.png'), 0),
                   'Brenda': ('test_chars.png', 1),
                   'Charles': ('test_chars.png', 0),
                   'Dylan': ('test_chars.png', 2)}
    image_and_index = CHAR_IMAGES[name]
    return Character(name, image_and_index[0], image_and_index[1])


def party_factory(reserve):
    return TestParty(reserve)


# Inventory context

class InventoryContext(Context):

    def __init__(self, map):
        Context.__init__(self, map)
        self.map = map
        self.reserve = map.world.reserve
        self.party = map.party
        self.inv = map.party.inventory

    KEY_TO_CHAR = {K_a: 'Andy', K_b: 'Brenda', K_c: 'Charles', K_d: 'Dylan'}

    def process_event(self, event):
        if not self.map.controller.message_queue.is_active() \
           and event.type == KEYDOWN:
            if event.key == K_i:
                msg = 'Inventory:' + str(self.inv.get_items_with_amounts())
                self.map.schedule_message(MessageDialog(msg))
                return True
            elif event.key == K_p:
                msg = 'Party:' + str(self.party)
                self.map.schedule_message(MessageDialog(msg))
                msg = 'Reserve:' + str(self.reserve.get_names())
                self.map.schedule_message(MessageDialog(msg))
                return True
            elif event.key in InventoryContext.KEY_TO_CHAR.keys():
                char = InventoryContext.KEY_TO_CHAR[event.key]
                if char in self.party.chars:
                    if (len(self.party.chars) > 1
                        and self.party.remove_char(char)):
                            msg = 'Removed %s.' % char
                    else:
                        msg = 'Cannot remove %s.' % char
                else:
                    if self.party.add_char(char):
                        msg = 'Added %s.' % char
                    else:
                        msg = 'Could not add %s.' % char
                self.map.schedule_message(MessageDialog(msg))
                return True
        return False


# Main

if __name__ == '__main__':
    librpg.init('Item Persist Test')
    librpg.config.graphics_config.config(tile_size=32,
                                         object_height=32,
                                         object_width=32,
                                         scale=2)

    world = MicroWorld(PersistTestMap(), char_factory, party_factory)
    if SAVE_FILE in os.listdir('.'):
        world.load_state(SAVE_FILE)
    else:
        world.initial_state(Position(4, 3),
                             chars=['Andy', 'Brenda', 'Charles', 'Dylan'],
                             party_capacity=3,
                             party=['Andy'])
    world.gameloop()
    exit()
