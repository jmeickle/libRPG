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


def build_lines(text, box_width, font):
    lines = []
    words = text.split()
    cur_line = words[0]
    _, height = font.size(cur_line)

    for word in words[1:]:
        projected_line = cur_line + ' ' + word
        width, height = font.size(projected_line)
        if width > box_width:
            lines.append([height, cur_line])
            cur_line = word
        else:
            cur_line += ' ' + word
    lines.append([height, cur_line])
    return lines

def split_boxes(lines, box_height, line_spacing):
    boxes = []
    box_cur_height = lines[0][0]
    box = [lines[0]]

    for line in lines[1:]:
        if box_cur_height + line[0] + line_spacing > box_height:
            boxes.append(box)
            box_cur_height = line[0]
            box = [line]
        else:
            box.append(line)
            box_cur_height += line[0] + line_spacing
    if box:
        boxes.append(box)

    return boxes

class Dialog(object):

    def __init__(self, block_movement=True):
        self.block_movement = block_movement

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
        Dialog.__init__(self, block_movement)
        self.text = text
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
            box_width = g_cfg.screen_width - 4 * cfg.border_width
            lines = build_lines(self.text,
                                box_width,
                                font)

            # Draw message
            y_acc = 0
            for line in lines:
                self.surface.blit(font.render(line[1], True, cfg.font_color),
                                  (2 * cfg.border_width, 2 * cfg.border_width +
                                   y_acc))
                y_acc += line[0] + cfg.line_spacing

        return self.surface, pygame.Rect(0, g_cfg.screen_height / 2,
                                         g_cfg.screen_width,
                                         g_cfg.screen_height / 2)

    def process_event(self, event):
        if event.key in m_cfg.key_action:
            return False
        else:
            return True


class ElasticMessageDialog(MessageDialog):

    """
    Same as a MessageDialog but resizes the box as needed for the text to
    fit in.
    """
    def draw(self):
        if not self.surface:
            font = pygame.font.SysFont(cfg.font_name, cfg.font_size)

            # Split into lines
            box_width = g_cfg.screen_width - 4 * cfg.border_width
            lines = build_lines(self.text,
                                box_width,
                                font)

            # Calculate box size
            self.box_height = (sum([line[0] for line in lines])
                          + (len(lines) - 1) * cfg.line_spacing
                          + 4 * cfg.border_width)
            assert self.box_height < g_cfg.screen_height,\
                   'Too much text for one box.'

            # Create empty surface
            self.surface = pygame.Surface((g_cfg.screen_width,
                                           self.box_height), SRCALPHA,
                                           32)

            # Draw dialog background
            dim = pygame.Rect((cfg.border_width, cfg.border_width),
                              (g_cfg.screen_width - 2 * cfg.border_width,
                               self.box_height - 2 * cfg.border_width))
            pygame.draw.rect(self.surface, cfg.bg_color, dim)

            # Draw message
            y_acc = 0
            for line in lines:
                self.surface.blit(font.render(line[1], True, cfg.font_color),
                                  (2 * cfg.border_width, 2 * cfg.border_width +
                                   y_acc))
                y_acc += line[0] + cfg.line_spacing

        return self.surface, pygame.Rect(0,
                                         g_cfg.screen_height - self.box_height,
                                         g_cfg.screen_width,
                                         self.box_height)


class MultiMessageDialog(MessageDialog):
    
    """
    Same as a MessageDialog but splits messages bigger than the default
    box size into multiple dialogs.
    """
    
    def __init__(self, text, block_movement=True):
        MessageDialog.__init__(self, text, block_movement)
        self.surfaces = None

    def draw(self):
        if not self.surfaces:
            self.surfaces = []
            font = pygame.font.SysFont(cfg.font_name, cfg.font_size)

            # Split into lines
            box_width = g_cfg.screen_width - 4 * cfg.border_width
            lines = build_lines(self.text,
                                box_width,
                                font)
            
            # Split into boxes
            box_height = g_cfg.screen_height / 2 - 4 * cfg.border_width
            self.boxes = split_boxes(lines, box_height, cfg.line_spacing)

            for box in self.boxes:

                # Create empty surface
                surface = pygame.Surface((g_cfg.screen_width,
                                          g_cfg.screen_height / 2), SRCALPHA,
                                          32)

                # Draw dialog background
                dim = pygame.Rect((cfg.border_width, cfg.border_width),
                                  (g_cfg.screen_width - 2 * cfg.border_width,
                                   g_cfg.screen_height / 2 - 2 * cfg.border_width))
                pygame.draw.rect(surface, cfg.bg_color, dim)

                # Draw message
                y_acc = 0
                for line in box:
                    surface.blit(font.render(line[1], True, cfg.font_color),
                                             (2 * cfg.border_width,
                                              2 * cfg.border_width + y_acc))
                    y_acc += line[0] + cfg.line_spacing

                self.surfaces.append(surface)

        return self.surfaces[0], pygame.Rect(0, g_cfg.screen_height / 2,
                                             g_cfg.screen_width,
                                             g_cfg.screen_height / 2)

    def process_event(self, event):
        if event.key in m_cfg.key_action:
            del self.surfaces[0]
            if self.surfaces:
                return True
            else:
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
        Dialog.__init__(self, block_movement)
        self.text = text
        self.choices = choices
        self.surface = None
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
            y_acc = 0
            for line in self.lines:
                self.surface.blit(font.render(line[1], True, cfg.font_color),
                                  (2 * cfg.border_width,
                                   2 * cfg.border_width + y_acc))
                y_acc += line[0] + cfg.line_spacing

            for n, line in enumerate(self.choice_lines):
                if n == self.selected:
                    color = cfg.selected_font_color
                else:
                    color = cfg.not_selected_font_color

                self.surface.blit(font.render(line[1], True, color),
                                  (3 * cfg.border_width,
                                   2 * cfg.border_width + y_acc))
                y_acc += line[0] + cfg.choice_line_spacing


        return self.surface, pygame.Rect(0, g_cfg.screen_height / 2,
                                         g_cfg.screen_width,
                                         g_cfg.screen_height / 2)

    def __build_lines(self, font):
        box_width = g_cfg.screen_width - 4 * cfg.border_width
        self.lines = build_lines(self.text,
                                 box_width,
                                 font)

        box_width = g_cfg.screen_width - 5 * cfg.border_width
        self.choice_lines = []
        for choice in self.choices:
            choice_line = build_lines(choice,
                                      box_width,
                                      font)
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
