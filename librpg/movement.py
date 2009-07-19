class Movement:

    # Abstract
    def flow(self, obj):
        raise NotImplementedError, 'Movement.flow() is abstract'
        
class MovementQueue(Movement, list):

    def __init__(self):
        list.__init__(self)
        
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

class Step(Movement):

    def __init__(self, direction):
        self.direction = direction
        
    def flow(self, obj):
        obj.map.try_to_move_object(obj, self.direction)
        return True
        