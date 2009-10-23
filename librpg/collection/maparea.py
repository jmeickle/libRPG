from librpg.maparea import MapArea
from librpg.util import Position

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
