import pygame

class ScaledScreen(pygame.Surface):

    def __init__(self, width_and_height, real_screen, scale=1, flags=0,
                 depth=0):
        pygame.Surface.__init__(self, width_and_height, flags, depth)
        self.real_screen = real_screen
        real_width = width_and_height[0] * scale
        real_height = width_and_height[1] * scale
        self.real_width_and_height = (real_width, real_height)

    def flip(self):
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
    return screen_container.screen

