import pygame

class ScaledScreen(pygame.Surface):
    """
    The ScaledScreen is a replacement for the Pygame display surface.
    It has the blit() and flip() methods, behaving like the display,
    except it scales whatever is blitted to it to the number configured
    thought *graphics_config*.
    
    The singleton ScaledScreen may be obtained by calling the
    *librpg.virtualscreen.get_screen()* function. The result will be a
    handle to it, which can be blitted on.
    
    This is especially important to implement the draw() methods of
    Contexts that display objects on the screen.
    """

    def __init__(self, width_and_height, real_screen, scale=1, flags=0,
                 depth=0):
        pygame.Surface.__init__(self, width_and_height, flags, depth)
        self.real_screen = real_screen
        real_width = int(width_and_height[0] * scale)
        real_height = int(width_and_height[1] * scale)
        self.real_width_and_height = (real_width, real_height)

    def flip(self):
        """
        Flips the ScaledScreen. This flips the Pygame display.
        """
        pygame.transform.scale(self, self.real_width_and_height,
                               self.real_screen)
        pygame.display.flip()

    def init_real_screen(real_screen_dimensions, display_mode):
        return pygame.display.set_mode(real_screen_dimensions,
                                       display_mode)

    def init_virtual_screen(screen_dimensions, final_screen, scale):
        return virtualscreen.ScaledScreen(screen_dimensions, final_screen,
                                           scale, depth=32)


class VirtualScreen(object):

    def __init__(self):
        self.real_screen = None
        self.screen = None

    def init_real_screen(self, real_screen_dimensions, display_mode):
        self.real_screen = pygame.display.set_mode(real_screen_dimensions,
                                                   display_mode)

    def init_virtual_screen(self, screen_dimensions, scale):
        self.screen = ScaledScreen(screen_dimensions, self.real_screen, scale,
                                   depth=32)

    def create_screen(self, real_screen_dimensions, display_mode,
                      screen_dimensions, scale):
        self.init_real_screen(real_screen_dimensions, display_mode)
        self.init_virtual_screen(screen_dimensions, scale)


screen_container = VirtualScreen()

def init(real_screen_dimensions, display_mode, screen_dimensions, scale):
    screen_container.create_screen(real_screen_dimensions, display_mode,
                                   screen_dimensions, scale)

def get_screen():
    """
    Returns the singleton ScaledScreen, a Surface that works as a screen,
    except it is scaled as configured in *graphics_config*.
    """
    return screen_container.screen

