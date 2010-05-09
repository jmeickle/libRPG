# Basic ###############################

TRANSPARENT = (0, 0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DARK_RED = (128, 0, 0)
DARK_GREEN = (0, 128, 0)
DARK_BLUE = (0, 0, 128)

DARKER_RED = (64, 0, 0)
DARKER_GREEN = (0, 64, 0)
DARKER_BLUE = (0, 0, 64)

CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

DARK_CYAN = (0, 128, 128)
DARK_MAGENTA = (128, 0, 128)
DARK_YELLOW = (128, 128, 0)

DARKER_CYAN = (0, 64, 64)
DARKER_MAGENTA = (64, 0, 64)
DARKER_YELLOW = (64, 64, 0)


# Complex #############################

INDIGO = (75, 0, 130)
GOLD = (255, 215, 0)
FOREST_GREEN = (34, 139, 34)
MIDNIGHT_BLUE = (25, 25, 112)
TURQUOISE = (64, 224, 208)
CRIMSON = (220, 20, 60)
ORANGE = (255, 165, 0)
SALMON = (255, 160, 122)


# Aliases #############################

GREY = GRAY

MAROON = DARK_RED
NAVY = DARK_BLUE

TEAL = DARK_CYAN
PURPLE = DARK_MAGENTA
OLIVE = DARK_YELLOW


# Functions ###########################

def transparency(color, amount):
    """
    Return a transparent version of *color*.
    
    *color* should be a 3-tuple representing an RGB color, with values in
    the 0-255 range. *amount* should be a number in [0, 1] representing
    how transparent the result should be, being 0 opaque and 1 invisible.
    """
    assert amount >= 0 and amount <= 1, 'Second argument should be a number'\
                                        ' in [0, 1]'
    assert len(color) == 3, 'First argument should be a 3-tuple representing '\
                            'an RGB color'
    return color + (int(255 * (1 - amount)),)
