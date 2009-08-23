import pygame
from pygame.locals import *

# Direction constants
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

ACTIVATE = 5

# Movement speed constants

VERY_FAST_SPEED, FAST_SPEED, NORMAL_SPEED, SLOW_SPEED, VERY_SLOW_SPEED = 3, 4, 6, 10, 15

SPEEDS = [VERY_FAST_SPEED, FAST_SPEED, NORMAL_SPEED, SLOW_SPEED, VERY_SLOW_SPEED]

# World saving constant

PARTY_POSITION_LOCAL_STATE = '__PARTY_POSITION_LOCAL_STATE'

# Frames per second

FPS = 30

# Future key config

KEY_TO_DIRECTION = {K_DOWN:DOWN, K_UP:UP, K_LEFT:LEFT, K_RIGHT:RIGHT}
