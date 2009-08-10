class Movement(object):

    def flow(self, obj):
        raise NotImplementedError, 'Movement.flow() is abstract'


class MovementQueue(Movement, list):

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

    def __init__(self, direction):
        self.direction = direction

    def flow(self, obj):
        obj.map.try_to_move_object(obj, self.direction)
        return True


class Face(Movement):

    def __init__(self, direction):
        self.direction = direction

    def flow(self, obj):
        obj.facing = self.direction
        return True


class Wait(Movement):

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

    def __init__(self, direction):
        self.direction = direction

    def flow(self, obj):
        obj.map.try_to_move_object(obj, self.direction, slide=True)
        return True


class ForcedStep(Movement):

    def __init__(self, direction):
        self.direction = direction

    def flow(self, obj):
        return obj.map.try_to_move_object(obj, self.direction)

