#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

class Dialog(object):
    def __init__(self, text):
        self.text = text
        
        self.surface_created = False
    def draw(self, r):
        if not self.surface_created:
            font = pygame.font.SysFont("verdana", 12)
            self.s   = pygame.Surface((r.width, r.height/2), SRCALPHA, 32)
            dim = pygame.Rect(20, 20, r.width-40, r.height/2-40)
            pygame.draw.rect(self.s, (128,0,128,128),dim)
            self.s.blit( font.render(self.text, True, (255,255,255)), (40, 40) )
        return self.s, pygame.Rect(0, r.height/2, r.width, r.height/2)
            
