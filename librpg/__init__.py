import pygame

from librpg import (virtual_screen, config, party, map, world, mapobject,
                    camera, image, log, item, util)
from librpg.locals import *


def init():
    pygame.init()
    virtual_screen.init(config.graphics_config.real_screen_dimensions,
                        config.graphics_config.display_mode,
                        config.graphics_config.screen_dimensions,
                        config.graphics_config.scale)

