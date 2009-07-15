from util import Direction

class MapObject:

    """
    image: ObjectImage (read-only)
    Image of the MapObject. If this field is None, the object will be invisible.

    map: MapModel (read-only)
    The MapModel in which the MapObject was placed. None is if it not placed in any map.

    position: Position (read-only)
    Where on the map the MapObject is. None if it is not in any map.

    obstacle: int (read-only)
    0 if a party or an object can move over this object, 3 if they can move under it, 1 if it is considered an obstacle. If it is a counter - that is, if push key events may affect objects on the other side of it -, this attribute is set to 2.
    
    facing: Direction (public)
    Direction that the object is facing.
    
    speed: int (public)
    Object speed, in the number of frames to move that object by 1 tile. Use VERY_FAST_SPEED, FAST_SPEED, NORMAL_SPEED, SLOW_SPEED and VERY_SLOW_SPEED.
    
    movement_phase: int (private)
    0 if still, 1 to speed if in the middle of a movement.
    """
    
    BELOW, OBSTACLE, COUNTER, ABOVE = 0, 1, 2, 3
    
    VERY_FAST_SPEED, FAST_SPEED, NORMAL_SPEED, SLOW_SPEED, VERY_SLOW_SPEED = 3, 4, 6, 10, 15
    SPEEDS = [VERY_FAST_SPEED, FAST_SPEED, NORMAL_SPEED, SLOW_SPEED, VERY_SLOW_SPEED]
    
    def __init__(self, obstacle, image=None, facing=Direction.DOWN, speed=NORMAL_SPEED):
    
        assert obstacle in range(0, 3), 'MapObject cannot be created with an obstacle value of ' + str(obstacle)
        self.obstacle = obstacle
        
        self.image, self.movement_phase, self.facing, self.speed = image, 0, facing, speed
        
        self.map, self.position = None, None

    # Virtual
    def activate(self, party):
    
        pass
        
    # Virtual
    def collide_with_party(self, party):
    
        pass
        
    def is_counter(self):
    
        return self.obstacle == MapObject.COUNTER

    def is_obstacle(self):
    
        return self.obstacle == MapObject.OBSTACLE or self.obstacle == MapObject.COUNTER
        
    def is_below(self):
    
        return self.obstacle == MapObject.BELOW
        
    def is_above(self):
    
        return self.obstacle == MapObject.ABOVE
    
    def get_surface(self):
    
        return self.image.get_surface(self)
    
#=================================================================================

class PartyAvatar(MapObject):
    
    def __init__(self, party, facing=Direction.DOWN, speed=MapObject.NORMAL_SPEED):
    
        MapObject.__init__(self, MapObject.OBSTACLE, party.get_image(self), facing, speed)
        self.party = party
        