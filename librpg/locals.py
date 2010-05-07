from pygame.locals import *

# Direction constants
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

ACTIVATE = 5
MOUSE_ACTIVATE = 6

# Movement speed constants

VERY_FAST_SPEED = 3
FAST_SPEED = 4
NORMAL_SPEED = 6
SLOW_SPEED = 10
VERY_SLOW_SPEED = 15

SPEEDS = [VERY_FAST_SPEED,
          FAST_SPEED,
          NORMAL_SPEED,
          SLOW_SPEED,
          VERY_SLOW_SPEED]

DEFAULT_OBJECT_IMAGE_BASIC_ANIMATION = [[1, 2], [1, 0]]

# World saving constant

PARTY_POSITION_LOCAL_STATE = '__PARTY_POSITION_LOCAL_STATE'
CHARACTERS_LOCAL_STATE = '__CHARACTERS_LOCAL_STATE'
PARTIES_LOCAL_STATE = '__PARTIES_LOCAL_STATE'

# Animated tiles

ANIMATION_PERIOD = 12

# Input

M_1 = 'MB1'
M_2 = 'MB2'
M_3 = 'MB3'
M_4 = 'MB4'
M_5 = 'MB5'
M_6 = 'MB6'
M_7 = 'MB7'
M_8 = 'MB8'
M_9 = 'MB9'
M_10 = 'MB10'
