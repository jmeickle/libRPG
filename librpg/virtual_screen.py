import pygame

class ScaledScreen(pygame.Surface):
    
    def __init__(self, width_and_height, real_screen, scale=1, flags=0, depth=0):
        pygame.Surface.__init__(self, width_and_height, flags, depth)
        self.real_screen = real_screen
        real_width = width_and_height[0] * scale
        real_height = width_and_height[1] * scale
        self.real_width_and_height = (real_width, real_height)
    
    def flip(self):
        pygame.transform.scale(self, self.real_width_and_height, self.real_screen)
        pygame.display.flip()
        
