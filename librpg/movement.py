"""
The :mod:`movement` module provides Movement objects that describe
a MapObject's movements. These can be used both for one-time movement
or for routinely movement.
"""

class Movement(object):

    """
    Movements are instructions for a MapObject to move.
    
    Movements can be used on a MapObject in two ways: one is to push them
    to the object's movement queue, which will make the object execute it
    once, as soon as the others that are already in progress or enqueued
    are done. The other way is to insert them into the object's behavior
    to have it execute it as part of its cyclic routine movement.
    """

    def flow(self, obj):
    """
    *Abstract.*
    
    Manipulate the object to have it moved.
    
    Return True if the Movement is done and the next can be executed (right
    after the MapObject's *movement_phase* becomes 0, that is, the object
    stops. Return False if it requires more flow() calls to complete.
    """
        raise NotImplementedError, 'Movement.flow() is abstract'


class MovementQueue(Movement, list):

    """
    A MovementQueue is the object that holds Movements waiting to be
    executed. To fill it, either pass a list in its *contents* parameter
    with the intended contents or append/extend Movements to it like
    any other list.
    
    MovementQueues may be inserted in MovementQueues, and will execute all
    their contents before yielding control.
    """
    
    def __init__(self, contents=None):
        list.__init__(self)
        if contents:
            self.extend(contents)

    def flow(self, obj):
        if len(self) == 0:
            return True
        first = self[0]
        should_remove = first.flow(obj)
        if should_remove:
            self.pop(0)
        if len(self) == 0:
            return True
        else:
            return False


class MovementCycle(Movement):

    """
    A MovementCycle holds Movements that are routinely executed. The
    Movements are not removed from it when executed, but just passed,
    and when the end of the MovementCycle is reached, it starts over.
    
    To fill it, either pass a list in its *contents* parameter
    with the intended contents or append/extend Movements to it like
    any other list.
    
    MovementCycles never yield control.
    """
    
    def __init__(self, contents=None):
        if contents is not None:
            self.movements = contents
        else:
            self.movements = []
        self.current = 0

    def flow(self, obj):
        if len(self.movements) == 0:
            return False
        current = self.movements[self.current]
        should_skip = current.flow(obj)
        if should_skip:
            self.current = (self.current + 1) % len(self.movements)
        return False


class Step(Movement):

    """
    Tries to make the object take one step to *direction*. Yields
    control immediately, not caring whether the step worked or not.
    """

    def __init__(self, direction):
        self.direction = direction

    def flow(self, obj):
        obj.map.try_to_move_object(obj, self.direction)
        return True


class Face(Movement):

    """
    Changes the object's facing to *direction* and immediately yields
    control.
    """

    def __init__(self, direction):
        self.direction = direction

    def flow(self, obj):
        obj.facing = self.direction
        return True


class Wait(Movement):

    """
    Waits *delay* frames before yielding control.
    """

    def __init__(self, delay):
        self.initial_delay = delay
        self.delay = delay

    def flow(self, obj):
        self.delay -= 1
        if self.delay == 0:
            self.delay = self.initial_delay
            return True
        else:
            return False


class Slide(Movement):

    """
    Tries to make the object slide one tile to *direction*. Yields
    control immediately, not caring whether the slide worked or not.
    """

    def __init__(self, direction):
        self.direction = direction

    def flow(self, obj):
        obj.map.try_to_move_object(obj, self.direction, slide=True)
        return True


class ForcedStep(Movement):

    """
    Tries to make the object take one step to *direction*. Yields
    control only when the step is taken.
    """

    def __init__(self, direction):
        self.direction = direction

    def flow(self, obj):
        return obj.map.try_to_move_object(obj, self.direction)

