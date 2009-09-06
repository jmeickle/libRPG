"""
The :mod:`dialog` module contains Dialogs that can be displayed through
the use of MessageQueue, which is built-in MapModels. These dialogs
are a tool for displaying conversations, questions, etc.
"""

import pygame

from librpg.locals import *
from librpg.config import dialog_config as cfg
from librpg.config import graphics_config as g_cfg
from librpg.config import game_config as m_cfg
from librpg.virtualscreen import get_screen
from librpg.context import Context


def build_lines(text, box_width, box_height, font, spacing, border_width,
                last_y_offset=0):
    lines = []
    words = text.split()
    cur_line = words[0]
    last_y = last_y_offset
    next_line_last_loop = True

    for word in words[1:]:
        projected_line = cur_line + ' ' + word
        width, height = font.size(projected_line)
        if width > box_width - 2 * cfg.border_width:
            lines.append([last_y, cur_line])
            last_y += height + spacing
            cur_line = word
            next_line_last_loop = True
        else:
            cur_line += ' ' + word
            next_line_last_loop = False
    lines.append([last_y, cur_line])
    if not next_line_last_loop:
        last_y += height + spacing
    return lines, last_y


class Dialog(object):

    def process_event(self, event):
        raise NotImplementedError, 'Dialog.process_event() is abstract'


class MessageDialog(Dialog):

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
            box_width = g_cfg.screen_width - 2 * cfg.border_width
            self.lines, _ = build_lines(self.text,
                                        box_width,
                                        0,
                                        font,
                                        cfg.line_spacing,
                                        cfg.border_width)

            # Draw message
            for line in self.lines:
                self.surface.blit(font.render(line[1], True, cfg.font_color),
                                  (2 * cfg.border_width, 2 * cfg.border_width +
                                   line[0]))

        return self.surface, pygame.Rect(0, g_cfg.screen_height / 2,
                                         g_cfg.screen_width,
                                         g_cfg.screen_height / 2)

    def process_event(self, event):
        if event.key in m_cfg.key_action:
            return False
        else:
            return True


class ChoiceDialog(Dialog):

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
            self.__build_lines(font)

            # Draw message
            for line in self.lines:
                self.surface.blit(font.render(line[1], True, cfg.font_color),
                                  (2 * cfg.border_width,
                                   2 * cfg.border_width + line[0]))
                                   
            for n, line in enumerate(self.choice_lines):
                if n == self.selected:
                    color = cfg.selected_font_color
                else:
                    color = cfg.not_selected_font_color
                    
                self.surface.blit(font.render(line[1], True, color),
                                  (3 * cfg.border_width,
                                   2 * cfg.border_width + line[0]))


        return self.surface, pygame.Rect(0, g_cfg.screen_height / 2,
                                         g_cfg.screen_width,
                                         g_cfg.screen_height / 2)

    def __build_lines(self, font):
        box_width = g_cfg.screen_width - 2 * cfg.border_width
        self.lines, y_offset = build_lines(self.text,
                                           box_width,
                                           0,
                                           font,
                                           cfg.line_spacing,
                                           cfg.border_width)

        box_width = g_cfg.screen_width - 3 * cfg.border_width
        self.choice_lines = []
        for choice in self.choices:
            choice_line, y_offset = build_lines(choice,
                                                box_width,
                                                0,
                                                font,
                                                cfg.choice_line_spacing,
                                                cfg.border_width,
                                                y_offset)
            self.choice_lines.extend(choice_line)

    def process_event(self, event):
        if event.key in m_cfg.key_action:
            return False
        elif event.key in m_cfg.key_up:
            self.selected = (self.selected - 1) % len(self.choice_lines)
            self.update()
        elif event.key in m_cfg.key_down:
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
