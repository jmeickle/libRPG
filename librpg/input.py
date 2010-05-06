#
# Wrapper for the pygame input module
#
# Copyright (C) 2009 Thadeus Burgess
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see /www.gnu.org/licenses/>
 
__author__="Thadeus Burgess &lt;thadeusb@thadeusb.com&gt;"
__date__ ="$Mar 23, 2009 12:20:34 AM$"
 
import pygame
from pygame.locals import *
 
class Input(object):
    """
    Wrapper for the pygame input module
 
    To check a key use the pygame.locals. Such as K_a, K_d, K_ESC, etc.
    To check a mouse event use "MB1", "MB2", "MB3", etc.
    To check exit event use "QUIT"
 
    Support for up to 10 mouse buttons.
 
    Uses:
 
    Input[KEY] - Returns the pygame.event for KEY
    Input.isset(KEY) - True if there is an event for KEY
    Input.get(KEY) - Retrieve tuple of (pygame.event, status)
    Input.event(KEY) - Retrieve pygame event of key
    Input.stat(KEY) - Retrieve status value of key
    Input.down(KEY) - True if the key is a down event
    Input.motion(KEY) - True if the key is being held down
    Input.up(KEY) - True if the key is an up event
    """
    DOWN = 1
    MOTION = 2
    UP = 3
    mice = (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION)
    butt = {
            1: "MB1",
            2: "MB2",
            3: "MB3",
            4: "MB4",
            5: "MB5",
            6: "MB6",
            7: "MB7",
            8: "MB8",
            9: "MB9",
            10: "MB10",
    }
    events = {}
 
    button_state = ()
    mouse_pos = ()
 
    class __metaclass__(type):
        def __getitem__(self, name):
            """
            Get the event.
            """
            try:
                event = Input.events[name][0]
            except KeyError:
                event = None
 
            return event
 
    @classmethod
    def add_event(cls, event):
        """
        Add a single pygame.event to the dictionary.
        """
        if event.type == KEYDOWN:
            Input.events.update({event.key: [event, Input.DOWN]})
        elif event.type == KEYUP:
            Input.events.update({event.key: [event, Input.UP]})
        elif event.type == MOUSEBUTTONDOWN:
            Input.events.update({Input.butt[event.button]: [event, Input.DOWN]})
        elif event.type == MOUSEBUTTONUP:
            Input.events.update({Input.butt[event.button]: [event, Input.UP]})
        elif event.type == MOUSEMOTION:
            Input.events.update({MOUSEMOTION: [event, Input.MOTION]})
        elif event.type == pygame.QUIT:
            Input.events.update({'QUIT': [event, True]}) # Fix by Gautham (comment on the blog)
 
    @classmethod
    def add_events(cls, events):
        """
        Add a list of pygame.events to the dictionary
        Expects a pygame.event.get() as the argument.
        """
        for event in events:
            Input.add_event(event)
 
    @classmethod
    def get(cls, name):
        """
        Returns a list containing the pygame.event and a status code
        """
        return Input.events.get(name)
 
    @classmethod
    def event(cls, name):
        """
        Returns the pygame.event
        """
        event = Input.get(name)
 
        if event != None:
            event = event[0]
 
        return event
 
    @classmethod
    def stat(cls, name):
        """
        Returns the status code
        """
        event = Input.get(name)
 
        if event != None:
            status = event[1]
        else:
            status = None
 
        return status
 
    @classmethod
    def isset(cls, name):
        """
        Is there an event for name
        """
        return name in Input.events
 
    @classmethod
    def down(cls, name):
        """
        Is the event in a down state.
        Did the user press the key or button now
        """
        return Input.stat(name) == Input.DOWN
 
    @classmethod
    def motion(cls, name):
        """
        If the key is being held down.
        """
        return Input.stat(name) == Input.MOTION
 
    @classmethod
    def up(cls, name):
        """
        Has the key just been released
        """
        return Input.stat(name) == Input.UP
 
    @classmethod
    def update_mouse(cls, buttons = (0,0,0), pos = (0,0)):
        """
        Updates the mouse postion and the three main buttons state.
        pygame.mouse.get_pos() and pygame.mouse.get_pressed()
        """
        Input.mouse_pos = pos
        Input.button_state = buttons
 
    @classmethod
    def update(cls):
        """
        Updates the list to reflect the end of a game cycle.
        This way events that are in a down state get moved to
        a motion state (being held down) and events that are in
        a up state get removed from the list.
        """
        flag = []
 
 
        for i in Input.events:
            if Input.events[i][0].type == KEYDOWN:
                Input.events[i][1] = Input.MOTION
            elif Input.events[i][0].type == KEYUP:
                flag.append(i)
            elif i == MOUSEMOTION:
                flag.append(i)
            elif i in Input.butt.values():
                if i.startswith("MB"):
                    if Input.down(i):
                        Input.events[i][1] = Input.MOTION
                    if Input.up(i):
                        flag.append(i)
 
        for i in flag:
            del Input.events[i]
 
    @classmethod
    def tostring(cls):
        """
        Print the list of events.
        """
        #for i in Input.events:
            #print Input.events[i]
        if len(Input.events) > 0:
            print Input.events
 
    @classmethod
    def down_unset(cls, name):
        """
        Is the event in a down state.
        Did the user press the key or button now
        """
        if Input.stat(name) == Input.DOWN:
            del Input.events[name]
            return True
        else:
            return False
