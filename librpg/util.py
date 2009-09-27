"""
The :mod:`util` module has assorted functions and classes for various
purposes.
"""

from librpg.locals import *

class Position(object):

    """
    Represents a pair (x, y) of 2D coordinates. It considers that the
    x axis goes from left to right and the y axis goes downwards.
    
    :attr:`x`
        Horizontal position.

    :attr:`y`
        Vertical position.
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, pos):
        """
        Positions may be added, which is a typical vectorial addition.
        """
        return Position(self.x + pos.x, self.y + pos.y)

    def __sub__(self, pos):
        """
        Positions may be subtracted, which is a typical vectorial subtraction.
        """
        return Position(self.x - pos.x, self.y - pos.y)

    def up(self, amount=1):
        """
        Return a Position that is *amount* tiles above this one.
        """
        return Position(self.x, self.y - amount)

    def down(self, amount=1):
        """
        Return a Position that is *amount* tiles below this one.
        """
        return Position(self.x, self.y + amount)

    def left(self, amount=1):
        """
        Return a Position that is *amount* tiles left of this one.
        """
        return Position(self.x - amount, self.y)

    def right(self, amount=1):
        """
        Return a Position that is *amount* tiles right of this one.
        """
        return Position(self.x + amount, self.y)

    def step(self, direction, amount=1):
        """
        Return a Position that is the position one would get by walking
        *amount* tiles towards *direction*.
        """
        return [None, self.up, self.right, self.down,
                self.left][direction](amount)

    def __repr__(self):
        return '(%s, %s)' % (self.x, self.y)

    def __cmp__(self, another):
        """
        Comparing two Positions will give compare their y coordinates,
        then, if they are tied, compare the x coordinates.
        """
        if self.y < another.y:
            return -1
        elif self.y > another.y:
            return 1
        elif self.x < another.x:
            return -1
        elif self.x > another.x:
            return 1
        else:
            return 0


class Matrix(object):

    """
    Represents a 2-dimensional matrix with fast random access.
    
    :attr:`width`
        Matrix width.
        
    :attr:`height`
        Matrix height.
        
    :attr:`size`
        Number of positions (height * width).
    
    """

    # m - array of elements. The element at (x,y) is at the
    # (x + width*y) position

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = width * height
        self.m = [None] * self.size

    def __repr__(self):
        return '(Matrix %s x %s)' % (self.width, self.height)

    def __str__(self):
        s = ''
        for y in xrange(self.height):
            s += str(self.m[y*self.width:(y+1)*self.width])
            s += '\n'
        return s

    def get(self, x, y):
        """
        Return the element at (*x*, *y*).
        
        Raises IndexError if *x* or *y* are not inside the matrix's
        limits.
        """
        if not self.valid(x, y):
            raise IndexError, '%s was indexed with x=%s y=%s' % (repr(self),
                                                                 x, y)
        return self.m[x + self.width * y]

    def set(self, x, y, value):
        """
        Sets the element at (*x*, *y*) to *value*.
        
        Raises IndexError if *x* or *y* are not inside the matrix's
        limits.
        """
        if not self.valid(x, y):
            raise IndexError, '%s was indexed with x=%s y=%s' % (repr(self),
                                                                 x, y)
        self.m[x + self.width * y] = value

    def get_pos(self, pos):
        """
        Return the element at x=*pos*.x, y=*pos*.y. Meant to be used
        with Position.
        
        Raises IndexError if x or y are not inside the matrix's
        limits.
        """
        return self.get(pos.x, pos.y)

    def set_pos(self, pos, value):
        """
        Set the element at x=*pos*.x, y=*pos*.y to *value*. Meant to be
        used with Position.
        
        Raises IndexError if x or y are not inside the matrix's
        limits.
        """
        self.set(pos.x, pos.y, value)

    def valid(self, x, y):
        """
        Return whether (*x*, *y*) are inside the matrix's limits.
        """
        return x < self.width and x >= 0 and y < self.height and y >= 0

    def valid_pos(self, pos):
        """
        Return whether (*pos*.x, *pos*.y) are inside the matrix's limits.
        """
        return self.valid(pos.x, pos.y)


def inverse(direction):
    """
    Return the opposite of a direction. UP <-> DOWN and LEFT <-> RIGHT.
    """
    return {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}[direction]

def determine_facing(new_pos, old_pos):
    """
    Returns the direction that has to be followed to get from *old_pos*
    to *new_pos*. Returns None if they are not adjacent.
    """
    delta = new_pos - old_pos
    if delta == Position(-1, 0):
        return LEFT
    elif delta == Position(+1, 0):
        return RIGHT
    elif delta == Position(0, -1):
        return UP
    elif delta == Position(0, +1):
        return DOWN
    else:
        return None


class IdFactory(object):

    """
    An IdFactory chooses from a set of classes and creates an instance
    of it based on the passed ID.
    """

    def __init__(self):
        self.classes = {}

    def register(self, _class):
        """
        Register a class-id pair.
        
        *_class* should be the class created when its id is passed
        to fabricate(). It should have id as a class attribute.
        """
        try:
            _class.id
        except AttributeError:
            raise Exception('A class must have an id attribute to be '
                            'registered.')
        assert _class.id not in self.classes.keys(), \
                'id %s already registered' % _class.id
        self.classes[_class.id] = _class

    def fabricate(self, id, *args):
        """
        Return a newly created instance of the class registers with the
        given *id*.
        
        If more arguments are passed, they will be forwarded to the
        class constructor.
        """
        return self.classes[id](*args)

    def __repr__(self):
        return self.classes.__repr__()
