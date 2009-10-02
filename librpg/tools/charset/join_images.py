import pygame
from pygame import Surface
from sys import argv

pygame.display.init()
d = pygame.display.set_mode((640, 480), 0, 32)

def check_parameters():
    argc = len(argv)
    if argc < 4 or not argv[2].isdigit():
        print 'Usage: python join_images.py [target file] [images per line] '\
              '[file1] [file2] ... [file n]'
        exit()

def parse_parameters():
    argc = len(argv)
    return argv[1], int(argv[2]), [s for s in argv[3:]]

def join_files(target, sources, images_per_line):
    lines = len(sources) / images_per_line
    if len(sources) % images_per_line != 0:
        lines += 1
    first = pygame.image.load(sources[0])
    w, h = first.get_width(), first.get_height()
    
    result = Surface((w * images_per_line, h * lines)).convert_alpha()
    result.fill((255,255,255,0))

    for i, source in enumerate(sources):
        im = pygame.image.load(source)
        im.convert_alpha()
        if im.get_width() != w or im.get_height() != h:
            print 'Image %s is not of the same size as the first'
            exit()
        
        x = w * (i % images_per_line)
        y = h * (i / images_per_line)
        result.blit(im, (x, y))
    # bg = Surface((640, 480), depth=32)
    # bg.convert_alpha()
    # bg.fill((255, 0, 0))
    # bg.blit(result, (0, 0))
    # d.blit(bg, (0, 0))
    # pygame.display.flip()
    # raw_input()
    pygame.image.save(result, target)


if __name__ == '__main__':
    check_parameters()

    target, images_per_line, sources = parse_parameters()
    print 'Target file: %s' % target
    print 'Source files: %s' % ', '.join(sources)

    join_files(target, sources, images_per_line)
    