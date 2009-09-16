import pygame
import os
import sys

USAGE = 'Usage: python init_boundaries.py [tilesize] (b/a)'
ABOVE = ['a', 'above']
BELOW = ['b', 'below']

def crop(name):
    parts = name.split('.')
    return '.'.join(parts[:-1])

def create_bnd(img_name, tile_size, type):
    bnd_name = crop(img_name) + '.bnd'
    print 'Creating %s from tileset %s' % (bnd_name, img_name)
    bnd = file(bnd_name, 'w')

    image = pygame.image.load(img_name)
    w = image.get_width() / tile_size
    h = image.get_height() / tile_size

    for i in xrange(h):
        for j in xrange(w):
            write_line(bnd, type, w * i + j)
        bnd.write('\n')

def write_line(file, type, i):
    file.write('normal, %d, %d, 0, 0, 0, 0\n' % (i, 3 if type == 'a' else 0))

if __name__ == '__main__':
    assert len(sys.argv) == 3, USAGE
    assert sys.argv[1].isdigit(), USAGE
    assert sys.argv[2] in ABOVE + BELOW, USAGE

    tile_size = int(sys.argv[1])
    if sys.argv[2] in ABOVE:
        type = 'a'
    else:
        type = 'b'

    for name in os.listdir('.'):
        if (name.endswith('.png')
           or name.endswith('.bmp')
           or name.endswith('.gif')
           or name.endswith('.jpg')
           or name.endswith('.jpeg')):
            create_bnd(name, tile_size, type)
