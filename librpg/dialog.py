#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

class MessageDialog(object):

    def __init__(self, text):
    
        self.text = text
        self.surface = None
        
    def draw(self, bg_rect):
    
        if not self.surface:
            font = pygame.font.SysFont("verdana", 12)
            self.surface = pygame.Surface((bg_rect.width, bg_rect.height/ 2), SRCALPHA, 32)
            dim = pygame.Rect(20, 20, bg_rect.width - 40, bg_rect.height / 2 - 40)
            pygame.draw.rect(self.surface, (128, 0, 128, 128), dim)
            self.surface.blit(font.render(self.text, True, (255, 255, 255)), (40, 40))

        return self.surface, pygame.Rect(0, bg_rect.height / 2, bg_rect.width, bg_rect.height / 2)
