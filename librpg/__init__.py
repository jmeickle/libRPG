import pygame

def init():
    pygame.init()
    
from config import graphics_config
from virtual_screen import ScaledScreen

def init_real_screen(real_screen_dimensions, display_mode):

    return pygame.display.set_mode(real_screen_dimensions, display_mode)

def init_virtual_screen(screen_dimensions, final_screen, scale):

    return ScaledScreen(screen_dimensions, final_screen, scale, depth=32)

real_screen = init_real_screen(graphics_config.real_screen_dimensions, graphics_config.display_mode)
screen = init_virtual_screen(graphics_config.screen_dimensions, real_screen, graphics_config.scale)

import party
import map
import mapobject
import camera
import image
import log
import item
import util
