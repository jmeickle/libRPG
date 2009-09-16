import csv
import pygame

from librpg.image import TileImage, SlicedImage
from librpg.config import graphics_config
from librpg.locals import *

class Tile(object):

    """
    image: TileImage (read-only)
    An TileImage containing the image for that tile.

    obstacle: int (read-only)
    0 if a party or an object can move over this tile, 3 if they can move under it, 1 if it is considered an obstacle. If it is a counter - that is, if push key events may affect objects on the other side of it -, this attribute is set to 2.

    open_directions: [bool] (read-only)
    4-position array with boolean values indicating if the tile is enterable by the given side.
    """

    BELOW, OBSTACLE, COUNTER, ABOVE = 0, 1, 2, 3

    def __init__(self, image):
        self.image = image
        self.obstacle = -1
        self.open_directions = [None] * 4

    def cannot_be_entered(self, direction):
        return self.open_directions[direction-1]

    def is_counter(self):
        return self.obstacle == Tile.COUNTER

    def is_obstacle(self):
        return self.obstacle == Tile.OBSTACLE or self.obstacle == Tile.COUNTER

    def is_below(self):
        return self.obstacle == Tile.BELOW

    def is_above(self):
        return self.obstacle == Tile.ABOVE

    def get_surface(self, animation_phase=0):
        return self.image.get_surface(animation_phase=animation_phase)


class Tileset(object):

    """
    tiles: [Tile] (read-only)
    Array of the Tiles that may be used to compose the layer.

    size: int (read-only)
    Number of tiles in the tileset.

    image: Surface (read-only)
    Surface with the whole tileset image.

    image_file: string (read-only)
    Name of the image file containing the tileset image.

    boundaries_file: string (read-only)
    Name of the .bnd file containing the attributes of each tile.
    """

    def __init__(self, image_file, boundaries_file):
        self.image_file = image_file
        self.load_image_file()

        self.boundaries_file = boundaries_file
        self.load_boundaries_file()

    def load_image_file(self):
        self.image = pygame.image.load(self.image_file)
        width, height = self.image.get_width(), self.image.get_height()
        tsize = graphics_config.tile_size
        assert width % tsize == 0,\
               'Tileset file width is not a multiple of %d: %s' \
               % (graphics_config.tile_size, self.image_file)
        assert height % tsize == 0,\
               'Tileset file height is not a multiple of %d: %s' \
               % (graphics_config.tile_size, self.image_file)

        tile_width = width / tsize
        tile_height = height / tsize
        self.size = tile_width * tile_height

        self.tiles = []
        sliced_image = SlicedImage(self.image, tsize, tsize)
        for i in xrange(self.size):
            ssur = sliced_image.get_slice(i)
            self.tiles.append(Tile(TileImage([ssur])))

    def load_boundaries_file(self):
        f = file(self.boundaries_file, "r")
        r = csv.reader(f, delimiter=',')

        y = 0
        for line in r:
            if line:
                normalize_type = line[0].lower()
                if normalize_type == 'normal' and y < self.size:
                    self.process_normal_bnd_line(y, line)
                    y += 1
                elif normalize_type == 'animated':
                    self.process_animated_bnd_line(line)
        f.close()

    def process_normal_bnd_line(self, y, line):
        assert y == int(line[1]),\
               'Entry %d in .bnd file should have id %d' % (int(line[1]), y)
        tile = self.tiles[y]
        tile.obstacle = int(line[2])
        for x, dir in zip(range(3, 7), range(0, 4)):
            tile.open_directions[dir] = int(line[x])

    def process_animated_bnd_line(self, line):
        ids = [int(id) for id in line[1:]]
        assert ANIMATION_PERIOD % len(ids) == 0,\
               'The number of animated tiles must divide %d' % ANIMATION_PERIOD
        new_image = TileImage([self.tiles[i].get_surface() for i in ids])
        for id in ids:
            self.tiles[id].image = new_image
