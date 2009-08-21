"""
The :mod:`dialog` module contains Dialogs that can be displayed through
the use of MessageQueue, which is built-in MapModels. These dialogs
are a tool for displaying conversations, questions, etc.
"""

import pygame
from pygame.locals import *

from librpg.config import dialog_config as cfg
from librpg.config import graphics_config as g_cfg
from librpg.virtualscreen import get_screen
from librpg.context import Context

class MessageDialog(object):

    """
    A MessageDialog is a simple message to be displayed on the screen.
    
    *text* is the string that will be displayed and *block_movement*
    tells the map whether the movement in the map should be blocked while
    the message is shown.
    """

    def __init__(self, text, block_movement=True):
        self.text = text
        self.surface = None
        self.block_movement = block_movement

    def draw(self):
        if not self.surface:
            font = pygame.font.SysFont(cfg.font_name, cfg.font_size)

            # Create empty surface
            self.surface = pygame.Surface((g_cfg.screen_width,
                                           g_cfg.screen_height / 2), SRCALPHA,
                                           32)

            # Draw dialog background
            dim = pygame.Rect((cfg.border_width, cfg.border_width),
                              (g_cfg.screen_width - 2 * cfg.border_width,
                               g_cfg.screen_height / 2 - 2 * cfg.border_width))
            pygame.draw.rect(self.surface, cfg.bg_color, dim)

            # Split into lines
            self.build_lines(font, g_cfg.screen_width)

            # Draw message
            for line in self.lines:
                self.surface.blit(font.render(line[1], True, cfg.font_color),
                                  (2 * cfg.border_width, 2 * cfg.border_width +
                                   line[0]))

        return self.surface, pygame.Rect(0, g_cfg.screen_height / 2,
                                         g_cfg.screen_width,
                                         g_cfg.screen_height / 2)

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

    def process_event(self, event):
        if event.key == K_SPACE or event.key == K_RETURN:
            return False
        else:
            return True


class ChoiceDialog(MessageDialog):

    """
    A ChoiceDialog is a message that comes along a list of options from
    which the player has to pick one option.
    
    *text* is the string that will be displayed and *block_movement*
    tells the map whether the movement in the map should be blocked while
    the message is shown.
    
    *choices* is a list of the options, which should be strings.
    """
    
    def __init__(self, text, choices=[], block_movement=True):
        self.text = text
        self.choices = choices
        self.surface = None
        self.block_movement = block_movement
        self.selected = 0
    
    def get(self):
        return self.selected
    
    def update(self):
        self.surface = None
        
    def draw(self):
        if not self.surface:
            font = pygame.font.SysFont(cfg.font_name, cfg.font_size)

            # Create empty surface
            self.surface = pygame.Surface((g_cfg.screen_width,
                                           g_cfg.screen_height / 2), SRCALPHA,
                                           32)

            # Draw dialog background
            dim = pygame.Rect((cfg.border_width, cfg.border_width),
                              (g_cfg.screen_width - 2 * cfg.border_width,
                               g_cfg.screen_height / 2 - 2 * cfg.border_width))
            pygame.draw.rect(self.surface, cfg.bg_color, dim)

            # Split into lines
            self.build_lines(font, g_cfg.screen_width)

            # Draw message
            for line in self.lines:
                self.surface.blit(font.render(line[1], True, cfg.font_color),
                                  (2 * cfg.border_width+line[0][0],
                                   2 * cfg.border_width +
                                   line[0][1]))
                                   
            for n, line in enumerate(self.choice_lines):
                if n == self.selected:
                    color = cfg.selected_font_color
                else:
                    color = cfg.not_selected_font_color
                    
                self.surface.blit(font.render(line[1], True, color),
                                  (2 * cfg.border_width+line[0][0],
                                   2 * cfg.border_width +
                                   line[0][1]))


        return self.surface, pygame.Rect(0, g_cfg.screen_height / 2,
                                         g_cfg.screen_width,
                                         g_cfg.screen_height / 2)

    def build_lines(self, font, box_width):
        self.lines = []
        self.choice_lines = []
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
        self.lines.append([(0, last_y_offset), cur_line])

        for choice in self.choices:
            width, height = font.size(choice)
            last_y_offset += height + cfg.line_spacing
            self.choice_lines.append([(cfg.border_width, last_y_offset),
                                      choice])

    def process_event(self, event):
        if event.key == K_SPACE or event.key == K_RETURN:
            return False
        elif event.key == K_UP:
            self.selected = (self.selected - 1) % len(self.choice_lines)
            self.update()
        elif event.key == K_DOWN:
            self.selected = (self.selected + 1) % len(self.choice_lines)
            self.update()
            
        return True


class MessageQueue(Context):

    def __init__(self, parent=None):
        Context.__init__(self, parent)
        self.current = None
        self.queue = []
    
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

    def draw(self):
        if self.current:
            surface, dim = self.current.draw()
            get_screen().blit(surface, dim)

    def step(self):
        self.pop_next()

    def process_event(self, event):
        if not self.current:
            return False
            
        if event.type == KEYDOWN:
            if not self.current.process_event(event):
                self.close()
            return True
                
        return False
