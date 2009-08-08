import pygame

import virtual_screen
import config
import party
import map
import mapobject
import camera
import image
import log
import item
import util

from locals import *

def init():

    pygame.init()
    virtual_screen.init(config.graphics_config.real_screen_dimensions, config.graphics_config.display_mode, config.graphics_config.screen_dimensions, config.graphics_config.scale)
    
