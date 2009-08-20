import os

from librpg.locals import *


class Position(object):

    # This considers that x axis goes from left to right and y axis goes downwards

    # Read-Only Attributes
    # x - horizontal position
    # y - vertical position

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, pos):
        return Position(self.x + pos.x, self.y + pos.y)

    def up(self, amount=1):
        return Position(self.x, self.y - amount)

    def down(self, amount=1):
        return Position(self.x, self.y + amount)

    def left(self, amount=1):
        return Position(self.x - amount, self.y)

    def right(self, amount=1):
        return Position(self.x + amount, self.y)

    def step(self, direction, amount=1):
        return [None, self.up, self.right, self.down,
                self.left][direction](amount)

    def __repr__(self):
        return '(%s, %s)' % (self.x, self.y)

    def __cmp__(self, another):
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

    # Read-Only Attributes
    # width - the matrix's width
    # height - the matrix's height
    # size - total number of positions in the matrix (width * height)

    # Private Attributes
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
        if not self.valid(x, y):
            raise IndexError, '%s was indexed with x=%s y=%s' % (repr(self),
                                                                 x, y)
        return self.m[x + self.width * y]

    def set(self, x, y, value):

        if not self.valid(x, y):
            raise IndexError, '%s was indexed with x=%s y=%s' % (repr(self),
                                                                 x, y)
        self.m[x + self.width * y] = value

    def get_pos(self, pos):
        return self.get(pos.x, pos.y)

    def set_pos(self, pos, value):
        self.set(pos.x, pos.y, value)

    def valid(self, x, y):
        return x < self.width and x >= 0 and y < self.height and y >= 0

    def valid_pos(self, pos):
        return self.valid(pos.x, pos.y)


def inverse(direction):
    """
    Return the opposite of a direction. UP <-> DOWN and LEFT <-> RIGHT.
    """
    return {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}[direction]

def lib_path(relative_path):
    """
    Return the absolute file path of a file, specified by a *relative_path*
    to the librpg module root directory.
    """
    return os.path.join(os.path.split(__file__)[0], relative_path)
