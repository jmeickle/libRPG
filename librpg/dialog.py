"""
The :mod:`dialog` module contains Dialogs that can be displayed through
the use of MessageQueue, which is built-in MapModels. These dialogs
are a tool for displaying conversations, questions, etc.
"""

from librpg.locals import KEYDOWN
from librpg.color import TRANSPARENT
from librpg.config import dialog_config as cfg
from librpg.config import graphics_config as g_cfg
from librpg.config import game_config as m_cfg
from librpg.config import menu_config
from librpg.context import Context
from librpg.menu import (Menu, Label, Panel, Cursor, ArrowCursorTheme)
from librpg.input import Input


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


class MessageDialog(Menu):

    """
    A MessageDialog is a simple message to be displayed on the screen.

    *text* is the string that will be displayed and *block_movement*
    tells the map whether the movement in the map should be blocked while
    the message is shown.
    """

    def __init__(self, text, block_movement=True):
        self.text = text
        self.block_movement = block_movement

        Menu.__init__(self, g_cfg.screen_width - 2 * cfg.border_width,
                            g_cfg.screen_height / 2 - 2 * cfg.border_width,
                            cfg.border_width,
                            g_cfg.screen_height / 2 + cfg.border_width,
                            bg=TRANSPARENT,
                            blocking=block_movement)

        panel = Panel(self.width, self.height)
        self.add_widget(panel, (0, 0))

        font = self.theme.get_font(cfg.font_size)
        box_width = g_cfg.screen_width - 4 * cfg.border_width
        lines = build_lines(self.text,
                            box_width,
                            font)

        # Draw message
        y_acc = 0
        for line in lines:
            label = Label(line[1])
            panel.add_widget(label,
                             (cfg.border_width,
                              cfg.border_width + y_acc))
            y_acc += line[0] + cfg.line_spacing

    def activate(self):
        self.close()


class ElasticMessageDialog(Menu):

    """
    Same as a MessageDialog but resizes the box as needed for the text to
    fit in.
    """

    def __init__(self, text, block_movement=True):
        self.text = text
        self.block_movement = block_movement

        # Split into lines
        theme = menu_config.theme
        font = theme.get_font(cfg.font_size)
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

        Menu.__init__(self, g_cfg.screen_width - 2 * cfg.border_width,
                            self.box_height - 2 * cfg.border_width,
                            cfg.border_width,
                            g_cfg.screen_height - self.box_height\
                            + cfg.border_width,
                            bg=TRANSPARENT,
                            blocking=block_movement)

        panel = Panel(self.width, self.height)
        self.add_widget(panel, (0, 0))

        # Draw message
        y_acc = 0
        for line in lines:
            label = Label(line[1])
            panel.add_widget(label,
                             (cfg.border_width,
                              cfg.border_width + y_acc))
            y_acc += line[0] + cfg.line_spacing

    def activate(self):
        self.close()


class MultiMessageDialog(Menu):

    """
    Same as a MessageDialog but splits messages bigger than the default
    box size into multiple dialogs.
    """

    def __init__(self, text, block_movement=True):
        self.text = text
        self.block_movement = block_movement
        self.current_panel = None

        Menu.__init__(self, g_cfg.screen_width - 2 * cfg.border_width,
                            g_cfg.screen_height / 2 - 2 * cfg.border_width,
                            cfg.border_width,
                            g_cfg.screen_height / 2 + cfg.border_width,
                            bg=TRANSPARENT,
                            blocking=block_movement)

        # Split into lines
        font = self.theme.get_font(cfg.font_size)
        box_width = g_cfg.screen_width - 4 * cfg.border_width
        lines = build_lines(self.text,
                            box_width,
                            font)

        # Split into boxes
        box_height = g_cfg.screen_height / 2 - 4 * cfg.border_width
        self.boxes = split_boxes(lines, box_height, cfg.line_spacing)
        self.panels = []

        # Draw panels
        for box in self.boxes:
            panel = Panel(self.width, self.height)
            y_acc = 0
            for line in box:
                label = Label(line[1])
                panel.add_widget(label,
                                 (cfg.border_width,
                                  cfg.border_width + y_acc))
                y_acc += line[0] + cfg.line_spacing
            self.panels.append(panel)

        self.advance_panel()

    def advance_panel(self):
        if self.current_panel is not None:
            self.remove_widget(self.current_panel)
            self.current_panel = None
        if self.panels:
            self.current_panel = self.panels.pop(0)
            self.add_widget(self.current_panel, (0, 0))

    def activate(self):
        self.advance_panel()
        if self.current_panel is None:
            self.close()


class ChoiceDialog(Menu):

    """
    A ChoiceDialog is a message that comes along a list of options from
    which the player has to pick one option.

    *text* is the string that will be displayed and *block_movement*
    tells the map whether the movement in the map should be blocked while
    the message is shown.

    *choices* is a list of tuples with the options, which should be strings.

    *completion_callback* is a function that will be called passing
    *user_data* and the number of the choice made by the player, when
    they do so. If is it not specified, the on_choice() method has
    to be implemented.

    *user_data* will be passed to *completion_callback*. This can be used
    to access anything the callback is supposed to use, like the map,
    the party avatar, the map object, and so on.
    """

    def __init__(self, text, choices, user_data=None, completion_callback=None,
                 block_movement=True):
        self.block_movement = block_movement
        self.text = text
        self.choices = choices
        self.completion_callback = completion_callback
        self.user_data = user_data

        Menu.__init__(self, g_cfg.screen_width - 2 * cfg.border_width,
                            g_cfg.screen_height / 2 - 2 * cfg.border_width,
                            cfg.border_width,
                            g_cfg.screen_height / 2 + cfg.border_width,
                            bg=TRANSPARENT,
                            blocking=block_movement)

        panel = Panel(self.width, self.height)
        self.add_widget(panel, (0, 0))

        # Build lines and choice lines
        font = self.theme.get_font(cfg.font_size)
        self.__build_lines(font)

        # Draw message
        y_acc = 0
        for line in self.lines:
            label = Label(line[1], focusable=False)
            panel.add_widget(label,
                             (cfg.border_width,
                              cfg.border_width + y_acc))
            y_acc += line[0] + cfg.line_spacing

        self.starting_option = None
        for index, line in enumerate(self.choice_lines):
            label = ChoiceLabel(line[1], index)
            panel.add_widget(label,
                             (2 * cfg.border_width,
                              cfg.border_width + y_acc))
            y_acc += line[0] + cfg.choice_line_spacing
            if self.starting_option is None:
                self.starting_option = label

        Cursor(ArrowCursorTheme()).bind(self, self.starting_option)

    def __build_lines(self, font):
        box_width = self.width - 2 * cfg.border_width
        self.lines = build_lines(self.text,
                                 box_width,
                                 font)

        box_width = self.width - 3 * cfg.border_width
        self.choice_lines = []
        for choice in self.choices:
            choice_line = build_lines(choice,
                                      box_width,
                                      font)
            self.choice_lines.extend(choice_line)

    def complete(self, choice):
        self.result = choice
        if self.completion_callback is not None:
            self.completion_callback(self.user_data, choice)
        self.on_choice(self.user_data, choice)

    def on_choice(self, user_data, choice):
        """
        *Virtual.*

        Execute an action depending on what the player chose.

        If no *completion_callback* is specified in constructor, this
        method has to be overridden.

        *user_data* is the user_data passed to the ChoiceDialog when it was
        written.

        *choice* is the index of the choice. The first option is 0, the
        second is 1, and so on.
        """
        pass


class ChoiceLabel(Label):

    def __init__(self, text, index):
        Label.__init__(self, text, focusable=True)
        self.index = index

    def activate(self):
        self.menu.complete(self.index)
        self.menu.close()
        return True

    def update_input(self):
        for key in m_cfg.key_left.union(m_cfg.key_right):
            Input.was_pressed(key)


class MessageQueue(Context):

    def __init__(self, parent=None):
        Context.__init__(self, parent)
        self.current = None
        self.controller = None
        self.queue = []

    def is_busy(self):
        return self.current is not None and self.current.block_movement

    def is_active(self):
        return self.current is not None

    def pop_next(self):
        if self.current is None and self.queue:
            self.current = self.queue.pop(0)
            self.current.open()
            self.controller = self.current.get_controller()

    def push(self, message):
        self.queue.append(message)

    def update(self):
        if self.controller is not None and self.controller.is_done():
            self.current = None
        self.pop_next()
        return False
