import pygame
from pygame.locals import *

from librpg.locals import *
from librpg.virtual_screen import get_screen

class ContextStack(object):

    def __init__(self):
        self.stack = []

    def stack_context(self, context):
        self.stack.append(context)
        self.__inserted_context(context)

    def insert_context(self, context, index):
        self.stack.insert(index, context)
        self.__inserted_context(context)

    def remove_context(self, context):
        try:
            self.stack.remove(context)
        except ValueError:
            return None
        self.__destroyed_context(context)
        return context

    def stop(self):
        self.keep_going = False

    def __inserted_context(self, context):
        context.initialize()

    def __destroyed_context(self, context):
        context.destroy()
        for possible_child in self.stack:
            if possible_child.parent is context:
                self.remove_context(possible_child)

    def gameloop(self):
        self.keep_going = True
        self.clock = pygame.time.Clock()
        while self.stack and self.keep_going:
            self.clock.tick(FPS)
            for context in self.stack:
                if context.active:
                    context.step()
                    context.draw()
            get_screen().flip()
            

            self.__process_events()

    def __process_events(self):
        for event in pygame.event.get():
            # print event
            for context in reversed(self.stack):
                consumed_event = context.process_event(event)
                if consumed_event:
                    break


class Context(object):

    def __init__(self, parent=None):
        self.active = True
        self.parent = parent

    # Virtual
    def process_event(self, event):
        return False

    # Virtual
    def step(self):
        pass

    # Virtual
    def initialize(self):
        pass

    # Virtual
    def draw(self):
        pass

    # Virtual
    def destroy(self):
        pass

    def stop(self):
        removed = get_context_stack().remove_context(self)
        if removed is not None:
            self.destroy()

context_stack = ContextStack()

def get_context_stack():
    return context_stack
