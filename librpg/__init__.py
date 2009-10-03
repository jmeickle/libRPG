import pygame

from librpg import (virtualscreen, config, party, map, world, mapobject,
                    camera, image, loader, item, util, context, maparea,
                    tile, dialog, mapview, menu, movement, state, sound, quest,
                    path)

def init(game_name='LibRPG Game', icon=None):
    pygame.init()
    sound.init()
    
    if icon is not None:
        icon = pygame.image.load(icon)
    else:
        icon = pygame.image.load(path.data_path('icon.png'))
    pygame.display.set_icon(icon)
    
    virtualscreen.init(config.graphics_config.real_screen_dimensions,
                       config.graphics_config.display_mode,
                       config.graphics_config.screen_dimensions,
                       config.graphics_config.scale)
    pygame.display.set_caption(game_name)
