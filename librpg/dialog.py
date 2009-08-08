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
            BACKGROUND_COLOR = (128, 0, 128, 128)
            FONT_COLOR = (255, 255, 255)
            BORDER_WIDTH = 20
            FONT_NAME = "verdana"
            FONT_SIZE = 12
            font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
            
            # Create empty surface
            self.surface = pygame.Surface((bg_rect.width, bg_rect.height / 2), SRCALPHA, 32)
            
            # Draw dialog background
            dim = pygame.Rect((BORDER_WIDTH, BORDER_WIDTH), (bg_rect.width - 2 * BORDER_WIDTH, bg_rect.height / 2 - 2 * BORDER_WIDTH))
            pygame.draw.rect(self.surface, BACKGROUND_COLOR, dim)
            
            # Split into lines
            self.build_lines(font, bg_rect.width)
            
            # Draw message
            for line in self.lines:
                self.surface.blit(font.render(line[1], True, FONT_COLOR), (2 * BORDER_WIDTH, 2 * BORDER_WIDTH + line[0]))

        return self.surface, pygame.Rect(0, bg_rect.height / 2, bg_rect.width, bg_rect.height / 2)

    def build_lines(self, font, box_width):
    
        BORDER_WIDTH = 20
        LINE_SPACING = 5
        
        self.lines = []
        last_y_offset = 0
        words = self.text.split()
        cur_line = words[0]
        
        for word in words[1:]:
            projected_line = cur_line + ' ' + word
            width, height = font.size(projected_line)
            if width > box_width - 4 * BORDER_WIDTH:
                self.lines.append([last_y_offset, cur_line])
                last_y_offset += height
                cur_line = word
            else:
                cur_line += ' ' + word
        self.lines.append([last_y_offset, cur_line])
        

        return
        
        i = 0
        self.lines = []
        last_y_offset = 0
        
        while 1:
            previous_line = words[i]
            i += 1
            while 1:
                if i >= len(words):
                    self.lines.append([last_y_offset, previous_line])
                    last_y_offset += height + LINE_SPACING
                    break
                print i
                projected_line = previous_line + ' ' + words[i]
                width, height = font.size(projected_line)
                if width > bg_rect.width - 4 * BORDER_WIDTH:
                    self.lines.append([last_y_offset, previous_line])
                    last_y_offset += height + LINE_SPACING
                    break
                previous_line = projected_line
                i += 1
                if i >= len(words):
                    self.lines.append([last_y_offset, previous_line])
                    last_y_offset += height + LINE_SPACING
                    break
            if i + 1 >= len(words):
                break