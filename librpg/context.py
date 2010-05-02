"""
The :mod:`context` module is used to allow asynchronous processes running
concurrently but synchronized with the gameloop.

Two basic classes are defined here, the Context, which represents a
process, and the ContextStack, which manages Contexts. The module also
defines a global ContextStack, accessible through the method
context.get_context_stack().
"""

import pygame

from librpg.locals import *
from librpg.config import game_config
from librpg.virtualscreen import get_screen
from librpg.animation import get_metronome


class ContextStack(object):

    """
    A ContextStack organizes Contexts in a stack and runs them.

    The stack of Contexts defines the orders of updating, drawing and
    receiving events. The latter happens from the most recently inserted
    Contexts to the oldest ones (top-down), which the formers do the
    opposite (bottom-up).

    :attr:`stack`
    List representing the Context stack. Do not modify it directly.
    Instead use the insert_context() and remove_context() methods.
    """

    def __init__(self):
        self.stack = []

    def stack_context(self, context):
        """
        *context* is inserted as the top Context in the stack, meaning
        it will be the first to be offered in incoming event, and the last
        to be updated and drawn.

        This method causes the Context to be initialized.
        """
        self.stack.append(context)
        self.__inserted_context(context)

    def insert_context(self, context, index):
        """
        *context* is inserted at the given *index*, pushing the ones above
        one position upwards.

        This method causes the Context to be initialized.
        """
        self.stack.insert(index, context)
        self.__inserted_context(context)

    def remove_context(self, context):
        """
        Remove *context* from the stack, wherever it is.

        This method causes the Context and all Contexts that were created
        as its child to be destroyed.
        """
        try:
            self.stack.remove(context)
        except ValueError:
            return None
        self.__destroyed_context(context)
        return context

    def stop(self):
        """
        Once called, the gameloop will stop right after the current
        iteration.
        """
        self.keep_going = False

    def __inserted_context(self, context):
        context.initialize()

    def __destroyed_context(self, context):
        context.destroy()
        for possible_child in self.stack:
            if possible_child.parent is context:
                self.remove_context(possible_child)

    def gameloop(self, current=None):
        """
        This method transfers the control flow to the ContextStack,
        which will keep its stacked Contexts running until one of them
        calls ContextStack.stop() or they are all removed from the
        ContextStack.

        The ContextStack will cap the cycles/second at game_config.fps.
        In each cycle, the following will happen:

        1) For each active context in the map, bottom-up:
            a) The update() method of that Context will be called
            b) The draw() method of that Context will be drawn
        2) The screen will be flipped so that the screen receives all the
           updates at once.
        3) For each incoming event:
            a) For each context, top-down:
                i) The event will be offered to the context.
                ii) The context will choose to pass down or hold the
                    event, no matter if it was actually used or not.
                iii) If the context chose not to pass down, continue to
                     do 3.
        4) If anyone called ContextStack.stop() or if there are no
           Contexts in the stack, stop.
        """
#        print 'gameloop started'
        self.keep_going = True
        self.clock = pygame.time.Clock()
        while self.stack and self.keep_going:
            # Limit FPS
            self.clock.tick(game_config.fps)
            get_metronome().step()

            # Update contexts in reverse order
            stop = False
            for context in reversed(self.stack):
                if context.active:
                    stop = context.update()
                if stop:
                    break

            # Draw active contexts in normal order
            for context in self.stack:
                context.draw()

            # Flip display
            get_screen().flip()

            # Distribute pygame events to contexts
            self.__process_events()
            
            if current is not None and current not in self.stack:
                self.keep_going = False
#        print 'gameloop ended'
        self.keep_going = True


    def __process_events(self):
        for event in pygame.event.get():
#            if event.type != MOUSEMOTION: 
#                print 'processing', event
            if event.type == QUIT:
                self.stop()
                break
            for context in reversed(self.stack):
#                if event.type != MOUSEMOTION:
#                    print 'offering to', context
                consumed_event = context.process_event(event)
                if consumed_event:
#                    if event.type != MOUSEMOTION:
#                        print context, 'consumed the event'
                    break

    def stack_model(self, model):
        """
        Insert the Context created by *model*.create_context() as the
        top Context of the stack.

        This method causes the Context to be initialized.
        """
        context = model.get_controller()
        self.stack_context(context)


class Context(object):

    """
    A Context is an asynchronous process that will be run
    concurrently with other processes.

    Contexts may be a variety of features, ranging from information
    on the screen (life bars, money counters, compasses), custom actions
    (a button to change the party order, capturing mouse clicks to give
    information about clicked objects) to menus that run along with the
    map, allowing them to be used while the party moves.
    """

    def __init__(self, parent=None):
        """
        *Constructor.*

        *parent* should be another Context that, when removed from the
        stack, will cause this Context to also be removed. Contexts might
        not have a parent.
        """
        self.active = True
        self.parent = parent

    # Virtual
    def process_event(self, event):
        """
        *Virtual.*

        Handle the incoming event. Return True if it should NOT be passed
        down to the lower Contexts (that is, if it should be captured).
        Return False if it should be passed down.

        Note that not passing down events of a certain type (eg. direction
        key presses) will deprive lower Contexts of that event, which can
        be used to block movement for example.

        By default, process_event() returns False.
        """
        return False

    # Virtual
    def update(self):
        """
        *Virtual.*

        Update the Context for the current iteration.

        This method should do whatever periodic processing the context
        needs, information updates, etc.

        Return True if the contexts below it should not be updated this
        cycle, False otherwise. By default, update() returns False.
        """
        return False

    # Virtual
    def initialize(self):
        """
        *Virtual.*

        Initialize a context to be run.

        This method will be called when the Context is added to a
        ContextStack.
        """
        pass

    # Virtual
    def draw(self):
        """
        *Virtual.*

        Draw whatever output the Context wants to blit on the screen.

        This method should access the screen by calling
        virtual_screen.get_screen() and then blit into it. The flip()
        method should not be called, as the ContextStack will do so after
        all Contexts are done drawing.
        """
        pass

    # Virtual
    def destroy(self):
        """
        *Virtual.*

        Destroy a context that just stopped.

        This method will be called when the Context is removed from a
        ContextStack. It does not have to actually destroy the Context,
        but do whatever deinitialization that applies.
        """
        pass

    def stop(self):
        """
        Stop the Context from running and remove it from its ContextStack.
        """
        removed = get_context_stack().remove_context(self)
        if removed is not None:
            self.destroy()


class Model(object):

    """
    A Model is an object controlled by a Context. Inheriting from this
    class allows the model to be stacked onto the ContextStack with the
    stack_model() method.

    *controller_parent* should be a Context that will be the parent of
    the Model's controller. If None or not specified, it will not have
    a parent.
    """

    def __init__(self, controller_parent=None):
        self.controller = None
        self.controller_parent = controller_parent

    def create_controller(self):
        """
        *Abstract.*

        Create a controller derived from Context for this model.
        """
        raise NotImplementedError('Model.create_controller() is abstract.')

    def get_controller(self):
        """
        Return the model's controller, creating with create_controller()
        it if it has not been created already.
        """
        if self.controller is None:
            self.controller = self.create_controller()
        return self.controller
    
    def sync_open(self):
        stack = get_context_stack()
        stack.stack_model(self)
        stack.gameloop(self.get_controller())


context_stack = ContextStack()


def get_context_stack():
    """
    Return the global ContextStack.
    """
    return context_stack
