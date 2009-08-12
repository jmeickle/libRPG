#!/usr/bin/env python

import pygame
from pygame.locals import *
from config import dialog_config as cfg


class MessageDialog(object):

    def __init__(self, text, block_movement=True):
        self.text = text
        self.surface = None
        self.block_movement = block_movement

    def draw(self, bg_rect):
        if not self.surface:
            font = pygame.font.SysFont(cfg.font_name, cfg.font_size)

            # Create empty surface
            self.surface = pygame.Surface((bg_rect.width, bg_rect.height / 2),
                                          SRCALPHA, 32)

            # Draw dialog background
            dim = pygame.Rect((cfg.border_width, cfg.border_width),
                              (bg_rect.width - 2 * cfg.border_width,
                               bg_rect.height / 2 - 2 * cfg.border_width))
            pygame.draw.rect(self.surface, cfg.bg_color, dim)

            # Split into lines
            self.build_lines(font, bg_rect.width)

            # Draw message
            for line in self.lines:
                self.surface.blit(font.render(line[1], True, cfg.font_color),
                                  (2 * cfg.border_width, 2 * cfg.border_width +
                                   line[0]))

        return self.surface, pygame.Rect(0, bg_rect.height / 2, bg_rect.width,
                                         bg_rect.height / 2)

    def build_lines(self, font, box_width):
        self.lines = []
        last_y_offset = 0
        words = self.text.split()
        cur_line = words[0]

        for word in words[1:]:
            projected_line = cur_line + ' ' + word
            width, height = font.size(projected_line)
            if width > box_width - 4 * cfg.border_width:
                self.lines.append([last_y_offset, cur_line])
                last_y_offset += height + cfg.line_spacing
                cur_line = word
            else:
                cur_line += ' ' + word
        self.lines.append([last_y_offset, cur_line])


class MessageQueue:

    def __init__(self):
        self.current = None
        self.queue=[]
    
    def is_busy(self):
        return self.current is not None and self.current.block_movement

    def is_active(self):
        return self.current is not None

    def pop_next(self):
        if self.current is None and self.queue:
            self.current = self.queue.pop(0)

    def close(self):
        self.current = None

    def push(self, message):
        self.queue.append(message)

    def blit(self, screen, bg_rect):
        if self.current:
            surface, dim = self.current.draw(bg_rect)
            screen.blit(surface, dim)
