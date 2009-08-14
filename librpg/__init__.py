import pygame

from librpg import (virtual_screen, config, party, map, world, mapobject,
                    camera, image, log, item, util, context, maparea, tile,
                    dialog, mapview, menu, movement, state)

def init():
    pygame.init()
    virtual_screen.init(config.graphics_config.real_screen_dimensions,
                        config.graphics_config.display_mode,
                        config.graphics_config.screen_dimensions,
                        config.graphics_config.scale)
