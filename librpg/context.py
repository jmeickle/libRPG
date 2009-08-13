import pygame
from pygame.locals import *

from librpg.locals import *

class ContextStack:

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
        context.destroy()
        context.context_stack = None
        return context

    def stop(self):
        self.keep_going = False

    def __inserted_context(self, context):
        context.initialize()
        context.context_stack = self

    def gameloop(self):
        self.keep_going = True
        self.clock = pygame.time.Clock()
        while self.stack and self.keep_going:
            self.clock.tick(FPS)
            for context in self.stack:
                if context.active:
                    context.step()
                    context.draw()
            self.__process_events()

    def __process_events(self):
        for event in pygame.event.get():
            #print event
            for context in reversed(self.stack):
                consumed_event = context.process_event(event)
                if consumed_event:
                    break


class Context(object):

    def __init__(self):
        self.active = True

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
        removed = self.context_stack.remove_context(self)
        if removed is not None:
            self.destroy()
