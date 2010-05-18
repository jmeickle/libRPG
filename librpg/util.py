"""
The :mod:`util` module has assorted functions and classes for various
purposes.
"""

from librpg.locals import UP, DOWN, LEFT, RIGHT
from librpg.config import graphics_config, game_config


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

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        else:
            raise IndexError('Position is only 2 dimensional')

    def __setitem__(self, i, value):
        if i == 0:
            self.x = value
        elif i == 1:
            self.y = value
        else:
            raise IndexError('Position is only 2 dimensional')

    def __hash__(self):
        return hash((self.x, self.y))


class Matrix(object):

    """
    Represents a 2-dimensional matrix with fast random access.

    :attr:`width`
        Matrix width.

    :attr:`height`
        Matrix height.
    """

    def __init__(self, width, height):
        self.width = 0
        self.height = 0
        self.m = []
        self.resize(width, height)

    def __repr__(self):
        return '(Matrix %s x %s)' % (self.width, self.height)

    def __getitem__(self, pos):
        """
        Return the element at *pos* == (x, y).

        Raises IndexError if x or y are not inside the matrix's
        limits.
        """
        x, y = pos
        if not self.valid(pos):
            raise IndexError('%s was indexed with x=%s y=%s'
                             % (repr(self), x, y))
        return self.m[y][x]

    def __setitem__(self, pos, value):
        """
        Sets the element at *pos* == (x, y) to *value*.

        Raises IndexError if x or y are not inside the matrix's
        limits.
        """
        x, y = pos
        if not self.valid(pos):
            raise IndexError('%s was indexed with x=%s y=%s'
                             % (repr(self), x, y))
        self.m[y][x] = value

    def valid(self, pos):
        """
        Return whether *pos* == (x, y) is inside the matrix's limits.
        """
        x, y = pos
        return x < self.width and x >= 0 and y < self.height and y >= 0

    def resize(self, width=None, height=None):
        new_width = self.width if (width is None) else width
        new_height = self.height if (height is None) else height

        if height is not None:
            if new_height < self.height:
                self.m = self.m[:new_height]
                outdated_lines = new_height
            elif new_height > self.height:
                for i in xrange(new_height - self.height):
                    self.m.append([None] * new_width)
                outdated_lines = self.height
            else:
                outdated_lines = self.height
            self.height = new_height
        else:
            outdated_lines = self.height

        if width is not None:
            if new_width < self.width:
                for i in xrange(outdated_lines):
                    self.m[i] = self.m[i][:width]
            elif new_width > self.width:
                for i in xrange(outdated_lines):
                    self.m[i].extend([None] * (new_width - self.width))
            self.width = new_width


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
    elif delta == Position(1, 0):
        return RIGHT
    elif delta == Position(0, -1):
        return UP
    elif delta == Position(0, 1):
        return DOWN
    else:
        return None


def check_direction(key):
    if key in game_config.key_up:
        return UP
    elif key in game_config.key_down:
        return DOWN
    elif key in game_config.key_left:
        return LEFT
    elif key in game_config.key_right:
        return RIGHT
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


def fill_with_surface(target, source):
    x, y = 0, 0
    t_w, t_h = target.get_width(), target.get_height()
    s_w, s_h = source.get_width(), source.get_height()
    while y < t_h:
        while x < t_w:
            target.blit(source, (x, y))
            x += s_w
        y += s_h
        x = 0


def descale_point(pos):
    return (pos[0] / float(graphics_config.scale),
            pos[1] / float(graphics_config.scale))


def build_lines(text, box_width, font):
    lines = []
    words = text.split()
    cur_line = words[0]
    _, height = font.size(cur_line)

    for word in words[1:]:
        projected_line = cur_line + ' ' + word
        width, height = font.size(projected_line)
        if width > box_width:
            lines.append([height, cur_line])
            cur_line = word
        else:
            cur_line += ' ' + word
    lines.append([height, cur_line])
    return lines
