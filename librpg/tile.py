import csv

import pygame

from image import TileImage
from config import *

class Tile:

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
        return self.is_obstacle() or self.open_directions[direction-1]

    def is_counter(self):
        return self.obstacle == Tile.COUNTER

    def is_obstacle(self):
        return self.obstacle == Tile.OBSTACLE or self.obstacle == Tile.COUNTER
        
    def is_below(self):
        return self.obstacle == Tile.BELOW
        
    def is_above(self):
        return self.obstacle == Tile.ABOVE
    
    def get_surface(self):
        return self.image.get_surface()
        
#=================================================================================

class Tileset:

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
        assert width % GraphicsConfig.TILE_SIZE == 0, 'Tileset file width is not a multiple of ' + str(GraphicsConfig.TILE_SIZE) + ': ' + self.image_file
        assert height % GraphicsConfig.TILE_SIZE == 0, 'Tileset file height is not a multiple of ' + str(GraphicsConfig.TILE_SIZE) + ': ' + self.image_file
        
        tile_width, tile_height = width / GraphicsConfig.TILE_SIZE, height / GraphicsConfig.TILE_SIZE
        self.size = tile_width * tile_height
        
        print 'load_image_file', 'width=' + str(width), 'height=' + str(height), 'tile_width=' + str(tile_width), 'tile_height=' + str(tile_height)
        
        self.tiles = []
        for i in xrange(self.size):
            x, y = i % tile_width, i / tile_width
            self.tiles.append(Tile(TileImage(self.image.subsurface((x * GraphicsConfig.TILE_SIZE, y * GraphicsConfig.TILE_SIZE), (GraphicsConfig.TILE_SIZE, GraphicsConfig.TILE_SIZE)))))
        
    def load_boundaries_file(self):
        f = file(self.boundaries_file, "r")
        r = csv.reader(f, delimiter=',')

        y = 0
        for line in r:
            if len(line) == 5:
                tile = self.tiles[y]
                tile.obstacle = int(line[0])
                for x, dir in zip(range(1, 5), range(0, 4)):
                    tile.open_directions[dir] = int(line[x])
                y += 1
            if y >= self.size:
                break
        f.close()
        